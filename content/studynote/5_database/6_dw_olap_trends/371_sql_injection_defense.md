+++
title = "371. SQL 인젝션 공격 및 방어 - 데이터베이스 보안의 기본"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 371
+++

# 371. SQL 인젝션 공격 및 방어 - 데이터베이스 보안의 기본

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL 인젝션(Injection)은 사용자의 입력값에 악의적인 SQL 구문을 삽입하여 **데이터베이스 엔진이 공격자가 의도한 쿼리를 비정상적으로 실행하게 만드는 웹 보안 취약점**이다.
> 2. **가치**: 미인증 사용자의 데이터 열람, 삭제, 관리자 권한 탈취 등 파괴적인 결과를 초래할 수 있으므로, 웹 애플리케이션 보안 설계에서 가장 우선적으로 해결해야 할 과제다.
> 3. **융합**: Prepared Statement(바인드 변수) 사용, 입력값 검증, DB 방화벽 기술이 융합되어 다층 방어 체계(Defense in Depth)를 구축함으로써 공격을 원천 무력화한다.

+++

### Ⅰ. SQL 인젝션의 주요 유형

1. **Error-based**: 고의로 에러를 유발하여 에러 메시지 속에 포함된 DB 정보를 탈취하는 방식.
2. **Union-based**: `UNION` 연산자를 사용하여 원래 쿼리 결과에 공격자가 원하는 테이블 정보를 합쳐서 출력하는 방식.
3. **Blind SQL Injection**: 쿼리 결과가 화면에 나오지 않아도, 참/거짓 응답이나 응답 시간 차이(Time-based)를 보고 데이터를 한 글자씩 유추하는 방식.

+++

### Ⅱ. 방어 매커니즘: Prepared Statement (ASCII Flow)

공격자가 `' OR '1'='1` 과 같은 구문을 넣어도 데이터로만 처리되게 하는 것이 핵심입니다.

```text
[ Unsafe Query (String Concatenation) ]
  Query: "SELECT * FROM Users WHERE ID = '" + input + "';"
  Input: "admin' --"
  Result: SELECT * FROM Users WHERE ID = 'admin' --'; (비정상 실행 💥)

[ Safe Query (Prepared Statement) ]
  Query: "SELECT * FROM Users WHERE ID = ?;"
  Input: "admin' --"
  Result: SELECT * FROM Users WHERE ID = "admin' --"; (단순 문자열로 취급 ✅)
```

+++

### Ⅲ. 단계별 방어 전략

- **코드 레벨**: 반드시 **바인드 변수(Parameter Binding)**를 사용하고, MyBatis 등 ORM 프레임워크의 취약한 동적 SQL 사용을 지양합니다.
- **DB 서버 레벨**: 최소 권한 계정(Principle of Least Privilege)을 사용하고, 에러 메시지가 외부로 노출되지 않도록 설정합니다.
- **인프라 레벨**: DB 방화벽(DB Firewall)이나 WAF를 도입하여 실시간으로 인젝션 패턴을 차단합니다.

- **📢 섹션 요약 비유**: SQL 인젝션은 **'택배 주소지에 적힌 가짜 명령'**과 같습니다. 받는 사람 이름 칸에 "이 상자를 열지 말고 경비실에 맡긴 뒤 금고 열쇠를 내어주시오"라고 적는 것과 같습니다. 똑똑한 택배 기사(Prepared Statement)라면 그 글자를 명령이 아닌 단순한 '이름'으로만 보고 무시한 채 배달만 완료하는 것과 같습니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[Parameter Binding]**: SQL 인젝션의 완벽한 기술적 해답.
- **[Stored Procedure]**: 바인드 변수를 쓰지 않으면 SP 내에서도 인젝션이 발생할 수 있으니 주의.
- **[OWASP Top 10]**: 웹 보안 위협 중 항상 최상위에 랭크되는 취약점.

📢 **마무리 요약**: **SQL Injection**은 고전적이지만 여전히 강력한 위협입니다. 입력값을 절대 신뢰하지 않는 **검증과 바인딩의 원칙**만이 데이터를 안전하게 지키는 유일한 길입니다.