---
title: "Data Serialization Avro Protobuf Thrift"
date: "2026-04-29"
tags:
  - "studynote-bigdata"
weight: 49
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Avro, Protocol Buffers(Protobuf), Apache Thrift는 구조화된 데이터를 언어·플랫폼 독립적인 바이너리 형식으로 직렬화(Serialization)하는 프레임워크로, JSON/XML 대비 크기·속도에서 탁월한 효율을 제공한다.
> 2. **가치**: 빅데이터 파이프라인에서 직렬화 형식 선택은 네트워크 비용·처리 지연·스토리지 비용에 직접 영향을 준다. Kafka 메시지 직렬화에 JSON 대신 Avro를 사용하면 메시지 크기가 50~70% 줄고 역직렬화 속도가 10배 이상 빨라질 수 있다.
> 3. **판단 포인트**: 세 가지 선택 기준 — ①스키마 진화(Schema Evolution) 용이성: Avro > Protobuf ≈ Thrift, ②언어 지원 폭: Protobuf ≈ Thrift > Avro, ③Kafka/Hadoop 생태계 통합: Avro > Protobuf > Thrift. 실무에서는 Kafka+Confluent Schema Registry = Avro, gRPC 서비스 = Protobuf가 사실상 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
+--------------------------------------------------------+
|     JSON vs. Avro vs. Protobuf 비교                    |
+-----------------+--------------------------------------+
| 형식            | 특징                                  |
+-----------------+--------------------------------------+
| JSON            | 사람이 읽기 쉬움, 크기 큼, 파싱 느림 |
| Avro            | 바이너리, 스키마 분리, Hadoop 친화    |
| Protobuf        | 바이너리, 스키마 필드 번호 기반, gRPC |
| Thrift          | 바이너리, RPC 통합, Meta 오리지널     |
+-----------------+--------------------------------------+
```

- **📢 섹션 요약 비유**: 직렬화 형식 선택은 국제 소포 포장 방식이다. JSON은 큰 종이 박스(사람이 읽기 쉽지만 부피가 크다), Avro/Protobuf는 진공 포장(작고 빠르지만 기계만 읽을 수 있다).

---

## Ⅱ. 아키텍처 및 핵심 원리

### 각 형식의 직렬화 방식

```text
Avro:
  - 스키마를 .avsc 파일(JSON)로 별도 정의
  - 데이터에 스키마 없음 -> Schema Registry에서 참조
  - 스키마 진화: 필드 추가/제거 + default값으로 backward/forward 호환

Protobuf:
  - .proto 파일에 스키마 정의
  - 각 필드에 고유 번호 (field=1, field=2...)
  - 번호 기반 인코딩 -> 필드명 변경해도 호환 유지

Thrift:
  - .thrift 파일에 데이터 + 서비스(RPC) 정의
  - 직렬화 + RPC 프레임워크 통합
  - Meta(Facebook) 오리지널
```

### Avro 스키마 예시

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

- **📢 섹션 요약 비유**: Avro 스키마는 택배 포장 명세서다. 포장 안에 무엇이 들어있는지(스키마)를 별도 문서로 관리하고, 실제 택배 상자(바이너리 데이터)는 내용물만 담아 최소 크기로 보낸다.

---

## Ⅲ. 비교 및 연결

| 비교 | Avro | Protobuf | Thrift |
|:---|:---|:---|:---|
| 스키마 언어 | JSON (.avsc) | IDL (.proto) | IDL (.thrift) |
| 스키마 진화 | Excellent | Good | Good |
| 바이트 효율 | Good | Better | Good |
| Kafka 통합 | Excellent | Good | Fair |
| gRPC 지원 | 없음 | Native | 없음 |
| 언어 지원 | 10+ | 13+ | 28+ |

- **📢 섹션 요약 비유**: Avro는 하둡·카프카 세계의 모국어, Protobuf는 구글 마이크로서비스의 모국어, Thrift는 Meta 데이터센터의 모국어다. 어느 세계에 사는지에 따라 가장 편한 언어가 다르다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### Kafka + Confluent Schema Registry + Avro

```text
Producer -> [Avro 직렬화] -> Kafka 토픽
              ^ 스키마 등록/조회
           Schema Registry
              v 스키마 조회/역직렬화
Consumer <- [Avro 역직렬화] <- Kafka 토픽
```

### gRPC + Protobuf
- 마이크로서비스 간 고속 통신: HTTP/2 + Protobuf 바이너리.
- .proto -> 각 언어 클라이언트 자동 생성.
- 스트리밍 지원: 단방향·양방향 스트리밍.

- **📢 섹션 요약 비유**: gRPC+Protobuf는 국제 은행 간 SWIFT 전문(電文) 시스템이다. 표준화된 형식(Protobuf)으로 빠르고 정확하게 정보를 전달하고, 수신 측은 자동으로 해석(역직렬화)한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **네트워크 효율** | JSON 대비 50~80% 데이터 크기 감소 |
| **처리 속도** | 바이너리 파싱으로 역직렬화 10배+ 향상 |
| <strong>스키마 관리</strong> | Schema Registry로 스키마 버전 중앙 관리 |

AI/ML 파이프라인에서 대규모 Feature Store와 모델 서빙에 Protobuf·Avro가 표준 직렬화로 자리잡고 있으며, Apache Arrow의 컬럼형 인메모리 포맷이 분석 워크로드에서 새로운 직렬화 표준으로 부상하고 있다.

- **📢 섹션 요약 비유**: Apache Arrow는 초고속 직렬화의 미래다. 행 단위(Avro/Protobuf) 대신 열 단위로 데이터를 정렬하여 CPU 캐시를 최적으로 활용 — 분석 쿼리가 수십 배 빨라진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Schema Registry</strong> | Avro 스키마 중앙 저장·버전 관리 |
| <strong>gRPC</strong> | Protobuf 기반 고성능 RPC 프레임워크 |
| <strong>Kafka</strong> | Avro/Protobuf 직렬화의 주요 활용 시스템 |
| **Apache Arrow** | 컬럼형 인메모리 직렬화 차세대 표준 |
| <strong>스키마 진화</strong> | 데이터 구조 변경 시 하위 호환성 유지 |

### 📈 관련 키워드 및 발전 흐름도

```text
[JSON/XML — 텍스트 직렬화, 사람 가독성, 크기 비효율]
    |
    v
[Avro/Protobuf/Thrift — 바이너리 직렬화, 효율성]
    |
    v
[Schema Registry — 스키마 버전 중앙 관리]
    |
    v
[gRPC + Protobuf — 마이크로서비스 표준 RPC]
    |
    v
[Apache Arrow — 컬럼형 인메모리 분석 직렬화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 직렬화는 데이터를 택배 상자에 포장하는 방법이에요! JSON은 큰 종이 박스, Avro/Protobuf는 진공 포장 — 훨씬 작고 빠르게 전달돼요!
2. Kafka에서는 Avro+Schema Registry가 표준, 마이크로서비스에서는 Protobuf+gRPC가 표준이에요!
3. Apache Arrow는 분석 전용 초고속 포장재예요 — 컬럼 단위로 정렬해서 수십 배 빠른 분석이 가능하답니다!
