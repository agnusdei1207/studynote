+++
title = "07. 가상 메모리 및 OS 통합 (Virtual Memory)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-computer-architecture"
kids_analogy = "내 책상은 작지만, 마술 상자(가상 메모리) 덕분에 세상의 모든 책을 다 올려놓고 공부하는 것처럼 느껴지는 마법이에요. 상자 안의 요정이 내가 지금 읽을 페이지만 진짜 책상 위로 슥 갖다 놓아준답니다!"
+++

# 07. 가상 메모리 및 OS 통합 (Virtual Memory)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 물리적 메모리의 한계를 극복하고 각 프로세스에 독립적인 거대 논리 주소 공간을 제공하는 주소 매핑 기술.
> 2. **가치**: 메모리 보호(Protection), 공유(Sharing), 그리고 효율적 할당을 통해 안정적인 멀티태스킹 환경 구축.
> 3. **융합**: MMU(Memory Management Unit) 하드웨어와 OS 커널의 페이징(Paging) 정책이 결합된 하이드웨어-소프트웨어 공조 시스템.

---

### Ⅰ. 개요 (Context & Background)
가상 메모리는 현대 컴퓨팅의 안정성을 지탱하는 근간이다. 실제 RAM 용량보다 큰 프로그램을 실행할 수 있게 할 뿐만 아니라, 프로세스 간 메모리 침범을 원천적으로 차단하여 시스템 보안을 강화한다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 메커니즘
- **Paging**: 고정 크기 블록(Page) 단위 매핑
- **Segmentation**: 논리적 단위(Code, Data) 매핑
- **TLB (Translation Lookaside Buffer)**: 주소 변환 고속 캐시
- **Page Fault**: 필요한 페이지가 메모리에 없을 때 발생하는 인터럽트

#### 2. 주소 변환 흐름 (ASCII)
```text
    [ Virtual to Physical Translation ]
    
    Virtual Address [ VPN | Offset ]
                      |       |
             +--------v-------+
             |   TLB (Cache)  | --- Hit ---> [ PPN | Offset ]
             +----------------+                  |
                    | Miss                       |
             +------v---------+                  |
             |   Page Table   | --- Valid ---> Physical Address
             +----------------+
                    | Invalid
             [   Page Fault   ] --> OS Disk I/O
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 페이징(Paging) vs 세그먼테이션(Segmentation)
| 항목 | 페이징 (Paging) | 세그먼테이션 (Segmentation) |
| :--- | :--- | :--- |
| **단위 크기** | 고정 (Fixed Size) | 가변 (Variable Size) |
| **파편화** | 내부 파편화 발생 | 외부 파편화 발생 |
| **관리** | 시스템 중심 (하드웨어 용이) | 사용자/언어 중심 (논리적) |
| **복잡도** | 단순함 | 복잡함 |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 **Thrashing(스래싱)** 현상은 시스템 성능을 마비시키는 주범이다. 기술사는 워킹 셋(Working Set) 모델을 이해하고, 애플리케이션의 메모리 참조 패턴을 최적화하여 Page Fault를 최소화하는 전략을 구사해야 한다.

---

### Ⅴ. 기대효과 및 결론
가상 메모리는 클라우드 가상화 및 컨테이너 기술의 기반이 된다. 향후 테라바이트급 메모리 시대를 맞아 거대 페이지(Huge Page) 지원 및 하드웨어 가속 주소 변환 기술이 더욱 고도화될 것이다.
