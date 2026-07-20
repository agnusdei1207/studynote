---
title: "Key-Value Solid-State Drive"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 594
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 키-밸류 SSD (Key-Value Solid-State Drive, KV-SSD)는 호스트가 논리 블록 주소 (Logical Block Address, LBA) 대신 key를 넘기면, 장치가 그 key에 대응하는 value의 위치와 저장 배치를 직접 관리하는 스토리지 인터페이스다.
> 2. **가치**: 작은 객체와 메타데이터가 많은 워크로드에서 파일 시스템, 블록 매핑, 사용자 공간 키-값 엔진이 겹쳐 만들던 중복 인덱싱과 데이터 복사를 줄여 중앙처리장치 (Central Processing Unit, CPU) 오버헤드와 쓰기 증폭을 낮출 수 있다.
> 3. **판단 포인트**: KV-SSD의 핵심 질문은 “스토리지가 key를 이해하느냐”보다 “내 워크로드가 point lookup 중심이고, 애플리케이션 프로그래밍 인터페이스 (Application Programming Interface, API)를 바꿀 수 있느냐”에 있으며, 범위 검색·복잡한 트랜잭션·2차 인덱스는 여전히 호스트 책임인 경우가 많다.

---

## Ⅰ. 개요 및 필요성

KV-SSD는 블록 주소 대신 key를 주고받는 저장장치다. 전통적인 SSD는 “몇 번째 블록을 읽고 쓸지”만 이해하지만, 실제 애플리케이션은 사용자 ID, 객체 ID, 세션 토큰, 파일 해시처럼 이미 key 중심으로 데이터를 다룬다. 그래서 지금까지는 애플리케이션의 key를 파일 시스템과 데이터베이스 엔진이 다시 블록 주소 체계로 번역해야 했고, 이 번역 과정이 메타데이터와 복사 비용을 누적시켰다.

특히 작은 객체가 매우 많고 갱신이 잦은 시스템일수록 이 불일치가 커진다. 호스트 쪽 키-값 저장소는 보통 로그 구조 병합 트리 (Log-Structured Merge Tree, LSM-Tree)나 유사 구조를 사용해 블록 장치 위에서 key semantics를 흉내 내는데, 이 과정에서 compaction, bloom filter, page cache, file metadata가 겹친다. KV-SSD는 이 중 일부 의미 해석을 장치 안쪽으로 내려, “원래 key로 다루던 데이터를 왜 끝에서야 다시 key로 되돌리느냐”라는 질문에 답하는 구조다.

아래 그림은 기존 블록 경로와 KV-SSD 경로를 비교한 것이다.

```text
+----------------------------------------------------------------------------+
| Block path emulates key semantics, KV-SSD exposes them directly           |
+----------------------------------------------------------------------------+
| Traditional path                                                          |
| Application -> Key-Value Engine -> File System -> Block SSD -> Flash      |
|                                                                            |
| KV-SSD path                                                               |
| Application / Key-Value Library -> PUT(GET, DELETE by key) -> KV-SSD -> Flash |
|                                                                            |
| Fewer translation layers, but the application must speak the new API      |
+----------------------------------------------------------------------------+
```

물론 KV-SSD가 모든 소프트웨어 레이어를 없애 주는 것은 아니다. 트랜잭션, 복제, 2차 인덱스, range query 같은 상위 데이터 서비스는 여전히 호스트가 맡는다. 그렇지만 “블록 장치가 모르는 key 의미를 상위 소프트웨어가 억지로 여러 번 재현한다”는 중복은 줄일 수 있어, 특히 metadata-heavy 시스템에서 가치가 커진다.

- **📢 섹션 요약 비유**: 기존 저장장치는 창고 칸 번호만 아는 직원이고, KV-SSD는 물건 이름표를 직접 읽을 수 있는 직원과 같다. 덕분에 손님이 “3층 12번 칸”을 외우지 않아도 되지만, 어떤 물건을 언제 폐기하고 어떻게 분류할지는 여전히 창고 운영자가 정해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

