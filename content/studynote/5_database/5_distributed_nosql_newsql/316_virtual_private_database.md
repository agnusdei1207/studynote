+++
title = "316. 가상 프라이빗 데이터베이스 (VPD) - 보이지 않는 보안의 벽"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 316
+++

# 316. 가상 프라이빗 데이터베이스 (VPD, Virtual Private Database)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: VPD(Virtual Private Database)는 사용자가 제출한 SQL 질의를 데이터베이스 엔진이 가로채어, **보안 정책에 따른 조건절(WHERE 절)을 자동으로 추가함으로써 사용자별로 허용된 데이터만 보이게 하는 동적 보안 기술**이다.
> 2. **가치**: 애플리케이션 레벨에서 복잡한 권한 로직을 구현할 필요 없이 DB 레벨에서 행(Row) 및 열(Column) 단위의 **미세 권한 제어(Fine-Grained Access Control)**를 완벽히 수행한다.
> 3. **융합**: 멀티테넌트(Multi-tenant) 아키텍처와 융합되어, 하나의 공유 테이블 안에서도 각 고객사가 오직 자신의 데이터만 볼 수 있도록 격리하는 논리적 방벽 역할을 한다.

+++

### Ⅰ. VPD의 작동 매커니즘

1. **사용자 요청**: 사용자가 `SELECT * FROM Orders;` 쿼리를 날립니다.
2. **보안 정책 적용**: DB 엔진은 설정된 VPD 정책을 확인합니다. (예: "부서장이면 자기 부서 것만 봐라")
3. **질의 재작성 (Query Rewrite)**: 엔진이 내부적으로 쿼리를 수정합니다. ──▶ `SELECT * FROM Orders WHERE Dept_ID = 'Sales';`
4. **결과 반환**: 수정된 쿼리에 따른 필터링된 결과만 사용자에게 전달됩니다.

+++

### Ⅱ. VPD 아키텍처 시각화 (ASCII Flow)

```text
[ VPD Query Rewrite Process ]

  (User: Agent_K) ──▶ [ SQL: SELECT * FROM Clients ]
                             │
                             ▼
                    ┌──────────────────┐
                    │ DB Policy Engine │ ◀── [ Context: Agent_K / Region: Asia ]
                    └────────┬─────────┘
                             │ (Rewrite)
                             ▼
                    [ Modified SQL:    ]
                    [ SELECT * FROM Clients WHERE Region = 'Asia' ]
                             │
                             ▼
                    [ Actual Data Access ] ──▶ ✅ Filtered Results
```

+++

### Ⅲ. VPD의 주요 장점

- **중앙 집중식 보안**: 보안 규칙이 DB에 있으므로, 어떤 툴(웹, 모바일, CLI)로 접속하든 동일한 보안 정책이 강제됩니다.
- **개발 생산성**: 개발자가 SQL마다 권한 체크 로직을 일일이 넣지 않아도 되므로 실수가 줄어들고 코드가 단순해집니다.
- **성능 효율**: 뷰(View)를 수천 개 만드는 것보다 시스템 부하가 적고 관리가 용이합니다.

- **📢 섹션 요약 비유**: VPD는 **'사용자 맞춤형 마법 안경'**과 같습니다. 데이터베이스라는 큰 방에 온갖 물건이 다 들어있지만, 내가 어떤 안경(VPD 정책)을 쓰고 들어갔느냐에 따라 내 눈에는 내가 가질 자격이 있는 물건들만 보이고 나머지는 투명하게 사라지는 것과 같습니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[FGAC]**: Fine-Grained Access Control의 약자로 VPD의 기술적 원형.
- **[Application Context]**: 세션 정보를 DB 정책에 전달하는 매개체.
- **[Row Level Security]**: PostgreSQL이나 SQL Server에서 VPD와 유사하게 작동하는 기능.

📢 **마무리 요약**: **VPD**는 데이터베이스 보안의 정수입니다. 데이터의 양이 방대해지고 사용자가 다양해지는 현대 환경에서, 가장 신뢰할 수 있는 데이터 격리 및 보호 솔루션입니다.