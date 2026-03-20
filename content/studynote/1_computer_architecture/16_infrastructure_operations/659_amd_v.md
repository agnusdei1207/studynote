---
title: "AMD-V (AMD Virtualization)"
date: 2026-03-20
weight: 659
description: "인텔의 VT-x에 맞서 AMD가 독자적으로 개발한 하드웨어 보조 가상화 기술로, 서버 및 데스크톱 시장에서 고성능 가상 머신 구동을 가능하게 하는 핵심 아키텍처"
taxonomy:
    tags: ["Computer Architecture", "Virtualization", "AMD", "AMD-V", "CPU"]
---

> **핵심 인사이트**
> 1. **AMD-V (코드명 Pacifica)**는 인텔의 VT-x와 똑같은 목적(소프트웨어 가상화 오버헤드 제거)을 달성하기 위해 AMD가 자사 CPU에 탑재한 **하드웨어 가상화 확장 명령어 세트**다.
> 2. 내부적으로 부르는 용어(VMRUN, VMCB 등)만 다를 뿐, 인텔처럼 호스트(하이퍼바이저)와 게스트(VM)의 실행 권한을 물리적으로 분리하여 네이티브 속도로 VM을 돌리게 해준다.
> 3. 특히 메모리 가상화 기술인 **NPT(Nested Page Table, 혹은 RVI)**를 인텔보다 먼저 세계 최초로 상용화하여, 초창기 가상화 전쟁에서 기술적 우위를 점했던 역사적 의의가 있다.

<br>

## Ⅰ. 가상화 전쟁의 서막

2005년, 클라우드라는 단어가 막 태동할 무렵 인텔이 'VT-x'를 발표하며 가상화 시장의 주도권을 잡으려 했습니다. AMD는 1년 뒤인 2006년, 이에 대항하는 **AMD-V** 기술을 발표합니다.

인텔과 AMD의 기술은 철학이 거의 똑같습니다. "CPU 명령어의 실행 모드를 나누어, 가상 머신이 하드웨어와 직접 대화(Native Execution)하게 만들되, 위험한 행동을 하면 하드웨어가 낚아채자(Trap)!"는 것입니다.

### 인텔 vs AMD 용어 비교

| 기능 | Intel VT-x | AMD-V |
| :--- | :--- | :--- |
| **명령어 집합** | VMX (Virtual Machine Extensions) | SVM (Secure Virtual Machine) |
| **상태 저장 장부**| VMCS (Virtual-Machine Control Structure)| VMCB (Virtual Machine Control Block) |
| **VM 시작 명령어**| VMLAUNCH / VMRESUME | VMRUN |
| **모드 분리** | VMX Root / Non-Root Mode | Host Mode / Guest Mode |

> 📢 **섹션 요약 비유**: 펩시와 코카콜라입니다. 상표명(명령어 이름)만 다를 뿐, 둘 다 콜라(하드웨어 보조 가상화)라는 완벽히 동일한 결과물을 내놓습니다. 현대의 KVM이나 VMware 하이퍼바이저 소스코드를 보면 `if (CPU == Intel) { VMLAUNCH } else if (CPU == AMD) { VMRUN }` 처럼 분기 처리되어 있습니다.

<br>

## Ⅱ. AMD-V의 선제 공격: RVI (Rapid Virtualization Indexing)

초창기 가상화 기술(VT-x, AMD-V)은 CPU '명령어' 가상화 오버헤드는 잡았지만, **'메모리 주소 변환'** 오버헤드는 해결하지 못했습니다. (이건 뒤에 확장 페이지 테이블 챕터에서 자세히 다룹니다.)

그런데 AMD는 2007년 바르셀로나(Barcelona) 아키텍처를 출시하면서 인텔의 뒤통수를 강하게 때렸습니다. 인텔보다 한발 앞서 하드웨어 메모리 가상화 기술인 **RVI (Rapid Virtualization Indexing)**를 AMD-V에 얹어서 출시한 것입니다. 

이 RVI(이후 NPT로 불림) 기술 덕분에 당시 AMD 서버는 가상 머신의 메모리 접근 속도에서 인텔을 압살하며 클라우드 초기 시장에서 강력한 존재감을 뽐냈습니다.

> 📢 **섹션 요약 비유**: 인텔이 통역사 없는 '외국어 직통 마이크(명령어 가상화)'를 먼저 발명했다면, AMD는 1년 늦게 마이크를 만들었지만 덤으로 '자동 외국어 문서 번역기(메모리 가상화)'까지 최초로 달고 나와서 시장의 판도를 뒤흔든 격입니다.

<br>

## Ⅲ. 현대의 AMD-V와 에픽(EPYC)의 부상

한동안 인텔 제온(Xeon)에 밀려 암흑기를 겪던 AMD는, Zen 아키텍처 기반의 **EPYC(에픽) 서버 프로세서**를 내놓으며 화려하게 부활했습니다.

최신 EPYC 프로세서는 AMD-V 기술을 밑바탕으로 깔고, 코어 개수를 무지막지하게 늘린 칩렛 아키텍처와 결합하여 "1대의 서버에 수백 개의 가상 머신(VM)을 성능 저하 없이 가장 싸게 올릴 수 있는 최고의 깡패 가성비 칩"으로 등극했습니다. 현재 AWS, Google Cloud 등 전 세계 클라우드 인프라의 거대한 축을 담당하고 있습니다.