KV-SSD의 내부 동작은 크게 key 명령 수신, key 인덱스 조회, value 배치, flash 관리의 네 단계로 나뉜다. 호스트가 `put(key, value)`를 보내면 장치는 key를 해시하거나 인덱스로 조회해 기존 항목 여부를 판단하고, 새 value를 플래시에 기록한 뒤 key와 물리 위치의 대응 관계를 갱신한다. `get(key)`는 인덱스에서 위치를 찾고, `delete(key)`는 엔트리를 무효화하거나 tombstone 처리를 한다. 즉 인터페이스가 key 기반일 뿐, 내부 매체 관리까지 사라지는 것은 아니다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| Key Command Interface | put, get, delete, iterate 같은 명령을 받는다. | 애플리케이션이 블록 I/O 대신 KV API를 써야 한다. |
| Device-side Key Index | key를 value 위치와 연결한다. | 충돌 처리, key 길이, 메모리 사용량이 성능을 좌우한다. |
| Value Placement 엔진 | variable-length value를 실제 플래시 페이지에 배치한다. | 작은 객체와 큰 객체가 섞일 때 단편화와 정렬 정책이 중요하다. |
| Garbage Collection / Wear Leveling | 무효화된 value를 정리하고 마모를 분산한다. | KV semantics를 알아도 flash의 erase 제약은 여전히 존재한다. |
| Completion Queue | 비동기 결과와 상태를 호스트에 돌려준다. | 지연 시간, 배치 처리, 재시도 전략과 연결된다. |
| Namespace / Isolation Logic | 여러 application namespace를 분리한다. | 멀티 tenant 환경에서는 key 충돌 방지와 서비스 품질 (Quality of Service, QoS) 분리가 중요하다. |

아래 그림은 put과 get의 내부 흐름을 요약한다.

```text
+----------------------------------------------------------------------------+
| KV-SSD data path: key lookup outside, flash management still inside       |
+----------------------------------------------------------------------------+
| PUT(key, value) -> Key Index Lookup -> Allocate Flash Space -> Write Value |
|                                         |                                  |
|                                         +-> Update key -> physical map     |
|                                                                            |
| GET(key) -> Key Index Lookup -> Read Flash Pages -> Return value           |
| DELETE(key) -> Invalidate entry / mark obsolete                            |
+----------------------------------------------------------------------------+
```

이 구조에서 자주 오해되는 부분은 “KV-SSD면 파일 시스템과 데이터베이스가 완전히 필요 없어지는가”이다. 실제로는 그렇지 않다. 장치가 key를 이해해도 데이터 모델 전체를 이해하는 것은 아니며, 정렬 순서, 복제 일관성, 버전 관리, 범위 스캔은 상위 계층이 계속 맡는다. KV-SSD의 본질은 데이터베이스 전체를 SSD에 넣는 것이 아니라, <strong>블록 기반 저장장치가 강요하던 불필요한 주소 번역을 줄이는 것</strong>이다.

- **📢 섹션 요약 비유**: 도서관이 책 제목으로 바로 찾아 주는 시스템을 갖췄다고 해서, 분류 체계나 대출 규칙까지 모두 없어지는 것은 아니다. 책 찾기는 쉬워지지만, 어떤 책을 어떤 코너에 둘지와 대출 정책은 도서관이 계속 관리해야 한다.

---

## Ⅲ. 비교 및 연결

KV-SSD를 제대로 이해하려면 블록 SSD, 존 스토리지, 스마트 SSD와의 경계를 함께 보는 것이 좋다. 블록 SSD는 주소 기반 저장을 제공하고, 존 스토리지는 여전히 주소 기반이지만 쓰기 규칙을 바꾸며, 스마트 SSD는 저장장치에 연산을 얹는다. KV-SSD는 이 셋과 달리 <strong>저장 인터페이스의 의미 단위를 block에서 key-value object로 끌어올린다</strong>는 점이 핵심이다.

| 방식 | 인터페이스 단위 | 장점 | 한계 |
| :--- | :--- | :--- | :--- |
| 블록 SSD | LBA + 고정 크기 블록 | 범용성이 가장 높고 기존 소프트웨어와 잘 맞는다 | key semantics를 상위 소프트웨어가 반복 구현해야 한다 |
| 존 스토리지 | LBA + 순차 존 규칙 | WAF와 tail latency를 줄이기 쉽다 | 여전히 주소 기반이며 zone-aware 설계가 필요하다 |
| KV-SSD | key + value | 작은 객체와 point lookup에서 레이어 중복을 줄인다 | 범위 검색, 복잡한 트랜잭션, 이식성 문제가 남는다 |
| 스마트 SSD | block 또는 vendor command + in-drive compute | 필터링·압축·검색을 장치 안에서 수행한다 | 저장 의미를 바꾸기보다 계산 오프로딩에 가깝다 |

