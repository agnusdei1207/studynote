---
title: "Exception Handling Info Leak Audit"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 253
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 예외 처리(Exception Handling) 미흡으로 인한 정보 노출은 스택 트레이스(Stack Trace), DB 오류 메시지, 서버 경로 등이 공격자에게 직접 노출되는 심각한 취약점이다.
> 2. **가치**: 오류 메시지 하나가 SQL 테이블 구조, 서버 내부 경로, 사용 프레임워크 버전을 노출하여 후속 공격의 발판이 된다.
> 3. **판단 포인트**: 사용자에게 노출되는 오류 메시지는 "일반화된 안내 문구"만 표시하고, 상세 정보는 서버 측 로그에만 기록하는지 확인한다.

---

## Ⅰ. 개요 및 필요성
예외 처리(Exception Handling)의 보안 목표는 두 가지다. 첫째, 시스템 내부 정보를 외부에 노출하지 않는 것. 둘째, 예외 발생 시에도 서비스가 안전하게 지속되는 것이다. 행정안전부 개발보안 가이드의 "오류 메시지를 통한 정보 노출" 항목은 Critical 등급으로 분류되어 있다.

| 노출 정보 유형 | 예시 | 공격자 활용 방법 |
|:---|:---|:---|
| 스택 트레이스 | `NullPointerException at com.app.UserDAO:45` | 패키지 구조, 클래스 명, 라인 번호 파악 |
| DB 오류 메시지 | `Table 'users' doesn't exist` | 테이블명, DB 종류 파악 |
| SQL 구문 노출 | `Syntax error in SQL: SELECT * FROM user WHERE id=` | SQL 인젝션 공격 포인트 확인 |
| 서버 경로 | `/usr/local/tomcat/webapps/app/WEB-INF/` | 파일 업로드 경로 추측 |
| 프레임워크 버전 | `Apache Struts 2.3.5` | 알려진 취약점(CVE) 적용 |

- 개발 환경(`DEBUG` 모드)과 운영 환경(`PRODUCTION` 모드) 설정 미분리
- 전역 예외 처리기(Global Exception Handler) 미구현
- `catch (Exception e) { e.printStackTrace(); }` 패턴 남용

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 오류 메시지를 그대로 노출하는 것은 "고장난 자판기가 내부 회로도를 유리창에 붙여두는 것"이다. 수리 직원만 볼 수 있어야 할 정보가 모든 사람에게 공개된다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+------------------------------------------------------------+
|              예외 처리 2-Channel 아키텍처                    |
|                                                            |
|  예외 발생                                                  |
|       |                                                    |
|       v                                                    |
|  +----------------------------------------------+          |
|  |         전역 예외 처리기 (Global Handler)      |          |
|  |   @ControllerAdvice / web.xml error-page      |          |
|  +--------------------+-------------------------+          |
|                       |                                    |
|           +-----------+--------------+                     |
|           |                          |                     |
|           v                          v                     |
|  +------------------+   +-------------------------+        |
|  |  사용자 응답      |   |  서버 내부 로그           |        |
|  |  (Public)        |   |  (Private)               |        |
|  |                  |   |                          |        |
|  | "서비스 오류가    |   | [ERROR] 2026-04-21       |        |
|  |  발생했습니다.    |   | NullPointerException     |        |
|  |  관리자에게       |   | at UserDAO.java:45       |        |
|  |  문의하세요."     |   | SQL: SELECT * FROM...   |        |
|  |                  |   | Stack: ...               |        |
|  +------------------+   +-------------------------+        |
|    브라우저에 표시           로그 파일/SIEM에만 기록          |
+------------------------------------------------------------+
```

```java
// 취약한 코드 (Bad)
@GetMapping("/user/{id}")
public User getUser(@PathVariable Long id) {
    try {
        return userService.findById(id);
    } catch (Exception e) {
        e.printStackTrace();  // 스택 트레이스가 로그에 노출
        throw e;              // 예외를 그대로 전파 -> HTTP 500 + 스택 트레이스
    }
}

// 안전한 코드 (Good)
@ControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleAll(Exception e) {
        log.error("Unhandled exception", e);  // 서버 로그에만 기록
        return ResponseEntity.status(500)
            .body(new ErrorResponse("서비스 오류가 발생했습니다."));
    }
}
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 전역 예외 처리기는 "병원 접수창구"다. 의사의 진단 내용(상세 오류)은 의무기록실(서버 로그)에 보관되고, 환자(사용자)에게는 "다음에 다시 오세요"라는 안내만 전달한다.

---

## Ⅲ. 비교 및 연결
| 패턴 | 보안성 | 유지보수성 | 감리 판정 |
|:---|:---|:---|:---|
| `e.printStackTrace()` 직접 출력 | ❌ 취약 | △ 개발 중에만 유용 | 지적 필수 |
| HTTP 500 + 스택 트레이스 반환 | ❌ 취약 | △ | 지적 필수 |
| 전역 핸들러 + 일반 메시지 반환 | ✅ 안전 | ✅ | 권장 패턴 |
| 오류 코드 기반 응답 | ✅ 안전 | ✅ 추적 용이 | 권장 패턴 |
| 오류 발생 시 자동 알림(Slack/이메일) | ✅ 안전 | ✅✅ | 우수 사례 |

| 설정 항목 | 개발 환경 | 운영 환경 |
|:---|:---|:---|
| `spring.profiles.active` | `dev` | `prod` |
| `server.error.include-stacktrace` | `always` | `never` |
| `server.error.include-message` | `always` | `never` |
| `logging.level.root` | `DEBUG` | `WARN` |
| `spring.mvc.log-request-details` | `true` | `false` |

