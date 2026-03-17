+++
title = "625. 계층형 파일 시스템 (UnionFS / OverlayFS)"
date = "2026-03-14"
weight = 625
+++

# 625. 계층형 파일 시스템 (UnionFS / OverlayFS)

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 물리적으로 분리된 저장소를 논리적으로 합치는 유니언 마운트(Uinion Mount) 기술로, 리눅스 커널 레벨에서 VFS (Virtual File System)를 통해 추상화됩니다.
> 2. **가치**: 컨테이너 이미지의 계층화를 통해 스토리지 효율을 극대화하며, Copy-on-Write (CoW) 메커니즘으로 초고속 스냅샷과 배포를 지원합니다.
> 3. **융합**: 리눅스 커널의 Namespace와 Cgroup(Control Group) 기반의 컨테이너 가상화 환경에서 필수적인 스토리지 백엔드로 활용됩니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**UnionFS (Union File System)** 또는 **OverlayFS**는 서로 다른 물리적 파티션이나 디렉토리를 하나의 논리적 디렉토리로 합쳐서(Merge) 보여주는 기술입니다. 사용자 입장에서는 여러 디스크가 합쳐진 하나의 드라이브처럼 보이지만, 내부적으로는 레이어(Layer) 구조로 관리됩니다.

- **핵심 철학**: "분리된 책임과 효율적인 공유". 변하지 않는 데이터(Infrastructure)와 변하는 데이터(Application)를 분리하여 관리합니다.
- **VFS (Virtual File System)**: 리눅스 커널의 파일 시스템 인터페이스 계층으로, OverlayFS는 이 표준 인터페이스를 준수하여 다양한 파일 시스템(ext4, xfs 등) 위에 구축될 수 있습니다.

#### 2. 등장 배경 및 진화 과정
① **기존 한계**: 전체 가상머신(VM) 이미지를 복제하여 사용하는 방식은 디스크 공간 낭비가 심하고, 이미지 업데이트 시 전체 복사가 필요하여 관리 비용이 증가했습니다.
② **혁신적 패러다임**: 레고 블록처럼 베이스 이미지 위에 변경 사항만 덧붙이는 **Layered Storage** 개념이 도입되었습니다. 이를 통해 수정 불가능한(Immutable) 인프라와 수정 가능한(Mutable) 상태를 분리했습니다.
③ **비즈니스 요구**: 클라우드 네이티브(Cloud Native) 환경에서 초당 수백 개의 컨테이너가 생성되고 파괴되는 상황에서, Zero-Copy에 가까운 속도로 인스턴스를 기동해야 한다는 요구가 OverlayFS의 표준화(Kernel 3.18+ 포함)를 이끌었습니다.

#### 3. ASCII 다이어그램: 레이어 개념 도식화
```text
+-------------------+  [ Layer 3: Application Layer ]
|   Python App      |  (사용자 코드, 변경 잦음)
+-------------------+
         |
         v (Union Mount)
+-------------------+  [ Layer 2: Runtime Layer ]
|   Python 3.9      |  (라이브러리 의존성, 반변경)
+-------------------+
         |
         v (Union Mount)
+-------------------+  [ Layer 1: OS Base Layer ]
|   Ubuntu 22.04    |  (베이스 OS, 거의 변경 없음)
+-------------------+
```
> **해설**: 각 레이어는 독립적인 파일 시스템(또는 디렉토리)입니다. 사용자는 최상위에서 이 모든 레이어가 합쳐진 하나의 파일 시스템(Merged View)을 인식하게 됩니다. 이 구조는 디스크 블록 레벨의 중복을 제거합니다.

📢 **섹션 요약 비유**: 계층형 파일 시스템은 **"투명한 OHP 필름 여러 장에 각각 다른 그림을 그린 뒤, 겹쳐서 하나의 완성된 그림을 투사하는 것"**과 같습니다. 밑의 필름(베이스)은 건드리지 않고, 위에 필름(변경사항)을 얹어 내용을 수정하거나 추가할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 (Component Table)
OverlayFS의 핵심은 하위 디렉토리(Lower)와 상위 디렉토리(Upper)를 결합하는 메커니즘입니다.

