---
title: "Apache Spark, Ray"
date: "2026-05-06"
tags:
  - "studynote-ai"
weight: 182
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 아파치 스파크 (Apache Spark)와 레이 (Ray)는 한 대의 서버를 키우는 Scale-Up이 아니라, 여러 노드의 CPU (Central Processing Unit)·메모리·GPU (Graphics Processing Unit)를 묶어 하나의 AI 처리 플랫폼처럼 쓰게 만드는 Scale-Out 분산 컴퓨팅 프레임워크다.
> 2. **가치**: Spark는 테라바이트(TB)급 데이터 전처리와 SQL (Structured Query Language)·배치 집계에 강하고, Ray는 Python 기반 태스크·액터·분산 학습·하이퍼파라미터 탐색에 강해 현대 AI 파이프라인의 앞단과 뒷단을 나눠 맡기 좋다.
> 3. **판단 포인트**: 대규모 셔플(Shuffle)과 데이터 병렬이 중심이면 Spark, 상태를 가진 분산 작업과 GPU 스케줄링이 중심이면 Ray가 유리하며, 실제 현업에서는 둘 중 하나만 고집하기보다 하이브리드 구성이 가장 현실적이다.

---

## Ⅰ. 개요 및 필요성

AI (Artificial Intelligence) 시스템이 커질수록 병목은 모델 코드보다 먼저 데이터와 자원에서 발생한다. 수십 테라바이트의 로그를 조인하고 정제해야 하고, 수십 개 GPU를 동시에 묶어 모델을 학습해야 하며, 하이퍼파라미터 탐색이나 강화 학습 (RL, Reinforcement Learning)처럼 서로 다른 작업이 동시에 돌아가기도 한다. 이런 요구는 단일 서버의 메모리, 디스크 대역폭, GPU 개수만으로는 감당하기 어렵다.

이때 필요한 것이 분산 처리다. 핵심은 거대한 입력과 연산을 작은 단위로 나누어 여러 워커(Worker)가 병렬로 처리하게 하고, 중간 결과를 다시 모아 전체 답을 만드는 것이다. 하지만 AI 파이프라인은 모든 구간의 병렬성이 같지 않다. 원천 데이터 정제는 대용량 배치와 셔플이 중요하고, 분산 학습은 GPU 배치, 태스크 스케줄링, 상태 공유가 더 중요하다.

그래서 Spark와 Ray는 같은 "분산 컴퓨팅"이라는 이름 아래 있으면서도 맡는 일이 다르다. Spark는 큰 표와 로그를 빠르고 안정적으로 가공하는 데이터 엔진에 가깝고, Ray는 Python 함수와 상태 객체를 클러스터 전역에 배치하는 AI 런타임에 가깝다. 즉 둘을 구분하는 핵심은 브랜드가 아니라 <strong>주도적인 병렬성의 형태가 무엇인가</strong>다.

- **📢 섹션 요약 비유**: Spark와 Ray는 둘 다 큰 공사를 여러 사람이 나눠 하는 방식이지만, Spark는 흙을 대량으로 퍼 나르는 토목 장비에 가깝고 Ray는 여러 팀이 각자 역할을 나눠 동시에 움직이는 관제 시스템에 가깝다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Spark의 중심은 Driver, DAG (Directed Acyclic Graph) 스케줄러, Executor, DataFrame/RDD (Resilient Distributed Dataset), Shuffle이다. 큰 데이터를 파티션으로 나누고, 변환 연산을 Stage로 계획한 뒤, Executor들이 각 파티션을 처리한다. 특히 집계와 조인처럼 데이터 재분배가 필요한 구간에서 Shuffle 비용을 어떻게 제어하느냐가 성능의 핵심이다.

Ray의 중심은 Head Node, Global Control Store, Worker, Object Store, Remote Task, Actor다. 개발자는 Python 함수에 `@ray.remote`를 붙여 분산 태스크로 만들거나, 상태를 유지하는 Actor를 클러스터 여러 노드에 배치할 수 있다. Ray는 세밀한 태스크 병렬성과 상태 유지, GPU 자원 예약, 분산 서비스 구성에 강하다.

