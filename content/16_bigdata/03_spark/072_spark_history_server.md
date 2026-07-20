---
title: "Spark History Server"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 72
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Spark History Server는 완료된 Spark 애플리케이션의 이벤트 로그(Event Log)를 HDFS/S3에서 읽어 Web UI로 시각화하는 독립 데몬으로, 실행 중인 SparkUI가 종료된 후에도 작업 실행 계획·스테이지·태스크 세부 정보를 사후 분석할 수 있게 한다.
- **가치**: 성능 병목 진단(어느 스테이지가 느렸는지), 메모리 스필(Spill) 여부, 셔플 I/O, 태스크 편차(Skew) 등을 Spark History Server의 Execution Plan과 Stage 탭에서 분석하면 코드 변경 없이 클러스터 최적화 방향을 도출할 수 있다.
- **판단 포인트**: History Server 없이 운영하면 장시간 실행된 작업이 완료 후 디버깅 수단이 사라지므로, 프로덕션 환경에서는 반드시 `spark.eventLog.enabled=true`와 이벤트 로그 저장 경로를 설정해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. Spark Web UI의 임시성 문제

Spark 애플리케이션 실행 중에는 `http://driver-host:4040`으로 실시간 Web UI에 접근할 수 있다. 그러나 애플리케이션이 종료되면 이 UI도 사라진다.

문제 시나리오:
- 어제 밤 배치 작업이 2시간 걸렸다 -> 왜 느렸는지 분석하려면?
- 클러스터에서 동시에 수십 개 작업이 실행 중 -> 과거 완료 작업 추적이 필요하다면?

Spark History Server는 이 공백을 채우는 <strong>사후 분석(Post-mortem Analysis) 도구</strong>다.

### 2. 이벤트 로그 기반 동작

애플리케이션 실행 중 Spark은 모든 이벤트(스테이지 시작/완료, 태스크 지표, 실행 계획 등)를 JSON 형태의 이벤트 로그 파일로 기록한다. History Server는 이 파일을 읽어 UI를 재구성한다.

**📢 섹션 요약 비유**
> Spark History Server는 "항공기 블랙박스 분석 센터"와 같다. 비행(작업)이 끝난 후 블랙박스(이벤트 로그)를 분석하여 어느 구간에서 이상이 있었는지 사후에 정밀 진단한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. History Server 동작 흐름

```
+------------------------------------------------------------+
|  Spark Application (실행 중)                                |
|                                                            |
|  Driver --- Event 생성 ---> EventLog Writer                 |
|             (Stage/Task/Executor 이벤트)                   |
+--------------------------+---------------------------------+
                           | 이벤트 로그 파일 스트리밍 기록
                           v
              +-------------------------+
              |  HDFS / S3 / 로컬       |
              |  /spark/eventlogs/      |
              |  app_001.json.inprogress|
              |  app_001.json (완료 후) |
              +------------+------------+
                           | 주기적 스캔
                           v
+----------------------------------------------------------+
|  Spark History Server (18080 포트)                        |
|                                                          |
|  +---------+  +----------+  +----------+  +----------+ |
|  | Jobs 탭 |  |Stages 탭 |  |Storage탭 |  |SQL 탭    | |
|  +---------+  +----------+  +----------+  +----------+ |
+----------------------------------------------------------+
              브라우저 접속: http://history-server:18080
```

### 2. 핵심 설정

```xml
<!-- spark-defaults.conf 또는 SparkSession 설정 -->

<!-- 이벤트 로그 활성화 (필수) -->
spark.eventLog.enabled=true
spark.eventLog.dir=hdfs:///spark/eventlogs

<!-- History Server 설정 (spark-env.sh) -->
SPARK_HISTORY_OPTS="-Dspark.history.fs.logDirectory=hdfs:///spark/eventlogs
                    -Dspark.history.ui.port=18080
                    -Dspark.history.retainedApplications=50"
```

```bash
# History Server 시작/중지
$SPARK_HOME/sbin/start-history-server.sh
$SPARK_HOME/sbin/stop-history-server.sh
```

### 3. History Server 주요 탭 및 분석 포인트

| 탭 | 주요 분석 내용 | 성능 문제 징후 |
|:---|:---|:---|
| Jobs | 잡 실행 시간, 완료/실패 수 | 특정 잡 비정상적으로 오래 걸림 |
| Stages | 스테이지별 소요 시간, 셔플 R/W | 셔플 크기 과다, 스테이지 재시도 발생 |
| Tasks | 태스크별 Duration, Spill 크기 | 특정 태스크만 느림 (Skew), GC 시간 과다 |
| SQL | 물리적 실행 계획 시각화 | BroadcastJoin vs SortMergeJoin 선택 확인 |
| Executors | Executor별 GC 시간, Spill 크기 | 특정 Executor 과부하 |
| Environment | Spark 설정값 확인 | 설정 오류 디버깅 |

**📢 섹션 요약 비유**
> History Server의 각 탭은 "공장 생산라인 CCTV 영상"이다. 잡 탭은 전체 생산량, 스테이지 탭은 공정별 소요 시간, 태스크 탭은 직원별 작업 시간, SQL 탭은 작업 설계도를 보여준다.

---

## Ⅲ. 비교 및 연결

### 1. History Server vs 실시간 Spark UI (4040)