| 요소명 | 영문명 | 속성 | 역할 및 내부 동작 | 프로토콜/구조 |
|:---|:---|:---:|:---|:---|
| **하위 레이어** | LowerDir | **RO**<br>(Read Only) | 베이스 이미지를 구성합니다. 하나 이상의 디렉토리를 스택(Stack)할 수 있으며, 수정이 불가능합니다. | 디렉토리 스택 구조 |
| **상위 레이어** | UpperDir | **RW**<br>(Read/Write) | 컨테이너 실행 중 생성되거나 수정된 파일이 저장되는 공간입니다. 초기에는 비어있을 수 있습니다. | 일반 파일 시스템 |
| **작업 공간** | WorkDir | **RW**<br>(Internal) | 원자적 파일 이동(Atomic Rename) 등을 보장하기 위해 커널이 내부적으로 사용하는 임시 디렉토리입니다. 사용자는 직접 접근하지 않습니다. | 동일 파일 시스템 내에 필수 존재 |
| **통합 뷰** | MergedDir | **View** | 사용자 프로세스가 실제로 접근하는 마운트 포인트입니다. Lower와 Upper가 합쳐진 결과를 보여줍니다. | VFS 마운트 포인트 |

#### 2. 오버레이 아키텍처 ASCII 다이어그램
```text
[ User Process ]
      |
      | (Open / Read / Write)
      v
+-------------------------------------+
|  OverlayFS Kernel Module (VFS)      |
+-------------------------------------+
      |           |           |
      |           |           |
      v           v           v
+-----------+-----------+--------------+
|  UpperDir |  WorkDir  |  LowerDir    | <--- Physical Disks/Directories
| (Container| (Internal)| (Base Image) |
|  Changes) |           |  (Layer N)   |
+-----------+-----------+--------------+
      |                       ^
      | (Copy-Up Logic)       | (Read Reference)
      +-----------------------+
```
> **해설**:
> 1. **Read(읽기)**: 사용자가 파일을 요청하면 OverlayFS는 먼저 `UpperDir`을 확인합니다. 파일이 없으면 `LowerDir` 스택을 순회하여 파일을 찾습니다.
> 2. **Write(쓰기)**: 새 파일 생성은 `UpperDir`에 직접 기록됩니다.
> 3. **Modify(수정)**: `LowerDir`에 있는 파일을 수정하려는 시도가 발생하면, 파일을 `LowerDir`에서 `UpperDir`로 복사(Copy-up)한 뒤 `UpperDir`의 파일을 수정합니다.

#### 3. 심층 동작 원리: Copy-on-Write (CoW) 및 Whiteout
**CoW (Copy-on-Write)**는 OverlayFS의 성능과 효율성을 담당하는 핵심 알고리즘입니다.

1.  **읽기 동작 (Lookup & Read)**:
    -   파일 접근 시 `UpperDir` 검색 -> 없으면 `LowerDir` 검색 (하위 스택 순차 탐색).
    -   `dentry` (Directory Entry) 캐시를 활용하여 검색 성능을 최적화합니다.

2.  **쓰기 동작 (Copy-Up)**:
    -   Lower 레이어에 존재하는 파일에 대한 쓰기 요청(`open(O_WRONLY)`) 발생.
    -   커널은 해당 파일의 메타데이터와 데이터를 Upper 레이어로 복사합니다 (이때 I/O 비용 발생).
    -   이후 모든 연산은 Upper 레이어의 사본에 대해 수행됩니다.

3.  **삭제 동작 (Whiteout)**:
    -   Lower 레이어의 파일을 삭제할 수는 없습니다 (읽기 전용이므로).
    -   대신 Upper 레이어에 해당 파일 이름과 동일한 **Whiteout 파일** (문자 'c'가 있는 특수 파일)을 생성합니다.
    -   Merged View에서는 Whiteout 파일이 존재하는 경로를 하위 레이어의 파일이 존재하지 않는 것처럼 처리(Lookup 시 배제)합니다.

#### 4. 핵심 로직 코드 예시 (C 스타일 의사코드)
```c
// Pseudo-code for OverlayFS Lookup Logic
struct file *overlayfs_lookup(char *filename) {
    // 1. Check UpperDir (Writable Layer)
    struct file *f = lookup_in_upper(filename);
    if (f != NULL) {
        if (is_whiteout(f)) {
            return NULL; // File is "deleted" in the merged view
        }
        return f; // Return modified or new file
    }

    // 2. Check LowerDir (Read-Only Layers)
    f = lookup_in_lower_stack(filename);
    if (f != NULL) {
        return f; // Return original read-only file
    }

    return NULL; // File not found
}

int overlayfs_write(struct file *f) {
    if (is_from_lower_layer(f)) {
        // Trigger Copy-Up before writing
        copy_file_to_upper(f);
    }
    // Proceed to write in UpperDir
    return write_to_upper(f);
}
```

📢 **섹션 요약 비유**: **"밑그림(Lower) 위에 먹지(Work)를 대고, 새로운 종이(Upper)에 덧그리는 과정"**과 같습니다. 원본 밑그림(Lower)은 훼손되지 않으며, 수정이 필요한 부분만 위로 가져와서(Copy-up) 그립니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison)