| 비교 축 | Apache Spark | Ray | 설계 의미 |
| :--- | :--- | :--- | :--- |
| 주된 병렬성 | 데이터 병렬, 배치 변환 | 태스크 병렬, 액터 병렬 | 워크로드 성격에 따라 선택 축이 갈림 |
| 핵심 실행 단위 | Partition, Stage, Task | Remote Function, Actor | Spark는 데이터 흐름, Ray는 실행 단위 표현이 강함 |
| 주요 강점 | ETL (Extract, Transform, Load), SQL, 대규모 집계 | 분산 학습, 튜닝, RL, Python 앱 | AI 파이프라인의 담당 구간이 다름 |
| 병목 포인트 | Shuffle, skew, serialization | object spilling, actor lifecycle, scheduling | 둘 다 네트워크와 직렬화 비용이 중요 |
| 대표 자원 | CPU, 메모리 중심 + 일부 GPU 연계 | CPU/GPU 세밀 스케줄링 | GPU 활용도는 Ray 쪽이 유연한 편 |

아래 그림은 실제 AI 파이프라인에서 Spark와 Ray가 어떻게 이어지는지 보여 준다.

```text
+----------------------------------------------------------------------+
| Hybrid AI pipeline: Spark + Ray                                     |
+----------------------------------------------------------------------+
| Raw logs / data lake                                                 |
|        |                                                             |
|        v                                                             |
| Spark cluster                                                        |
|   Driver -> DAG stages -> Executors -> shuffle / join / aggregate    |
|        |                                                             |
|        v                                                             |
| Feature table / parquet / feature store                              |
|        |                                                             |
|        v                                                             |
| Ray cluster                                                          |
|   Head node -> remote tasks / actors -> GPU workers                  |
|        |                                                             |
|        +- distributed training                                       |
|        +- hyperparameter tuning                                      |
|        +- reinforcement learning simulators                          |
|        |                                                             |
|        v                                                             |
| Model checkpoints / serving artifacts                                |
+----------------------------------------------------------------------+
```

핵심은 비용을 없애는 것이 아니라, 병목 위치를 바꾸는 데 있다. Spark는 디스크 기반 일괄 처리보다 메모리 기반 분산 처리로 이동하면서 속도를 높였지만, 큰 조인과 셔플에서 네트워크 병목이 생긴다. Ray는 Python 코드의 분산 표현력을 크게 높였지만, 객체 크기와 스케줄링 단위를 잘못 잡으면 오히려 오버헤드가 커진다. 따라서 두 프레임워크 모두 "노드를 많이 쓰면 무조건 빠르다"가 아니라, <strong>파티션·객체·통신 경계를 어떻게 자르느냐</strong>가 성패를 가른다.

- **📢 섹션 요약 비유**: Spark는 큰 곡물을 여러 창고에 나눠 담아 동시에 도정하는 방앗간 시스템이고, Ray는 여러 작업자와 로봇에게 역할을 배정해 동시에 움직이게 하는 작업 지휘실과 같다.

---

## Ⅲ. 비교 및 연결

Spark와 Ray는 경쟁 제품이면서도 동시에 보완 관계다. Spark는 DataFrame과 SQL 생태계가 강해 대용량 정제·집계·피처 엔지니어링에 유리하고, Ray는 Python 생태계와 잘 맞아 분산 학습, 서빙, 튜닝, 시뮬레이션 워크로드에 유리하다. 그래서 둘을 같은 기준으로 비교하면 안 되고, "어떤 종류의 병렬성을 많이 쓰는가"로 봐야 한다.

