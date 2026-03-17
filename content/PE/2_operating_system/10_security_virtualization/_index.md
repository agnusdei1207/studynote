+++
title = "10. 보안 및 가상화 (Security & Virtualization)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-operating-system"
kids_analogy = "하나의 컴퓨터 안에 여러 개의 '가짜 컴퓨터'를 만드는 마법이에요. 서로 다른 가짜 컴퓨터끼리는 절대로 안을 들여다볼 수 없어서, 한쪽이 감기에 걸려도 다른 쪽은 건강하답니다!"
+++

# 10. 보안 및 가상화 (Security & Virtualization)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 하이브리드 클라우드 환경을 위한 자원의 논리적 격리(Isolation) 및 하드웨어 자원의 추상화 계층 구축.
> 2. **가치**: 서버 통합(Consolidation)을 통한 ROI 향상 및 샌드박싱(Sandboxing)을 통한 보안성 극대화.
> 3. **융합**: 하이퍼바이저(Hypervisor)와 컨테이너(Container) 기술의 조화를 통한 마이크로서비스 아키텍처(MSA) 실현.

---

### Ⅰ. 개요 (Context & Background)
가상화는 현대 IT 인프라의 마법이다. 물리적인 서버 한 대를 수십 대의 서버처럼 쓰게 함으로써 자원의 낭비를 막고, 장애 발생 시 즉각적인 복제와 이전을 가능하게 한다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 기술 유형
- **Type 1 Hypervisor**: 하드웨어 바로 위에서 동작 (ESXi, Xen)
- **Type 2 Hypervisor**: 일반 OS 위에서 동작 (VirtualBox, VMware)
- **Container**: OS 커널을 공유하며 프로세스 단위 격리 (Docker)
- **VMM (Virtual Machine Monitor)**: 가상 머신을 제어하는 핵심 소프트웨어

#### 2. 가상화 계층 구조 비교 (ASCII)
```text
    [ VM vs Container ]
    
       (Virtual Machine)              (Container)
    +-------------------+          +-------------------+
    |   App A | App B   |          |   App A | App B   |
    +---------+---------+          +---------+---------+
    |   Guest OS (Full) |          |  Container Engine |
    +-------------------+          +-------------------+
    |    Hypervisor     |          |   Host OS Kernel  |
    +-------------------+          +-------------------+
    |    Physical HW    |          |    Physical HW    |
    +-------------------+          +-------------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 전가상화(Full) vs 반가상화(Para)
| 항목 | 전가상화 (Full-Virtualization) | 반가상화 (Para-Virtualization) |
| :--- | :--- | :--- |
| **수정 여부** | Guest OS 수정 불필요 | Guest OS 수정 필요 (Hypercall) |
| **성능** | 상대적으로 낮음 (바이너리 변조) | 높음 (하드웨어 직접 요청) |
| **호환성** | 매우 높음 (모든 OS 가능) | 낮음 (특정 커널만 가능) |
| **대표 사례** | VMware, KVM (초기) | Xen, Hyper-V |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 **Container Escape**와 같은 보안 사고는 치명적이다. 기술사는 커널을 공유하는 컨테이너의 보안 한계를 명확히 인지하고, 핵심 워크로드에 대해서는 하이퍼바이저 기반의 강한 격리(gVisor, Kata Container)를 고려해야 한다.

---

### Ⅴ. 기대효과 및 결론
가상화는 서버리스와 엣지 컴퓨팅의 기반 기술로 계속 진화하고 있다. 향후 하드웨어 수준에서 가상화를 지원하는 VT-x, AMD-V 기술과 결합하여 '오버헤드 제로'의 가상화 환경이 구축될 것이다.