#### 1. 심층 기술 비교: AUFS vs OverlayFS
초기 Docker는 AUFS를 사용했으나, 현재는 커널 표준인 OverlayFS(구현체: Overlay2)로 이동했습니다.

| 비교 항목 | AUFS (Advanced UnionFS) | OverlayFS / Overlay2 |
|:---|:---|:---|
| **커널 지원** | 비표준 (Mainline 미포함, 별도 패치 필요) | **Linux Kernel 3.18+ 표준 포함** |
| **성능 (Inode)** | 인덱스 생성 방식이 복잡하여 많은 파일 처리 시 성능 저하 | **인덱스를 매핑하여 성능 우수** (NFS 등에서도 안정적) |
| **복잡도** | 매우 복잡한 코드베이스 | 설계가 간단하고 유지보수 용이 |
| **안정성** | 오래 사용되었으나 커널 트리와 충돌 가능성 | 현대적 커널 구조와 통합, 안정적 |
| **Cache Performance** | 페이지 캐시 공유 메커니즘이 복잡함 | 페이지 캐시 공유가 최적화되어 있음 |

#### 2. 분석표: 정량적 스토리지 비교
동일한 베이스 이미지(1GB)를 사용하는 10개의 컨테이너 구동 시 가정.

| 구분 | 일반 파일 시스템 (Copy 방식) | 계층형 파일 시스템 (OverlayFS) |
|:---|:---:|:---:|
| **총 디스크 사용량** | 1GB × 10 = **10 GB** | 1GB (Base) + (10 × 10MB) ≈ **1.1 GB** |
| **컨테이너 생성 시간** | 전체 복사 시간 소요 (수~수십 초) | **즉시 (ms 단위, Layer Link만 생성)** |
| **이미지 업데이트** | 모든 인스턴스 재복사 필요 | 베이스 레이어만 교체하면 모든 컨테이너에 반영 |

#### 3. 타 영역 융합 관점
-   **OS/컴퓨터 구조**: OverlayFS는 하드웨어적인 가상화가 아닌, 운영체제 커널 차원의 **소프트웨어 격리(Software Isolation)**를 제공합니다. 이는 페이지 캐시(Page Cache)의 효율적인 공유를 가능하게 하여 메모리 사용량을 감소시킵니다.
-   **네트워크**: 네트워크 파일 시스템(NFS) 환경에서 OverlayFS를 구성할 경우, 다수의 클라이언트가 동일한 Lower 레이어를 마운트하여 네트워크 대역폭 절약 및 데이터 일관성을 유지할 수 있습니다.

📢 **섹션 요약 비유**: **"고속도로 통행료 징수"**와 비교할 수 있습니다. 모든 차량이 별도의 부스(Independent FS)를 설치하면 비용(디스크)이 많이 드지만, 하이패스 차로(OverlayFS)를 통해 공유 인프라(Lower Layer)를 효율적으로 이용하면 혼잡 비용을 줄이고 처리 속도를 높일 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy)

#### 1. 실무 시나리오 및 의사결정 과정
**[시나리오]** 대규모 CI/CD 파이프라인 구축 시 빌드 속도가 병목 현상이 발생함.

**[의사결정]**
1.  **문제 분석**: 매번 소스 코드를 빌드할 때 의존성 라이브러리(node_modules 등)를 새로 다운로드하거나 이미지 전체를 복사하는 데 시간이 소요됨.
2.  **기술 적용**: 베이스 이미지(의존성 포함)를 Lower 레이어로 두고, 소스 코드만 포함하는 레이어를 Upper로 구성하는 빌드 캐싱 전략 수립.
3.  **결과**: 변경된 소스 코드에 대한 레이어만 교체하여 빌드 시간을 90% 단축 (Disk I/O 감소).

#### 2. 도입 체크리스트 (Checklist)

| 구분 | 항목 | 확인 사항 |
|:---|:---:|:---|
| **기술적** | 파일 시스템 호환성 | 사용하려는 백엔드 파일 시스템(ext4, xfs, zfs 등)이 OverlayFS의 ftype(파일 타입) 기능을 지원하는가? (xfs는 ftype=1 필수) |
| **성능** | Page Fault 비용 | 대용량 파일(GB 급)을 수정하는 시나리오가 많은가? Copy-up 오버헤드가 크므로 이 경우 Volume Mount 권장 |
| **운영적** | 데이터 영속성 | 컨테이너 삭제 후에도 데이터가 보존되어야 하는가? 그렇다면 **절대** Upper 레이어에 저장해서는 안 되며, Host Volume이나 NAS로 마운트해야 함 |
| **보안적** | 권한 분리 | Rootless 모드 컨테이너를 사용 시 레이어 간 권한 충돌이 발생하지 않는가? (User Namespace 매핑 필요) |

#### 3. 안티패턴 (치명적