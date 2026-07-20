---
title: "Stream Processing"
weight: 4
sort_by: "weight"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 하둡이나 스파크 배치가 '과거의 데이터'를 한 번에 처리한다면, 스트리밍 처리는 센서, 로그, 금융 거래 등 쉴 새 없이 쏟아지는 '현재의 데이터'를 파이프라인(Event Stream)에서 실시간으로 처리하는 기술이다.
> 2. **가치**: 고객의 사기 거래(FDS)를 결제 1초 만에 차단하거나, 쇼핑몰 접속 10초 만에 관심 상품을 추천하는 등 비즈니스의 '골든 타임(Golden Time)'을 확보하여 즉각적인 수익 창출과 리스크 방어를 가능케 한다.
> 3. **융합**: 데이터를 안정적으로 버퍼링하는 메시지 브로커(Apache Kafka)와, 도착한 데이터를 밀리초(ms) 단위로 연산하는 스트림 엔진(Apache Flink, Storm, Spark Streaming)이 결합된 람다/카파(Lambda/Kappa) 아키텍처로 완성된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

스트리밍 데이터는 "끝이 없는 데이터(Unbounded Data)"입니다. 기존의 데이터베이스나 배치 시스템은 데이터가 모두 도착했다고 가정하고 연산하지만, 스트리밍 시스템은 데이터가 영원히 들어온다고 가정하고 '창문(Window)' 단위로 잘라서 끊임없이 계산을 수행합니다.

이 섹션에서는 스트리밍 파이프라인의 대동맥 역할을 하는 <strong>Apache Kafka</strong>와 실시간 연산의 표준인 **Apache Flink**, 그리고 스트리밍 처리 시스템이 반드시 보장해야 하는 `Exactly-Once`(정확히 한 번 처리) 시맨틱의 원리를 다룹니다.

### 📈 관련 키워드 및 발전 흐름도

```text
배치 처리 (Hadoop MapReduce)
    |
    v
마이크로 배치 (Spark Streaming)
    |
    v
진정한 스트리밍 (Apache Flink, Apache Storm)
    |
    +-► Apache Kafka — 분산 메시지 큐 (영속성 스트림)
    +-► Exactly-Once 시맨틱
    +-► Watermark 기반 이벤트 시간 처리
    |
    v
카파 아키텍처 (배치 제거, 스트림 단일화)
```
