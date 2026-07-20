---
title: "Tungsten Engine"
date: "2024-03-23"
tags:
  - "studynote-bigdata"
weight: 58
---
## 핵심 인사이트 (3줄 요약)
- Tungsten은 Spark의 하드웨어 성능을 극한으로 끌어올리기 위한 실행 엔진 최적화 프로젝트로, 메모리 관리와 CPU 효율성에 집중한다.
- JVM 객체 오버헤드를 피하기 위해 자체적인 Off-heap 메모리 관리와 바이너리 데이터 포맷을 사용한다.
- Whole-stage Code Generation을 통해 런타임에 최적화된 바이트코드를 생성하여 가상 함수 호출 오버헤드를 제거한다.

### Ⅰ. 개요 (Context & Background)
- **정의**: Spark의 데이터 처리 속도를 개선하기 위해 하드웨어 아키텍처(CPU, RAM)를 최대한 활용하도록 설계된 엔진 계층이다.
- **배경**: Spark의 병목 현상이 네트워크/디스크 I/O에서 CPU와 메모리로 이동함에 따라, Java 객체의 높은 메모리 사용량과 GC(Garbage Collection) 부하를 해결하기 위해 등장했다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- <strong>Memory Management &amp; Binary Processing</strong>: 데이터를 Java 객체로 변환하지 않고 바이너리 형태로 메모리에 직접 저장한다. Unsafe Row 형식을 사용하여 직렬화 비용을 최소화한다.
- **Cache-aware Computation**: CPU 캐시(L1/L2/L3)의 지역성(Locality)을 고려한 알고리즘을 사용하여 캐시 미스를 줄인다.

```text
[ Tungsten CPU & Memory Optimization ]

   [ Standard JVM Approach ]          [ Tungsten Approach ]
   +-----------------------+        +--------------------------+
   |   Java Object (Rich)  |        | Binary Data (Row format) |
   | (Metadata, Padding)   | <----> | (Compact, No Metadata)   |
   +-----------------------+        +--------------------------+
               |                                |
       High GC Pressure                 Direct Memory Access
      High Cache Misses                 Cache-aware Algorithms
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 최적화 기법 | 주요 내용 | 기대 효과 |
| :--- | :--- | :--- |
| <strong>Off-heap Memory</strong> | JVM 힙 외부에서 메모리 직접 관리 | GC 부하 제거 및 대용량 메모리 효율성 |
| **Binary Row Format** | 데이터를 바이너리 직렬화 형태로 유지 | 메모리 사용량 감소 (객체 오버헤드 제거) |
| **Whole-stage CodeGen** | 여러 연산(Select, Filter 등)을 하나의 코드로 병합 | 가상 함수 호출 제거 및 루프 최적화 |
| **Vectorized Processing** | SIMD(Single Instruction Multiple Data) 활용 | CPU 연산 처리량(Throughput) 극대화 |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- <strong>메모리 설정</strong>: `spark.memory.offHeap.enabled=true` 설정을 통해 Tungsten의 Off-heap 기능을 활성화하여 GC 이슈가 잦은 대규모 워크로드를 안정화할 수 있다.
- <strong>데이터 구조 선택</strong>: RDD보다는 Tungsten의 혜택을 100% 받을 수 있는 DataFrame/Dataset API 사용을 강력히 권고한다. RDD는 Java 객체 오버헤드를 그대로 가지기 때문이다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- Tungsten은 Spark를 단순한 분산 프레임워크를 넘어 고성능 분석 엔진으로 진화시켰다. 최신 버전의 Spark에서는 벡터화된 실행(Vectorized Execution) 범위가 더욱 넓어지고 있으며, 이는 GPU 가속(RAPIDS) 및 차세대 하드웨어와의 융합으로 이어지는 토대가 되고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: Apache Spark
- **자식 개념**: Off-heap Memory, Whole-stage Code Generation
- **연관 개념**: Catalyst Optimizer, GC(Garbage Collection), SIMD

### 📈 관련 키워드 및 발전 흐름도

```text
[RDD]
    |
    v
[DataFrame]
    |
    v
[Tungsten 엔진]
    |
    v
[코드 생성 (Code Generation)]
    |
    v
[Photon 엔진]
```

Spark의 데이터 표현이 RDD에서 DataFrame으로 발전하고 Tungsten 최적화를 거쳐 하드웨어 가속 엔진으로 이어지는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
- 컴퓨터가 일을 할 때 메모장(Java 객체)을 예쁘게 꾸미느라 시간을 낭비하지 않고, 암호 같은 숫자(바이너리)로 바로바로 일하게 하는 거예요.
- 가방에 물건을 넣을 때 하나하나 포장하지 않고, 차곡차곡 빈틈없이 쌓아서 더 많이 넣고 빨리 꺼내는 기술과 비슷해요.
- 덕분에 아주 많은 데이터를 처리할 때도 컴퓨터가 지치지 않고 엄청 빠르게 일할 수 있답니다.
