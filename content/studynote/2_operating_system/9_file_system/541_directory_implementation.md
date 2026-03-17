+++
title = "541. 디렉터리 구현 - 효율적인 탐색 기법"
date = "2026-03-14"
weight = 541
+++

# # [541. 디렉터리 구현 - 효율적인 탐색 기법]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 디렉터리는 파일 시스템의 **네임 서버(Name Server)**로서, 추상적인 파일명(File Name)을 물리적 블록 매핑 정보인 **inode (Index Node)** 또는 **FCB (File Control Block)**로 변환하는 핵심 매핑 계층이다.
> 2. **가치**: 단순 선형 리스트(Linear List)의 $O(N)$ 복잡도를 **Hash Table**이나 **B-Tree (Balanced Tree)** 구조로 최적화하여 탐색 지연(Latency)을 획기적으로 줄이고, 대용량 파일 시스템에서의 **Seek Time**을 최소화한다.
> 3. **융합**: OS의 파일 시스템 구조와 DBMS의 인덱싱 기술이 결합된 분야로, **NVMe SSD**의 등장과 함께 **Dentry Cache (Directory Entry Cache)** 전략이 스토리지 성능을 좌우하는 핵심 변수가 되었다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**디렉터리(Directory)**는 사용자가 인식하는 논리적 파일명과 시스템이 관리하는 물리적 데이터 블록 사이의 인터페이스를 담당하는 특수한 파일 형태다. 파일 시스템의 관점에서 디렉터리는 '파일에 대한 파일'이며, 내부에는 파일명과 해당 파일의 메타데이터 위치(inode 번호 혹은 FCB 주소)가 저장된다. 초기 UNIX나 MS-DOS 시스템은 단순한 연결 리스트(Linked List)나 배열(Array) 기반의 선형 리스트를 사용하여 구현의 단순함을 추구했다. 그러나 이는 파일 수가 증가함에 따라 탐색 시간이 선형적으로 비례하여 증가하는 치명적인 단점이 있었다.

현대의 엔터프라이즈 환경과 클라우드 스토리지에서는 단일 디렉터리에 수백만 개의 파일이 존재하는 것이 예사다. 이러한 환경에서 $O(N)$의 시간 복잡도를 가지는 선형 탐색은 디스크의 회전 지연(Rotational Latency)과 탐색 시간(Seek Time)을 중첩시켜 시스템 전체의 병목 구간(Bottleneck)을 유발한다. 따라서 효율적인 디렉터리 구현을 위해 **해싱(Hashing)** 기법을 통한 직접 접근 방식과, 정렬된 순서를 유지하며 범위 탐색에 유리한 **B-Tree (Balanced Tree)** 혹은 **B+Tree** 구조를 도입하여 탐색 복잡도를 $O(1)$ 또는 $O(\log N)$ 수준으로 최적화하는 것이 필수적이다.

#### 💡 비유
파일 시스템의 디렉터리는 거대한 도서관의 **'카드 목록(Catalog)'**이자 **'분류 시스템'**과 같다. 수만 권의 책(파일)이 꽂혀 있는 창고에서, 독자가 원하는 책 제목을 검색하면 도서관원(시스템)이 목록을 통해 해당 책이 꽂힌 정확한 납(Bookshelf, inode) 위치를 즉시 알려주는 역할을 수행한다.

#### 📢 섹션 요약 비유
선형 리스트 방식은 **"정리되지 않은 책상 위에서 서류 뭉치를 위에서부터 하나하나 펴보며 찾는 것"**과 같아서 서류가 조금만 많아져도 찾는 시간이 선형으로 늘어나는 반면, 효율적인 탐색 기법은 **"모든 서류를 알파벳 순으로 정리된 자동화 창고에 보관하여, 컴퓨터 입력을 통해 순식간에 위치를 파악하는 것"**과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

효율적인 디렉터리 구현을 위해서는 데이터의 저장 방식(Storage Layout)과 탐색 알고리즘(Search Algorithm)의 결합이 필수적이다. 대표적으로 **Hash Table**과 **B-Tree** 기반의 아키텍처가 가장 널리 사용되며, 최근에는 메모리 자원을 활용한 **Cache** 전략이 결합된다.

