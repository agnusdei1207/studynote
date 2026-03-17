+++
title = "444. 영속성(Durability) - 잊히지 않는 데이터의 약속"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 444
+++

# 444. 영속성(Durability) - 잊히지 않는 데이터의 약속

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 영속성은 성공적으로 완료(Commit)된 트랜잭션의 결과는 **시스템 장애(정전, 하드웨어 고장 등)가 발생하더라도 영구적으로 보존**되어야 함을 의미한다.
> 2. **가치**: "이미 끝난 일은 절대 취소되지 않는다"는 신뢰를 사용자에게 부여하며, 예기치 못한 사고 후에도 데이터베이스를 장애 직전의 최신 상태로 재현 가능케 한다.
> 3. **융합**: 비휘발성 저장 장치로의 기록과 **WAL(Write-Ahead Logging)** 프로토콜이 융합되어 구현되며, 복구 시 Redo 로그를 재실행하는 복구 관리자의 핵심 목표가 된다.

+++

### Ⅰ. 영속성의 물리적 구현

트랜잭션이 성공했다고 사용자에게 알리는 시점에, 데이터는 반드시 **디스크(Non-volatile Storage)**에 안전하게 기록되어야 합니다.
- **Log First**: 실제 데이터 파일을 고치는 것보다, 변경 내역을 담은 로그를 디스크에 먼저 쓰는 것이 훨씬 빠르고 안전합니다. (WAL)
- **Commit Confirm**: 로그가 디스크에 물리적으로 기록(fsync)되는 순간, 비로소 영속성이 확보된 것으로 간주합니다.

+++

### Ⅱ. 영속성 보장 매커니즘 시각화 (ASCII Model)

```text
[ Durability: The Shield against Crash ]

  1. SQL Commit Requested
  2. [ Log Buffer (Mem) ] ──▶ [ Redo Log File (Disk) ] 💾 (Flush!)
  3. "COMMIT SUCCESS" Message sent to User ✅
  
  (--- 💥 SYSTEM CRASH! Memory Erased ---)
  
  4. System Restart
  5. [ Recovery Manager ] reads [ Redo Log File (Disk) ]
  6. Replay Transactions ──▶ [ Data File ] is UPDATED! ✅
  "장애 전의 약속을 로그가 기억하고 복구함"
```

+++

### Ⅲ. 영속성과 성능의 조율

- **Sync vs Async Commit**: 
    - 매번 디스크 쓰기를 기다리면(Sync) 영속성은 완벽하지만 성능이 느려집니다. 
    - 가끔 로그를 몰아서 쓰면(Async) 빠르지만, 찰나의 장애 시 1~2초 분량의 데이터 유실을 감수해야 할 수도 있습니다.
- **하드웨어 보강**: 배터리가 내장된 캐시 컨트롤러나 고성능 NVMe SSD를 통해 영속성 확보 시간을 단축시킵니다.

- **📢 섹션 요약 비유**: 영속성은 **'은행 통장의 인출 기록'**과 같습니다. 인출기에서 "돈이 출금되었습니다"라는 메시지를 본 뒤에(Commit), 갑자기 은행 전체가 정전이 된다고 해서 내 통장의 잔액 기록이 예전으로 돌아가지는 않는 것과 같습니다. 은행 시스템은 어떤 사고가 나도 '이미 처리된 거래'는 절대 잊어버리지 않도록 기록(Log)을 겹겹이 쌓아두기 때문입니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Redo Log]**: 영속성을 지키는 가장 강력한 기록물.
- **[WAL (Write-Ahead Logging)]**: 영속성 구현의 글로벌 표준 규약.
- **[Check-pointing]**: 영속성은 유지하되 복구 시간을 줄이기 위한 중간 저장 기법.

📢 **마무리 요약**: **Durability**는 데이터베이스의 생명력입니다. 어떤 재난 상황에서도 "데이터는 살아남는다"는 믿음을 실현함으로써 정보 사회의 근간을 지탱합니다.