| 항목 | Spark | Ray |
| :--- | :--- | :--- |
| 잘하는 일 | 대규모 ETL (Extract, Transform, Load), SQL, 배치 집계, 데이터 레이크 처리 | 분산 학습, Ray Train, Ray Tune, RL, 상태 있는 서비스 |
| 약한 구간 | 장수명 상태 객체, 세밀한 GPU 태스크 제어 | 대규모 SQL성 조인과 전통적 배치 ETL |
| 연결 생태계 | Hive, Delta Lake, Iceberg, Spark SQL | PyTorch, TensorFlow, XGBoost, Serve |
| 대표 실패 패턴 | Data Skew, 과도한 shuffle | 거대한 객체 전송, actor 남용 |
| 일반적 조합 | 전처리 엔진 | 학습·튜닝·서빙 엔진 |

또한 이 둘은 Airflow 같은 오케스트레이터와도 구분해야 한다. Airflow는 순서와 재시도를 관리하는 제어 평면이고, Spark와 Ray는 실제 계산을 수행하는 데이터 평면이다. 즉 Airflow가 "언제 돌릴지"를 정한다면, Spark와 Ray는 "무엇을 어떻게 병렬 계산할지"를 담당한다.

프레임워크 내부 철학도 다르다. Spark는 DAG 최적화와 배치 처리에 강한 반면, Ray는 액터 모델 (Actor Model)과 원격 함수 호출로 더 유연한 분산 애플리케이션 구조를 제공한다. 그래서 대규모 표 처리와 반복 집계는 Spark가 더 예측 가능하고, 상태를 가진 병렬 워커와 GPU 자원 배치는 Ray가 더 자연스럽다.

- **📢 섹션 요약 비유**: Spark가 거대한 원자재를 규격품으로 가공하는 생산 라인이라면, Ray는 가공된 부품을 들고 여러 전문 작업자가 동시에 조립하는 공장 관리 시스템에 가깝다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서는 먼저 병목을 수치화해야 한다. 수백 기가바이트 이상 데이터를 조인·집계하는 데 시간이 걸리는가, 아니면 이미 정제된 데이터를 여러 GPU에 나눠 학습시키는 데 시간이 걸리는가에 따라 선택이 갈린다. 데이터 준비가 병목이면 Spark가 먼저이고, 모델 실험과 분산 실행이 병목이면 Ray가 먼저다.

| 실무 상황 | 권장 방향 | 이유 |
| :--- | :--- | :--- |
| 로그·클릭스트림·정형 데이터 ETL | Spark 우선 | 대용량 셔플과 SQL 최적화가 강함 |
| 분산 딥러닝 학습·튜닝 | Ray 우선 | Python 친화적이고 GPU 스케줄링이 유연함 |
| RL 시뮬레이터 다수 실행 | Ray 우선 | 상태를 가진 Actor 모델이 자연스러움 |
| 피처 생성 후 모델 학습까지 일관 파이프라인 | Spark + Ray 조합 | 전처리와 학습의 병렬성이 다름 |

### 실무 체크리스트

1. Spark에서는 파티션 크기, Broadcast Join, Data Skew, Shuffle 횟수를 먼저 점검했는가?
2. Ray에서는 객체 크기, Actor 수명주기, GPU 배치(Placement Group), Object Store spilling을 점검했는가?
3. 데이터 이동 경로가 명확한가? 전처리 결과를 파일, 테이블, Feature Store 중 어디로 넘길지 정했는가?
4. 분산 실패 복구 전략이 있는가? 체크포인트, 재시도, 멱등성 있는 작업 단위를 설계했는가?
5. Kubernetes나 YARN (Yet Another Resource Negotiator) 같은 자원 관리자와 비용 통제를 함께 고려하고 있는가?

### 자주 발생하는 안티패턴

- 로컬 Pandas 사고방식을 그대로 유지한 채 Spark에서 행 단위 UDF (User Defined Function)를 남발하는 경우
- 대규모 조인이 중심인 작업을 Ray만으로 처리해 불필요한 구현 복잡도를 키우는 경우
- 작은 태스크를 지나치게 잘게 쪼개 스케줄링 오버헤드가 계산 비용보다 커지는 경우
- 모델 학습 코드와 데이터 전처리 코드를 한 프레임워크에 억지로 몰아넣는 경우