이 비교가 중요한 이유는 KV-SSD가 “더 똑똑한 SSD”라는 표현 하나로는 설명되지 않기 때문이다. 존 스토리지는 물리 쓰기 규칙을 노출하는 기술이고, KV-SSD는 데이터 의미를 더 가깝게 노출하는 기술이며, 스마트 SSD는 계산을 더 가까이 붙이는 기술이다. 서로 경쟁 관계라기보다, 저장장치가 점점 더 <strong>블록 이상의 의미</strong>를 가지기 시작했다는 같은 흐름 안에 있다.

또한 KV-SSD는 객체 저장소와도 닮았지만 완전히 같지는 않다. 객체 저장소는 네트워크 서비스와 메타데이터 체계를 포함하는 상위 시스템이고, KV-SSD는 그보다 훨씬 아래의 장치 인터페이스다. 즉 KV-SSD는 네트워크 객체 저장소를 대체한다기보다, 로컬 장치 수준에서 key-addressable semantics를 제공하는 기반이라고 보는 편이 정확하다.

- **📢 섹션 요약 비유**: 블록 SSD가 사서가 책장 번호만 알려 주는 도서관이라면, 존 스토리지는 책을 한 줄씩 꽂아야 하는 서가 규칙을 알려 주는 도서관이고, KV-SSD는 책 제목만 말하면 직접 찾아주는 도서관이다. 스마트 SSD는 거기에 더해 책 내용을 미리 요약해 주는 사서를 붙인 경우에 가깝다.

---

## Ⅳ. 실무 적용 및 실무자 판단

KV-SSD가 특히 잘 맞는 환경은 key 자체가 이미 서비스의 기본 단위인 시스템이다. 예를 들어 사용자 프로필, 세션 데이터, 객체 메타데이터, 캐시 항목, 로그 색인 정보처럼 point lookup과 simple CRUD(Create, Read, Update, Delete)가 중심인 경우에는 호스트 쪽 LSM-Tree 오버헤드를 줄이고, 작은 객체 처리 효율을 높일 여지가 있다. 반면 긴 range scan, 정렬 집약 분석, 복잡한 관계형 질의처럼 key 외의 관계를 많이 쓰는 시스템은 장치만 KV화한다고 문제가 해결되지 않는다.

실무에서는 API 전환 비용과 운영 가시성이 가장 큰 변수다. 블록 장치는 운영체제와 파일 시스템이 이미 잘 감싸 주지만, KV-SSD는 응용이 직접 또는 전용 라이브러리를 통해 key 명령을 말해야 한다. 또한 key 인덱스의 메모리 사용량, 긴 key의 비용, 멀티 tenant namespace 설계, 장애 시 복구 경로 같은 문제가 함께 따라오므로, “단순히 장치가 똑똑하니 더 빠르겠지” 식 접근은 위험하다.

### 적용 판단 체크리스트

1. 워크로드의 중심이 point get / put / delete이며 range scan 비중이 낮은가?
2. 애플리케이션이 KV 전용 API로 직접 접근하도록 수정할 수 있는가?
3. 평균 key 길이와 value 크기가 장치 인덱스 메모리를 과도하게 잡아먹지 않는가?
4. 트랜잭션, 복제, secondary index 같은 상위 기능을 여전히 호스트에서 설계할 준비가 되어 있는가?
5. key hit ratio, device-side index 메모리 사용량, invalid value 비율 같은 운영 지표를 관찰할 수 있는가?

### 피해야 할 안티패턴

- 이식 가능 운영체제 인터페이스 (Portable Operating System Interface, POSIX) 파일 시스템 기반 응용을 거의 그대로 둔 채 장치만 KV-SSD로 바꾸는 기대
- 지나치게 긴 key를 남발해 인덱스 메모리와 비교 비용을 불필요하게 키우는 설계
- KV-SSD가 있으니 compaction, caching, replication 문제도 자동으로 사라질 것이라 가정하는 판단
- 멀티 tenant 환경에서 namespace 격리와 quota 설계를 하지 않아 key 충돌과 noisy neighbor를 만드는 운영

