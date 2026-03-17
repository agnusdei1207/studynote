+++
title = "416. DML(Data Manipulation Language) - 데이터의 생동하는 변화"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 416
+++

# 416. DML(Data Manipulation Language) - 데이터의 생동하는 변화

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DML(데이터 조작 언어)은 정의된 스키마 구조 내에서 실제 데이터를 **삽입(INSERT), 수정(UPDATE), 삭제(DELETE), 조회(SELECT)**하기 위해 사용하는 SQL 명령어군이다.
> 2. **가치**: 비즈니스의 실시간 활동을 데이터베이스에 반영하는 핵심 수단이며, 쿼리를 통해 사용자가 원하는 정보를 추출하는 실질적인 인터페이스 역할을 한다.
> 3. **특징**: DDL과 달리 **트랜잭션(Transaction)**의 통제를 받으므로, 실행 후 결과를 검토하여 확정(COMMIT)하거나 취소(ROLLBACK)할 수 있는 안전성을 가진다.

+++

### Ⅰ. DML의 주요 명령어와 트랜잭션 관계

| 명령어 | 기능 | 롤백 가능 여부 |
|:---|:---|:---|
| **INSERT** | 새로운 데이터를 테이블에 **추가** | **가능** (커밋 전) |
| **UPDATE** | 기존 데이터의 내용을 **변경** | **가능** (커밋 전) |
| **DELETE** | 조건에 맞는 데이터를 **삭제** | **가능** (커밋 전) |
| **SELECT** | 데이터를 **조회**하여 결과 반환 | N/A (상태 변경 없음) |

+++

### Ⅱ. DML과 트랜잭션 흐름 시각화 (ASCII Flow)

DML은 즉시 디스크에 쓰이지 않고 메모리 버퍼와 로그에 먼저 기록됩니다.

```text
[ DML Transaction Lifecycle ]

  (User) ──▶ [ UPDATE Account SET Bal=0 ]
                   │
                   ▼ [ Buffer Pool (Mem) ]
            ┌─────────────────────────────┐
            │ 1. Old Value -> Undo Log    │ ⏪ (Back-up)
            │ 2. New Value -> Redo Log    │ ⏩ (Log)
            │ 3. Memory Page Modified     │ 📝 (Dirty)
            └──────────────┬──────────────┘
                           │
          ┌────────────────┴────────────────┐
          ▼ (User Decision)                 ▼
    [ COMMIT! ]                     [ ROLLBACK! ]
    - Make it Permanent             - Use Undo Log to RESTORE ✅
    - Release Locks                 - "As if nothing happened"
```

+++

### Ⅲ. DML 사용 시 주의사항: 무결성 제약

- **PK 중복**: `INSERT` 시 기본키가 중복되면 무결성 위반으로 거부됩니다.
- **FK 참조**: `DELETE` 시 다른 테이블에서 참조 중인 데이터를 지우려 하면 거부되거나 연쇄 삭제가 발생합니다.
- **Locking 병목**: 대량의 `UPDATE`나 `DELETE`는 해당 행들에 락을 걸어 다른 사용자의 접근을 차단하므로 주의해야 합니다.

- **📢 섹션 요약 비유**: DML은 **'노트에 연필로 글을 쓰는 것'**과 같습니다. 내용을 적고(INSERT), 지우개로 지우고(DELETE), 고쳐 쓰는(UPDATE) 행위는 내 마음대로 할 수 있고, 마음에 안 들면 '되돌리기(ROLLBACK)'도 쉽습니다. 하지만 마지막에 사인(COMMIT)을 하고 제출하는 순간, 그 내용은 공식적인 기록이 됩니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[CRUD]**: Create, Read, Update, Delete의 약자로 DML의 핵심 기능.
- **[Undo Log]**: DML의 롤백을 가능케 하는 기술적 근거.
- **[Isolation]**: 내가 DML을 수행하는 동안 남이 못 보게 막는 트랜잭션 성질.

📢 **마무리 요약**: **DML**은 사용자와 데이터가 만나는 최전선입니다. 트랜잭션이라는 보호막 아래에서 안전하고 유연하게 데이터를 다루는 것이 현대 데이터베이스 조작의 핵심입니다.