#### 1. 구성 요소 상세 분석

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 주요 프로토콜/구조 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Linear List** | 기본 엔트리 저장 | 이름과 inode 포인터 쌍을 배열에 순차 저장. 삽입 시 정렬 여부에 따라 탐색 속도 변화. | Array / Linked List | 쌓여 있는 신문 더미 |
| **Hash Table** | 상수 시간 탐색 | 파일명을 해시 함수 $h(key)$에 통과시켜 버킷(Bucket) 인덱스 계산. 충돌 시 체이닝(Chaining) 사용. | Ext3 HTree, ReiserFS | 분실물 보관소 번호표 |
| **B-Tree / B+Tree** | 정렬된 범위 탐색 | 다중 경로 균형 트리. 노드 분할(Split)/합병(Merge)으로 높이 유지. 리프 노드에 데이터 저장. | NTFS, HFS+, XFS | 도서관 분류법 |
| **Dentry Cache** | 메모리 상주 캐시 | 최근 사용한 디렉터리 엔트리를 RAM에 캐싱하여 디스크 I/O 회피. | **SLAB Allocator**, **LRU** | 자주 쓰는 전화번호 단축키 |
| **Free Bitmap** | 공간 관리 | 디렉터리 내 빈 엔트리 슬롯을 관리하여 할당 속도 향상. 메타데이터 블록 내 위치 비트맵 활용. | Bitmap Allocator | 주차장 빈자리 표시등 |

#### 2. ASCII 구조 다이어그램: 해시 테이블 vs B-트리

아래는 두 가지 핵심 알고리즘이 디스크 블록에 데이터를 저장하는 방식의 차이를 도식화한 것이다. 해시는 계산을 통해 위치를 찾고, B-트리는 경로를 통해 위치를 찾는다.

```text
[디스크 블록 상 디렉터리 구조 비교]

1. Linear List (Single Linked Block View)  - O(N) Search
+-----------------------+
| .      (Self)  | i_1  |  --> 현재 디렉터리 inode
| ..     (Parent)| i_2  |  --> 부모 디렉터리 inode
| foo.exe        | i_55 |
| bar.txt        | i_12 |
| data.bin       | i_99 |
| ... (Huge file list) |
| target.zip     | i_77 |  <-- 찾으려는 파일 (처음부터 순차 접근)
+-----------------------+

2. Hash Table Method (Ext3/4 HTree - Indexed)  - O(1) ~ O(log N)
+-----------------------------------------+
| Directory Block Header                  |
+-----------------------------------------+
| Hash Table Area (Root/Leaf Blocks)      |
| [h(a)]: Blk_1024 | h(b): Blk_2048       |  <-- 파일명 해싱 -> 블록 오프셋
| [h(t)]: Blk_3072 | ...                  |
+-----------------------------------------+
| Data Area (Collision Resolution Chain)  |
| [foo.txt] [i_55] -> [bar.log] [i_99]    |  <-- Chaining (Same Hash)
+-----------------------------------------+

3. B+Tree Method (NTFS / XFS)  - O(log N) Search
            [ Root Node (Index) ]
           /      |       \
    [Internal]  [Internal] [Internal]
    /     |      \          \
[A-K]   [L-R]     [S-Z]      ...  (Delimiter Keys)
  |      |         |
[Leaf]  [Leaf]    [Leaf]     <-- Leaf Nodes (Sorted Entries)
 |      |         |
i_55   i_102      i_201      <-- Pointers to inodes
```

#### 3. 심층 동작 원리

1.  **경로 이름 해석(Pathname Resolution)**: 사용자가 `/usr/bin/bash`를 입력하면, **VFS (Virtual File System)**는 루트(`/`) 디렉터리의 inode를 로드한다.
2.  **단계별 탐색(Step-by-step Lookup)**: 루트 디렉터리의 데이터 블록을 읽어 `usr` 엔트리를 탐색한다. 이때 `usr`의 inode 번호를 획득하고, 해당 디스크 블록으로 이동(Seek)한다.
3.  **인덱스 활용(Indexing Strategy)**:
    *   **Hash**: `usr` 디렉터리 블록 내에서 `hash("bin")` 함수를 실행하여 버킷 위치를 계산하고, 즉시 해당 엔트리가 있는 블록으로 접근한다.
    *   **B-Tree**: `bin` 문자열을 트리의 노드들(Key)과 비교(Compare)하며 리프 노드(Leaf Node)까지 내려간다.
4.  **캐시 확인(Dentry Lookup)**: 모든 단계에서 먼저 커널의 **dcache (Directory Entry Cache)**를 확인한다. 캐시에 있다면(Hit) 디스크 I/O 없이 메모리에서 즉시 포인터를 반환하여 성능을 극대화한다.

#### 4. 핵심 알고리즘 (의사코드)