```
+-------------------------------------------------------------+
|          개발 vs 운영 오류 응답 차이                          |
|                                                             |
|  [개발 환경 응답]          [운영 환경 응답]                   |
|  {                         {                               |
|    "error": "500",           "error": "서비스 오류",         |
|    "message": "NullPointer", "code": "ERR_500",            |
|    "trace": "at com.app...", "message": "관리자 문의"        |
|    "path": "/api/user/1"   }                               |
|  }                                                          |
|       ^ 공격자에게 노출 금지      ^ 안전한 응답              |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 개발 환경과 운영 환경의 오류 설정 차이는 "연습장과 공연장의 차이"다. 연습 중엔 감독이 큰 소리로 지시를 외치지만, 공연 중엔 관객에게는 들리지 않게 귓속말로만 한다.

---

## Ⅳ. 실무 적용 및 실무자 판단
| 점검 단계 | 점검 방법 | 판정 기준 |
|:---|:---|:---|
| <strong>1단계: 설정 파일 확인</strong> | `application-prod.properties` 검토 | `include-stacktrace=never` |
| **2단계: 고의 오류 유발** | 존재하지 않는 URL 접근, 잘못된 파라미터 전송 | 일반 오류 메시지만 반환 |
| <strong>3단계: SQL 오류 확인</strong> | `' OR '1'='1` 입력 후 응답 확인 | DB 오류 메시지 미노출 |
| **4단계: 소스코드 검색** | `e.printStackTrace()` 패턴 검색 | 운영 코드에서 0건 |
| <strong>5단계: HTTP 헤더 확인</strong> | 응답 헤더의 `Server:`, `X-Powered-By:` 확인 | 서버 정보 미노출 |

HTTP 응답 헤더에서도 서버 정보가 노출될 수 있다.

```
# 취약한 헤더 예시
Server: Apache/2.4.49 (Ubuntu)
X-Powered-By: PHP/7.4.3

# 안전한 설정
Server: (제거 또는 임의값)
X-Powered-By: (제거)
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

로그에 저장되는 상세 정보 또한 보안 관리가 필요하다. 로그에 개인정보(Personal Information), 비밀번호, 세션 토큰이 기록되지 않도록 마스킹(Masking) 처리가 필요하다.

### 판단 체크리스트
1. 위험 시나리오와 점검 범위가 문서로 합의되었는가?
2. 지표·증적·로그가 재현 가능하게 수집되는가?
3. 예외 상황과 오탐·미탐 처리 절차가 있는가?
4. 재시험 또는 후속 조치 기준이 수치로 정의되었는가?

- **📢 섹션 요약 비유**: HTTP 응답 헤더에서 서버 버전을 노출하는 것은 "강도에게 '우리 집 자물쇠는 A사 2018년형'이라고 스티커를 붙여두는 것"이다. 버전 정보만으로도 알려진 취약점을 즉시 찾아낼 수 있다.

---

## Ⅴ. 기대효과 및 결론
예외 처리 정보 노출을 방지하면 공격자가 시스템 구조를 역추적하는 첫 번째 발판을 차단한다. 많은 APT(Advanced Persistent Threat, 지능형 지속 공격) 사례에서 초기 정찰 단계의 핵심 정보는 오류 메시지 분석을 통해 수집되었다. 운영 환경의 오류 응답 일반화와 서버 측 로깅 체계 구축은 최소 비용으로 최대 효과를 얻는 보안 기초 조치다.

감리인은 단순히 코드 패턴 탐색에 그치지 않고, <strong>실제 고의 오류를 유발하여 응답 내용을 확인</strong>하는 블랙박스 테스트를 병행해야 한다.

확장 방향은 ① Policy as Code, ② Continuous Audit, ③ 인공지능(AI, Artificial Intelligence) 기반 이상 탐지와 결합하는 것이다.

- **📢 섹션 요약 비유**: 예외 처리 감리는 "비상구 표시등이 제대로 작동하는지, 하지만 비상구 열쇠 위치는 외부에 공개되지 않는지" 모두를 확인하는 이중 점검이다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | SW 개발보안 43개 항목 | 오류 메시지 정보 노출 포함 |
| 상위 개념 | OWASP A09 - Security Misconfiguration | 오류 설정 미흡 분류 |
| 하위 개념 | 전역 예외 처리기 (Global Exception Handler) | @ControllerAdvice, web.xml |
| 하위 개념 | 스택 트레이스 (Stack Trace) | 내부 코드 구조 노출 정보 |
| 연관 개념 | SIEM (Security Information and Event Management) | 로그 통합 보안 모니터링 |
| 연관 개념 | HTTP 보안 헤더 | Server, X-Powered-By 제거 |

### 📈 관련 키워드 및 발전 흐름도
오류 분류 -> 예외 처리 정보 노출 감리 -> 관측 가능성·보안 로그

### 👶 어린이를 위한 3줄 비유 설명
1. 프로그램이 오류 났을 때 내부 메시지를 그대로 보여주는 건 "넘어진 다음에 엑스레이 사진을 모두에게 보여주는 것"이야.
2. 안전한 오류 처리는 "넘어졌을 때 '잠깐만요'라고만 말하고, 자세한 진단은 의사 선생님(서버 로그)한테만 전달"하는 거야.
3. 해커는 오류 메시지 하나에서 집 열쇠 위치를 알아낼 수 있으니까, 항상 "괜찮아요!"라고만 말하는 연습이 필요해.