- **📢 섹션 요약 비유**: KV-SSD는 이름표를 읽을 수 있는 창고 직원이지만, 어떤 물건을 언제 버리고 어떻게 분류할지까지 대신 결정해 주는 창고 관리자까지는 아니다. 이름표를 읽는 장점은 분명하지만, 창고 운영 규칙은 여전히 따로 있어야 한다.

---

## Ⅴ. 기대효과 및 결론

KV-SSD를 잘 적용하면 작은 객체가 많은 서비스에서 중복된 메타데이터 층을 줄여 CPU와 동적 램 (Dynamic Random Access Memory, DRAM) 부담을 낮출 수 있다. 또한 device-side index가 key와 value 배치를 더 직접 연결하므로, 일부 워크로드에서는 block-based stack보다 낮은 쓰기 증폭 계수 (Write Amplification Factor, WAF)와 더 짧은 lookup 경로를 기대할 수 있다. 즉 이 기술의 핵심 가치는 raw bandwidth보다 <strong>semantic mismatch를 줄여 얻는 시스템 단순화</strong>에 있다.

하지만 범용성은 블록 장치보다 떨어진다. 소프트웨어 생태계가 아직 넓지 않고, 벤더별 명령 집합과 tooling 차이가 남아 있으며, range query나 transaction semantics는 계속 호스트가 맡아야 한다. 앞으로의 방향은 KV-SSD가 단독으로 세상을 바꾸기보다, zone-aware 저장소, 계산형 스토리지, 객체 메타데이터 엔진과 결합해 <strong>의미를 더 아는 저장장치</strong>의 한 축으로 자리 잡는 쪽에 가깝다.

결론적으로 KV-SSD는 “SSD가 데이터베이스를 완전히 대체한다”는 과장으로 기억할 기술이 아니다. 오히려 <strong>블록 주소가 강요하던 불필요한 번역을 줄여, key-addressed workload를 더 자연스럽게 저장장치에 연결하는 인터페이스 혁신</strong>으로 기억하는 편이 정확하다.

- **📢 섹션 요약 비유**: 좋은 비서는 서류철 번호만 아는 사람이 아니라, 문서 제목을 듣고 바로 찾아오는 사람이다. KV-SSD도 저장장치가 그런 비서처럼 key를 이해하게 만들어, 사람과 창고 사이의 불필요한 전달 단계를 줄여 준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 논리 블록 주소 (Logical Block Address, LBA) | KV-SSD가 줄이려는 기존 저장 인터페이스의 핵심 추상화다. |
| 로그 구조 병합 트리 (Log-Structured Merge Tree, LSM-Tree) | 블록 장치 위에서 key semantics를 흉내 내는 대표 구조로, KV-SSD의 도입 배경과 직결된다. |
| 쓰기 증폭 계수 (Write Amplification Factor, WAF) | 중복 compaction과 내부 이동이 줄면 개선을 기대할 수 있는 핵심 지표다. |
| 객체 저장소 (Object Storage) | key-addressable semantics를 상위 시스템에서 제공하는 구조로, KV-SSD와 철학적으로 맞닿아 있다. |
| 존 스토리지 (Zoned Storage) | 물리 쓰기 규칙을 노출하는 기술로, 의미 단위를 바꾸는 KV-SSD와 해결 계층이 다르다. |
| 계산형 스토리지 (Computational Storage) | 저장장치가 block 저장만 넘어서 의미와 계산을 더 많이 맡아 가는 큰 흐름을 보여 준다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Block I/O + Host-side KV Engine
              |
              v
LSM-Tree · File System · Page Cache 중첩
              |
              v
Device-level key command set
              |
              v
KV-SSD
              |
              v
Semantic Storage · Data-Centric Access
```

이 흐름은 저장장치가 단순히 블록을 주고받는 계층에서 출발해, 이제는 애플리케이션의 key 의미를 더 직접 이해하는 방향으로 이동하고 있음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 예전에는 장난감을 찾으려면 “세 번째 서랍 네 번째 칸” 같은 위치를 기억해야 했어요.
2. KV-SSD는 “빨간 자동차 찾아 줘”처럼 이름만 말하면 상자가 알아서 꺼내 주는 방식이에요.
3. 그래서 찾기는 쉬워지지만, 어떤 장난감을 어디에 모아 둘지는 여전히 우리가 정해 줘야 한답니다.