```c
// 디렉터리 엔트리 검색 함수 (Hash Table 예시)
struct inode* lookup_directory(struct dir_entry *dir, const char *name) {
    unsigned long hash_val;
    struct dentry *cached_dentry;
    struct entry *curr;

    // 1. 성능 핵심: 메모리 캐시 확인 (dcache)
    cached_dentry = dentry_cache_lookup(name);
    if (cached_dentry) return cached_dentry->d_inode; // Cache Hit

    // 2. 디스크 I/O: 해시 함수 계산
    hash_val = hash_function(name);
    int bucket_idx = hash_val % TABLE_SIZE;

    // 3. 버킷 탐색 (충돌 처리: Chaining)
    curr = dir->table[bucket_idx];
    while (curr != NULL) {
        if (strcmp(curr->filename, name) == 0) {
            // 4. 탐색 성공: 캐시 업데이트 후 반환
            update_dentry_cache(name, curr->inode_ptr);
            return curr->inode_ptr; // FCB/inode 포인터 반환
        }
        curr = curr->next; // 체인의 다음 노드로 이동
    }
    return NULL; // 파일 없음 (ENOENT)
}
```

#### 📢 섹션 요약 비유
해시 테이블 방식은 **"도서관에 자동 사물함을 설치하고, 책 제목을 입력하면 해당 사물함 번호가 딱! 하고 나오는 시스템"**과 같아서 굉장히 빠르지만, 해시 충돌이 발생하면 줄을 서야 한다는 단점이 있습니다. B-트리 방식은 **"도서관을 층별로 나누고, 다시 구역별로 나누어, 'ㄱ' 구역 -> 'ㄴ' 구역 순으로 좁혀가며 찾는 체계적인 분류법"**과 같아서 책이 아주 많아도 순서대로 빠짐없이 찾을 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

#### 1. 심층 기술 비교 (정량적 지표)

| 비교 항목 | 선형 리스트 (Linear List) | 해시 테이블 (Hash Table) | B-트리 (B-Tree / B+Tree) |
|:---|:---|:---|:---|
| **탐색 복잡도** | $O(N)$ | $O(1)$ (평균) | $O(\log N)$ |
| **삽입/삭제 비용** | $O(1)$ (연결리스트 미정렬 시) | $O(1)$ (리해싱 제외) | $O(\log N)$ (노드 분할/합병 포함) |
| **공간 효율성** | 높음 (포인터 오버헤드 최소) | 중간 (빈 버킷 발생 가능) | 낮음 (내부 노드 포인터 오버헤드) |
| **순차 접근** | 매우 용이함 (연속 스캔) | 불가능에 가까움 (버킷 분산) | 매우 용이함 (리프 노드 연결) |
| **범위 검색** | $O(N)$ (전체 스캔 필요) | 지원 안 함 ($O(N)$) | $O(\log N + K)$ (매우 우수) |
| **구현 난이도** | 낮음 | 중간 (충돌 처리, 리해싱 로직) | 높음 (균형 유지 로직 복잡) |
| **대표 OS** | FAT (MS-DOS) | Ext3 (HTree), ReiserFS | NTFS, HFS+, XFS, Ext4 |

#### 2. ASCII 다이어그램: 성능 및 저장소 효율성 비교

아래 다이어그램은 파일 수가 증가함에 따른 탐색 시간(Sec)의 추이와 저장 공간 사용량을 개념적으로 도시한 것이다.

```text
[Performance & Storage Efficiency Graph]

^
| Search Time (Latency)
|
|        _________ Linear List (O(N)) -> explodes
|       /
|      /
|     /   
|    /     
|   /       ______ Hash Table (O(1)) -> Flat
|  /       /
| /       /
|/_______/________________________ B-Tree (O(log N)) -> Log Curve
|
+----------------------------------------------------> # of Files (N)

^
| Storage Usage (Overhead)
|
|             _________ B-Tree (Pointers in Nodes) -> High Overhead
|            /
|           /
|          /
|         /
|        /   ______ Hash Table (Empty Buckets) -> Medium
|       /
|      /
|_____/___________________________________________ Linear List -> Minimal
|
+----------------------------------------------------> # of Files (N)
```

#### 3. 과목 융합 관점 분석

*   **운영체제(OS)와 데이터베이스(DB)의 융합**:
    디렉터리 구조는 DBMS의 **인덱싱(Indexing)** 기술과 그 맥락을 같이한다. 특히 B-Tree 구조는 디스크 블록 접근을 최소화하기 위해 고안된 것으로, OS의 파일 시스템(NTFS, Ext4)과 DBMS의 저장소 엔진(InnoDB, Oracle) 양쪽에서 핵심 자료구조로 사용된다. 다만, 파일 시스템의 키(Key)가 '파일명(가변 길이 문자열)'인 점이 DBMS의 숫자형 기본 키(PK)와는 구별되는 특징이며, 이로 인해 파일 시스템은 가변 길이 키 비교에 최적화된 문자열 비교 루틴을 사용한다.

*   **네트워크와의 시너지 (Distributed File System)**:
    분산 파일 시스템(예: HDFS, Lustre) 환경에서는 디렉터리 메타데이터를 별도의 **MDS (Metadata Server)**에 분산 저장한다