| 항목 | 실시간 UI (4040) | History Server (18080) |
|:---|:---|:---|
| 접근 시점 | 애플리케이션 실행 중 | 완료 후 (또는 실행 중도 미러링) |
| 데이터 소스 | 드라이버 메모리 내 실시간 이벤트 | 이벤트 로그 파일 (HDFS/S3) |
| 지속성 | 앱 종료 시 사라짐 | 이벤트 로그 보존 기간 동안 유지 |
| 다중 앱 조회 | 단일 앱만 | 모든 완료 앱 목록 조회 |

### 2. 연결 개념

- <strong>이벤트 로그</strong>: History Server의 데이터 소스
- <strong>Spark SQL 탭</strong>: Catalyst 실행 계획 시각화 -> AQE 적용 여부 확인
- <strong>Ganglia / Prometheus + Grafana</strong>: 클러스터 수준 모니터링과 보완

**📢 섹션 요약 비유**
> 실시간 Spark UI는 "경기 중 스코어보드", History Server는 "경기 종료 후 하이라이트 분석 영상"이다. 둘 다 필요하지만 문제 분석은 주로 하이라이트 영상에서 이루어진다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. 성능 병목 진단 체크리스트 (History Server 활용)

- [ ] <strong>Stage Duration 확인</strong>: 특정 Stage가 전체의 80% 이상 차지 -> 해당 Stage 병목 집중 분석
- [ ] <strong>Task Duration 분포</strong>: 동일 Stage 내 태스크 편차가 10배 이상 -> Skew 의심
- [ ] **Shuffle Spill 크기**: 메모리 스필 > 0 -> `spark.executor.memory` 증가 또는 파티션 수 조정
- [ ] **GC Time 비율**: Executor GC Time > 총 실행 시간의 5% -> 힙 메모리 부족 신호
- [ ] <strong>SQL 탭 실행 계획</strong>: BroadcastHashJoin 대신 SortMergeJoin -> 소규모 테이블 힌트 추가
- [ ] **Failed Stages/Tasks**: 재시도 횟수 확인 -> 하드웨어 오류 또는 OOM 여부 판단

### 2. 이벤트 로그 용량 관리

```bash
# 이벤트 로그는 장기 보존 시 HDFS 공간 소모
# 주기적 정리 설정
spark.history.fs.cleaner.enabled=true
spark.history.fs.cleaner.interval=1d
spark.history.fs.cleaner.maxAge=7d  # 7일 이후 자동 삭제
```

**📢 섹션 요약 비유**
> History Server 진단은 "환자 혈액 검사 결과지 보는 것"이다. Stage Duration은 혈당, Shuffle Spill은 콜레스테롤, GC Time은 백혈구 수치다. 수치가 비정상이면 해당 원인을 찾아 처방(설정 조정)한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 사후 디버깅 가능 | 완료 후에도 실행 계획 및 성능 지표 분석 |
| 튜닝 근거 확보 | 객관적 지표로 파티션 수, 메모리 설정 조정 |
| 장애 원인 파악 | 실패한 태스크 오류 메시지 및 스택 트레이스 확인 |
| 운영 효율화 | 전체 클러스터 작업 이력 중앙 관리 |

### 2. 결론

Spark History Server는 프로덕션 Spark 클러스터의 <strong>필수 운영 인프라</strong>다. 이벤트 로그 활성화와 History Server 배포는 클러스터 구성 초기에 반드시 포함해야 하며, SQL 탭의 실행 계획 시각화를 활용한 쿼리 최적화는 실무자 수준의 Spark 운영 역량을 보여준다.

**📢 섹션 요약 비유**
> Spark History Server 없는 클러스터 운영은 "비행기록장치 없는 항공사 운영"과 같다. 사고가 났을 때(성능 문제) 원인을 알 수 없으므로, 블랙박스(이벤트 로그)와 분석 센터(History Server)는 필수 안전 장치다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| 이벤트 로그 (Event Log) | 데이터 소스 | History Server가 읽는 JSON 로그 파일 |
| Spark Web UI (4040) | 실시간 대응 | 실행 중 모니터링의 상호 보완 도구 |
| AQE (Adaptive Query Execution) | 확인 대상 | SQL 탭에서 AQE 재최적화 적용 여부 확인 |
| Ganglia / Prometheus | 보완 도구 | 클러스터 수준 메트릭과 Spark 앱 수준 분석 병행 |
| HDFS / S3 | 저장 위치 | 이벤트 로그의 안정적 저장소 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Spark Web UI (포트 4040 — 실시간 작업 모니터링)]
    |
    v
[이벤트 로그 (Event Log — HDFS/S3 영구 저장)]
    |
    v
[Spark History Server (포트 18080 — 사후 분석 UI)]
    |
    v
[SQL 탭 실행 계획 시각화 (AQE 재최적화 확인)]
    |
    v
[Prometheus / Grafana 연계 — 클러스터 메트릭 통합 대시보드]
```
Spark 작업 완료 후 사후 분석은 History Server가 담당하며, 이벤트 로그를 기반으로 SQL 실행 계획의 병목을 시각화하고 Prometheus/Grafana와 연계해 운영 인텔리전스를 완성한다.

### 👶 어린이를 위한 3줄 비유 설명

Spark History Server는 학교 숙제 검사 일지 같은 것이에요. 숙제(Spark 작업)가 끝나면 선생님(History Server)이 "누가 얼마나 빠르게 풀었는지, 어디서 막혔는지" 일지에 적어두어요. 나중에 숙제가 왜 어려웠는지 확인하고 싶을 때 이 일지를 보면 된답니다!