학습 정리에서는 <strong>"Spark는 데이터 병렬 ETL과 대규모 셔플 최적화에 강하고, Ray는 Python 기반 분산 태스크·액터·GPU 워크로드에 강하므로, AI 인프라는 병렬성의 종류에 따라 역할을 분리해 설계해야 한다"</strong>고 정리하면 좋다.

- **📢 섹션 요약 비유**: 좋은 설계자는 모든 장비를 하나로 합치지 않고, 토목 장비는 흙을 옮기게 하고 크레인은 조립을 맡기듯 프레임워크를 역할에 맞게 배치한다.

---

## Ⅴ. 기대효과 및 결론

Spark와 Ray를 적절히 조합하면 단일 서버 한계를 넘어서는 AI 인프라를 만들 수 있다. 대용량 원천 데이터를 빠르게 정제하고, 여러 GPU와 워커를 묶어 학습·탐색·서빙을 병렬화함으로써 데이터 준비 시간과 모델 실험 시간을 동시에 줄일 수 있다. 특히 데이터 규모와 실험 횟수가 함께 커지는 조직일수록 이 효과가 크다.

다만 분산 시스템은 마법이 아니다. 노드가 늘수록 네트워크 이동, 직렬화, 장애 복구, 관측성, 비용 통제가 새 문제로 따라온다. 그래서 분산 처리의 핵심 역량은 프레임워크 이름을 아는 것이 아니라, 병렬화가 이득이 되는 경계와 오히려 손해가 되는 경계를 구분하는 데 있다.

결론적으로 기억할 문장은 단순하다. <strong>Spark는 큰 데이터를 잘 움직이게 하고, Ray는 큰 AI 작업을 잘 움직이게 한다.</strong> 둘을 대체 관계로만 보지 말고, 데이터 준비와 모델 실행이라는 서로 다른 병렬성 축으로 이해하는 것이 실무적이다.

- **📢 섹션 요약 비유**: Spark와 Ray는 같은 공장을 움직이는 두 종류의 엔진으로, 하나는 원자재 흐름을 빠르게 만들고 다른 하나는 조립과 실험을 빠르게 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| ETL (Extract, Transform, Load) | Spark가 가장 강점을 보이는 전통적 대용량 데이터 처리 영역이다. |
| Shuffle | Spark 성능을 좌우하는 핵심 병목 구간으로 파티션 전략과 직결된다. |
| Actor Model | Ray가 상태 있는 분산 워커를 표현하는 핵심 개념이다. |
| Distributed Training | Ray가 PyTorch, TensorFlow와 결합해 수행하는 대표 AI 워크로드다. |
| Feature Store | Spark 전처리 결과가 Ray 학습 단계로 넘어가는 중간 자산이 된다. |
| Airflow | Spark와 Ray를 직접 대체하지 않고, 둘의 실행 순서를 조율하는 상위 오케스트레이터다. |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 서버 한계(CPU / RAM / GPU)
    |
    v
Scale-Out 클러스터 구성
    |
    +- 대용량 정형 데이터 -> Spark ETL / SQL / shuffle
    +- 피처 생성 -> parquet / feature store
    +- 분산 실험 / 학습 -> Ray task / actor / GPU scheduling
    |
    v
하이브리드 AI 파이프라인
    |
    v
대규모 전처리 + 분산 학습 + 튜닝 + 서빙
```

이 흐름은 분산 AI 인프라가 단순히 "컴퓨터를 많이 쓰는 것"이 아니라, 데이터 병렬과 실행 병렬을 서로 다른 엔진으로 나누어 최적화하는 과정임을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Spark는 아주 큰 퍼즐 조각을 여러 친구에게 나눠 주고, 같은 색끼리 빨리 모으게 하는 반장님이에요.
2. Ray는 친구마다 다른 역할을 주고, 어떤 친구는 그림 그리고 어떤 친구는 계산하게 하면서 같이 놀게 하는 감독님이에요.
3. 그래서 큰 숙제는 Spark가 정리하고, 어려운 실험은 Ray가 지휘하면 더 빨리 끝낼 수 있어요.
