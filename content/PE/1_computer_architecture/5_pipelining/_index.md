+++
title = "05. 제어 유닛 및 파이프라이닝 (Pipelining)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-computer-architecture"
kids_analogy = "공장에서 장난감을 만들 때, 한 사람이 처음부터 끝까지 다 만드는 게 아니라 여러 사람이 줄을 서서 각자 맡은 일만 빠르게 처리하는 '자동화 라인'이에요. 쉴 새 없이 움직여서 아주 많은 장난감을 빨리 만들어낼 수 있죠!"
+++

# 05. 제어 유닛 및 파이프라이닝 (Pipelining)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 명령어 실행을 여러 단계(IF-ID-EX-MEM-WB)로 세분화하고 각 단계를 병렬로 중첩 실행하여 처리량(Throughput)을 극대화하는 기법.
> 2. **가치**: 클럭 사이클 시간을 단축하고 매 클럭마다 명령어 하나가 완료되게 함으로써 이론적 최대 속도 도달.
> 3. **융합**: 파이프라인 해저드(Structural, Data, Control) 해결을 위한 분기 예측(Branch Prediction) 및 포워딩(Forwarding) 기술의 정수.

---

### Ⅰ. 개요 (Context & Background)
파이프라이닝은 컴퓨터 성능 향상의 가장 강력한 도구 중 하나다. 세탁소에서 빨래가 끝나기 전에 다음 옷을 세탁기에 넣는 것처럼, 이전 명령어가 끝나기 전에 다음 명령어를 시작하는 '시간적 병렬성'을 활용한다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 5단계 파이프라인 스테이지
- **IF (Instruction Fetch)**: 메모리에서 명령어 인출
- **ID (Instruction Decode)**: 명령어 해석 및 레지스터 읽기
- **EX (Execute)**: 연산 수행 및 주소 계산
- **MEM (Memory Access)**: 데이터 메모리 접근
- **WB (Write Back)**: 결과를 레지스터에 기록

#### 2. 파이프라인 해저드 (Hazards)
- **Structural**: 하드웨어 자원이 부족하여 발생하는 충돌
- **Data**: 이전 명령어의 결과가 준비되지 않아 발생하는 대기 (Data Dependency)
- **Control**: 분기 명령어 때문에 다음 명령어 주소를 모르는 상황

#### 3. 파이프라인 실행도 (ASCII)
```text
    Time ->    T1   T2   T3   T4   T5   T6   T7
    Inst 1:    IF   ID   EX   ME   WB
    Inst 2:         IF   ID   EX   ME   WB
    Inst 3:              IF   ID   EX   ME   WB
    Inst 4:                   IF   ID   EX   ME   WB
    
    [결과] T5부터 매 클럭마다 명령어 하나씩 WB 완료!
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 파이프라인 해저드 해결책
| 해저드 유형 | 해결 전략 | 상세 기술 |
| :--- | :--- | :--- |
| **데이터 해저드** | Forwarding / Bypassing | ALU 결과를 메모리에 쓰기 전 즉시 다음 명령어로 전달 |
| **제어 해저드** | Branch Prediction | 분기 여부를 미리 짐작하여 다음 명령어 인출 |
| **구조적 해저드** | Resource Duplication | 명령용 메모리와 데이터용 메모리 분리 (하버드 아키텍처) |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 파이프라인이 깊어질수록(Deep Pipelining) 클럭은 빨라지지만, 분기 예측 실패 시 발생하는 **Penalty(Flushing)**가 커진다. 기술사는 워크로드의 특성을 고려하여 적절한 파이프라인 깊이를 결정하고, 슈퍼스칼라(Superscalar)와 같은 다중 이슈 기술 도입 여부를 판단해야 한다.

---

### Ⅴ. 기대효과 및 결론
파이프라이닝은 현대 비순차 실행(Out-of-Order Execution) 아키텍처의 근간이다. 향후 투기적 실행(Speculative Execution)의 보안 취약점(Spectre 등)을 하드웨어 수준에서 어떻게 극복할지가 중요한 연구 과제다.
