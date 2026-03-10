+++
title = "537. 미리 읽기 (Read-ahead) 및 지연 쓰기 (Delayed-write / Write-behind)"
weight = 537
+++

# 537. I/O 벤치마크 (I/O Benchmarking)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: I/O 성능 측정 및 평가 방법
> 2. **가치**: 시스템 성능 최적화를 위한 데이터 제공
> 3. **융합**: 성능 튜닝, 프로파일링, 최적화와 연관

---

## Ⅰ. 개요

### 개념 정의
**I/O 벤치마크(I/O Benchmarking)**는 **시스템의 I/O 성능을 측정하고 평가하는 작업**입니다.

### 💡 비유: 자동차 주행 테스트
I/O 벤치마크는 **자동차의 성능 테스트**와 같습니다. 가속력, 제동력, 연비 등을 측정합니다.

### I/O 벤치마크 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                I/O 벤치마크 구조                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【주요 측정 항목】                                                │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  항목                설명                    단위                         │ │   │
│  │  ────                ────                    ───                         │ │   │
│  │  처리량(Throughput)    단위 시간당 데이터 양         MB/s, IOPS             │ │   │
│  │  지연 시간(Latency)     I/O 요청부터 완료까지 시간      ms/μs                   │ │   │
│  │  IOPS               초당 I/O 작업 수            ops/sec               │ │   │
│  │  대역폭(Bandwidth)    최대 데이터 전송 속도          MB/s                   │ │   │
│  │  큐 깊이(Queue Depth)    대기 중인 I/O 요청 수           개                     │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【벤치마크 도구】                                                      │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  도구                용도                    특징                         │ │   │
│  │  ────                ────                    ────                         │ │   │
│  │  fio                파일 시스템 성능             유연한 설정                   │ │   │
│  │  iozone             파일 시스템 벤치마크          다양한 테스트                 │ │   │
│  │  dd                기본 복사 성능             간단한 테스트                 │ │   │
│  │  iometer           스토리지 성능               종합 분석                     │ │   │
│  │  bonnie++          파일 시스템 성능             고전적 도구                   │ │   │
│  │  sysbench          종합 시스템 벤치마크         CPU/메모리/I/O                │ │   │
│  │  hdparm            디스크 성능 확인            기본 정보                     │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석
### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                I/O 벤치마크 상세                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【fio 사용법】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  // 순차 읽기                                                │ │   │
│  │  $ fio --name=seqread --filename=test.file \                        │
│  │        --rw=read --bs=1M --size=1G --numjobs=1                │ │   │
│  │                                                             │ │   │
│  │  // 랜덤 읽기                                                 │ │   │
│  │  $ fio --name=randread --filename=test.file \                       │
│  │        --rw=randread --bs=4k --size=1G --numjobs=4               │ │   │
│  │                                                             │ │   │
│  │  // 동기 쓰기                                                 │ │   │
│  │  $ fio --name=syncwrite --filename=test.file \                     │
│  │        --rw=write --bs=64k --size=1G --sync=1                   │ │   │
│  │                                                             │ │   │
│  │  // IOPS 측정                                                 │ │   │
│  │  $ fio --name=iops --filename=test.file \                            │ │   │
│  │        --rw=randread --bs=4k --size=10G --ioengine=libaio \          │ │   │
│  │        --iodepth=32 --numjobs=4                                 │ │   │
│  │                                                             │ │   │
│  │  // 혼합 워크로드                                               │ │   │
│  │  $ fio --name=mixed --filename=test.file \                           │ │   │
│  │        --rw=randrw --rwmixread=70 --bs=8k --size=1G                │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【iostat 결과 분석】                                               │
│  ──────────────────                                                │
│  $ iostat -x 1                                                   │
│  Device   rrqm/s  wrqm/s   r/s   w/s  rMB/s  wMB/s  await  %util      │
│  sda       0.50   10.00  50.0 100.0   2.00   4.00   5.00   80.0      │
│                                                                     │
│  // 항목 설명                                                        │
│  rrqm/s: 초당 병합된 읽기 요청                                       │
│  wrqm/s: 초당 병합된 쓰기 요청                                       │
│  r/s: 초당 읽기 요청                                                  │
│  w/s: 초당 쓰기 요청                                                  │
│  rMB/s: 초당 읽기 MB                                                   │
│  wMB/s: 초당 쓰기 MB                                                   │
│  await: 평균 I/O 대기 시간 (ms)                                       │
│  %util: 장치 활용률 (%)                                               │
│                                                                     │
│  【성능 기준】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  장치           순차 읽기       랜덤 읽기       IOPS             │ │   │
│  │  ────           ────────        ────────        ────             │ │   │
│  │  HDD (7200RPM)   ~150 MB/s      ~1 MB/s        ~100              │ │   │
│  │  HDD (10000RPM)  ~200 MB/s      ~1.5 MB/s      ~150             │ │   │
│  │  SATA SSD        ~550 MB/s      ~30 MB/s       ~50,000          │ │   │
│  │  NVMe SSD        ~3500 MB/s     ~100 MB/s      ~200,000         │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용
### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【fio 설정 파일 예시】                                               │
│  ──────────────────                                                │
│  # database_workload.fio                                            │
│  [global]                                                           │
│  ioengine=libaio                                                    │
│  iodepth=32                                                         │
│  size=10G                                                           │
│  directory=/mnt/test                                                │
│                                                                     │
│  [seq-read]                                                         │
│  name=Sequential Read                                               │
│  rw=read                                                             │
│  bs=1M                                                               │
│  numjobs=1                                                          │
│                                                                     │
│  [rand-read]                                                        │
│  name=Random Read                                                   │
│  rw=randread                                                         │
│  bs=8k                                                               │
│  numjobs=4                                                          │
│                                                                     │
│  [rand-write]                                                       │
│  name=Random Write                                                  │
│  rw=randwrite                                                        │
│  bs=8k                                                               │
│  numjobs=4                                                          │
│                                                                     │
│  [mixed-70-30]                                                      │
│  name=Mixed 70/30                                                   │
│  rw=randrw                                                           │
│  rwmixread=70                                                       │
│  bs=8k                                                               │
│  numjobs=4                                                          │
│                                                                     │
│  // 실행                                                            │
│  $ fio database_workload.fio                                        │
│                                                                     │
│  【iozone 예시】                                                     │
│  ──────────────────                                                │
│  // 기본 테스트                                                      │
│  $ iozone -a                                                        │
│                                                                     │
│  // 특정 파일 크기                                                   │
│  $ iozone -a -s 1G -y 4k -q 64k                                     │
│                                                                     │
│  // 대역폭 테스트                                                    │
│  $ iozone -r 4k -s 100m -t 4 -i 0 -i 1                             │
│                                                                     │
│  【sysbench I/O 테스트】                                              │
│  ──────────────────                                                │
│  // 파일 준비                                                        │
│  $ sysbench fileio --file-total-size=10G prepare                   │
│                                                                     │
│  // 순차 읽기 테스트                                                  │
│  $ sysbench fileio --file-total-size=10G \                         │
│        --file-test-mode=seqrd run                                   │
│                                                                     │
│  // 랜덤 읽기/쓰기 테스트                                             │
│  $ sysbench fileio --file-total-size=10G \                         │
│        --file-test-mode=rndrd run                                   │
│                                                                     │
│  // 정리                                                            │
│  $ sysbench fileio --file-total-size=10G cleanup                   │
│                                                                     │
│  【성능 병목 분석】                                                   │
│  ──────────────────                                                │
│  // 디스크 큐 확인                                                   │
│  $ cat /sys/block/sda/queue/nr_requests                              │
│  128                                                                 │
│                                                                     │
│  // 스케줄러 확인                                                    │
│  $ cat /sys/block/sda/queue/scheduler                               │
│  [mq-deadline] none                                                  │
│                                                                     │
│  // 장치 통계                                                        │
│  $ cat /proc/diskstats | grep sda                                   │
│                                                                     │
│  // blktrace 상세 분석                                               │
│  $ blktrace -d /dev/sda -o - | blkparse -i -                        │
│                                                                     │
│  【튜닝 권장사항】                                                    │
│  ──────────────────                                                │
│  // 읽기 성능 향상                                                    │
│  $ echo 256 > /sys/block/sda/queue/read_ahead_kb                   │
│                                                                     │
│  // 큐 깊이 증가                                                      │
│  $ echo 256 > /sys/block/sda/queue/nr_requests                      │
│                                                                     │
│  // NVMe 최적화                                                      │
│  $ echo none > /sys/block/nvme0n1/queue/scheduler                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: I/O 성능 측정 및 평가
• 항목: 처리량, 지연 시간, IOPS, 대역폭
• 도구: fio, iozone, dd, iometer, sysbench
• 기준: 장치별 성능 기준 존재
• 분석: iostat, blktrace, /proc/diskstats
• 튜닝: read_ahead, queue depth, scheduler
• 목적: 병목 식별, 성능 최적화
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [I/O 스케줄링](./516_io_scheduling.md) → I/O 최적화
- [파일 시스템 성능](../9_file_system/492_file_system_performance_tuning.md) → 성능 튜닝
- [성능 모니터링](../9_file_system/493_file_system_monitoring.md) → 상태 확인

### 👶 어린이를 위한 3줄 비유 설명
**개념**: I/O 벤치마크는 "자동차 주행 테스트" 같아요!

**원리**: 얼마나 빠른지 측정해요!

**효과**: 문제점을 찾아 개선해요!
