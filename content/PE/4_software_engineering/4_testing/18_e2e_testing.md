+++
title = "18. E2E 테스트 (End-to-End Testing)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["E2E-Testing", "End-to-End", "Selenium", "Playwright", "Cypress", "UI-Testing"]
draft = false
+++

# E2E 테스트 (End-to-End Testing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: E2E 테스트는 **"사용자 시나리오 관점에서 **시스템의 **시작부터 끝까지 **전체 흐름을 검증하는 테스트"**로, **UI**, **Backend**, **Database**, **External API**를 **모두 포함**하여 **실제 사용자 경험**을 시뮬레이션한다.
> 2. **가치**: **단위 테스트**, **통합 테스트**에서 발견하지 못한 **시스템 전체 문제**(데이터 일관성, API 연동, 상태 관리, UI/UX 흐름)를 **발견**하고 **Release 전 최종 검증** 수단으로 **필수적**이다.
> 3. **융합**: **Test Pyramid**에서 **최상위**(10%)에 위치하며 **Selenium**(WebDriver), **Playwright**(Chromium 기반), **Cypress**(JavaScript 전용)이 **대표 도구**이고 **CI/CD Pipeline**에서 **Smoke Test**, **Regression Test**로 **자동화**된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
E2E 테스트는 **"애플리케이션의 시작부터 끝까지 사용자 시나리오를 시뮬레이션하는 테스트"**이다.

**E2E 테스트의 범위**:
- **User Interface**: 프론트엔드 동작
- **Business Logic**: 백엔드 처리
- **Database**: 데이터 저장/조회
- **External Service**: API 연동
- **Network**: 네트워크 지연/실패

### 💡 비유
E2E 테스트는 **"실제 주문 테스트"**와 같다.
- **Unit Test**: 부품별 검사
- **Integration Test**: 부품 조립 확인
- **E2E Test**: 실제 주문~배달까지 전체 과정

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         E2E 테스트의 필요성                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

Manual QA:
    • 사람이 수행
    • 시간 오래 걸림
    • 실수 가능
         ↓
Automated Unit/Integration Test:
    • 빠른 피드백
    • 시스템 전체 검증 부족
         ↓
E2E Test:
    • 전체 시나리오 자동화
    • 사용자 경험 검증
    • Release Gate
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### Test Pyramid

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Test Pyramid (Mike Cohn)                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │                                                                                      │
    │                                    /#\                                                │
    │                                   /###\           E2E Test                           │
    │                                  /#####\          (10%)                              │
    │                                 /#######\         • 전체 시스템                       │
    │                                /#########\        • 느림, 깨지기 쉬움                 │
    │                               /###########\                                            │
    │                              /#####   #####\      Integration Test                    │
    │                             /#####     #####\     (20%)                              │
    │                            /#####       #####\    • 컴포넌트 간                       │
    │                           /#####         #####\   • 중간 속도                          │
    │                          /#####           #####\                                       │
    │                         /#####             #####\  Unit Test                          │
    │                        /#####               #####\ (70%)                              │
    │                       /#####                 #####\ • 단일 함수/클래스                   │
    │                      /#####                   #####\• 빠름, 안정적                      │
    │                     /#####                     #####\                                    │
    │                                                                                    │
    │  • 하층: 많고, 빠르고, 안정적                                                           │
    │  • 상층: 적고, 느리고, 깨지기 쉬움                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### E2E 테스트 도구 비교

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         E2E 테스트 도구                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Selenium WebDriver]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 표준적인 E2E 테스트 도구                                                               │
    │  │  • 다중 언어 지원 (Java, Python, JavaScript, C#)                                       │
    │  │  • 다중 브라우저 지원 (Chrome, Firefox, Safari, Edge)                                  │
    │  │  • WebDriver Protocol (W3C 표준)                                                      │
    │  │                                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  // Python 예시                                                                     │  │
    │  │  from selenium import webdriver                                                     │  │
    │  │  from selenium.webdriver.common.by import By                                        │  │
    │  │                                                                                     │  │
    │  │  driver = webdriver.Chrome()                                                        │  │
    │  │  driver.get("https://example.com/login")                                            │  │
    │  │                                                                                     │  │
    │  │  driver.find_element(By.ID, "username").send_keys("user@example.com")                │  │
    │  │  driver.find_element(By.ID, "password").send_keys("password123")                     │  │
    │  │  driver.find_element(By.ID, "login-btn").click()                                    │  │
    │  │                                                                                     │  │
    │  │  assert driver.title == "Dashboard"                                                 │  │
    │  │  driver.quit()                                                                      │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Playwright]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Microsoft 개발 (Chromium 기반)                                                        │
    │  │  • 빠른 실행, 병렬 테스트 지원                                                          │
    │  │  • 자동 대기 (Auto-waiting)                                                           │
    │  │  • Network Interception                                                              │
    │  │                                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  // TypeScript 예시                                                                 │  │
    │  │  import { test, expect } from '@playwright/test';                                   │  │
    │  │                                                                                     │  │
    │  │  test('user can login', async ({ page }) => {                                        │  │
    │  │      await page.goto('https://example.com/login');                                  │  │
    │  │      await page.fill('#username', 'user@example.com');                              │  │
    │  │      await page.fill('#password', 'password123');                                   │  │
    │  │      await page.click('#login-btn');                                                │  │
    │  │      await expect(page).toHaveTitle('Dashboard');                                    │  │
    │  │  });                                                                                │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Cypress]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • JavaScript 전용                                                                      │
    │  │  • 브라우저 내 직접 실행 (Fast)                                                       │
    │  │  • Time Travel Debugging                                                             │
    │  │  • Real-time Reload                                                                  │
    │  │                                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  // JavaScript 예시                                                                 │  │
    │  │  describe('Login', () => {                                                          │  │
    │  │      it('user can login', () => {                                                    │  │
    │  │          cy.visit('/login');                                                         │  │
    │  │          cy.get('#username').type('user@example.com');                               │  │
    │  │          cy.get('#password').type('password123');                                    │  │
    │  │          cy.get('#login-btn').click();                                               │  │
    │  │          cy.title().should('eq', 'Dashboard');                                       │  │
    │  │      });                                                                             │  │
    │  │  });                                                                                │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### E2E 테스트 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         E2E 테스트 아키텍처                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Test Runner (CI/CD)                                                               │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  • Jenkins / GitHub Actions / GitLab CI                                       │  │  │
    │  │  │  • 테스트 스케줄링                                                              │  │  │
    │  │  │  • 결과 리포트                                                                  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                      │                                                   │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Test Environment (Docker/Cloud)                                                  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                      │  │  │
    │  │  │  │ Web Browser │   │ Web Server   │   │ Database     │                      │  │  │
    │  │  │  │ (Chrome/FF)  │   │ (Spring)     │   │ (PostgreSQL) │                      │  │  │
    │  │  │  └──────────────┘   └──────────────┘   └──────────────┘                      │  │  │
    │  │  │                                                                  │  │
    │  │  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                      │  │  │
    │  │  │  │ Mock Server  │   │ Redis        │   │ Message Queue│                      │  │  │
    │  │  │  │ (WireMock)   │   │              │   │ (RabbitMQ)   │                      │  │  │
    │  │  │  └──────────────┘   └──────────────┘   └──────────────┘                      │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 테스트 레벨 비교

| 구분 | Unit | Integration | E2E |
|------|------|-------------|-----|
| **범위** | 단일 함수 | 컴포넌트 간 | 전체 시스템 |
| **속도** | ms | 초 | 분 |
| **비용** | 낮음 | 중간 | 높음 |
| **유지보수** | 쉬움 | 중간 | 어려움 |
| **신뢰성** | 높음 | 중간 | 낮음 (깨지기 쉬움) |

### E2E 테스트 시나리오 예시

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         E2E 테스트 시나리오: 쇼핑몰 주문                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  [시나리오: 로그인된 사용자가 상품을 주문]                                               │
    │                                                                                         │
    │  Given 사용자가 로그인되어 있음                                                          │
    │    • 브라우저 쿠키에 세션 저장                                                            │
    │                                                                                         │
    │  When 상품 목록 페이지에서 "노트북"을 클릭                                                │
    │    • URL 이동: /products → /products/123                                                │
    │                                                                                         │
    │  And "장바구니에 담기" 버튼 클릭                                                          │
    │    • API 호출: POST /api/cart/items                                                     │
    │    • Response 확인: 201 Created                                                         │
    │                                                                                         │
    │  And 장바구니 페이지로 이동                                                              │
    │    • UI 확인: 상품명, 수량, 가격                                                         │
    │                                                                                         │
    │  And "주문하기" 버튼 클릭                                                                │
    │    • API 호출: POST /api/orders                                                         │
    │    • DB 확인: orders 테이블에 레코드 생성                                                │
    │                                                                                         │
    │  Then "주문 완료" 페이지 표시                                                            │
    │    • URL 확인: /orders/456/complete                                                     │
    │    • UI 확인: 주문 번호, 결제 금액                                                        │
    │                                                                                         │
    │  And 이메일로 주문 확인 메일 발송                                                         │
    │    • External API 호출 확인                                                             │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: E2E 테스트 작성
**상황**: 로그인 기능 테스트
**판단**:

```typescript
// Playwright 예시
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
    test.beforeEach(async ({ page }) => {
        // 테스트마다 상태 초기화
        await page.goto('https://example.com');
    });

    test('successful login', async ({ page }) => {
        // Given: 로그인 페이지
        await page.click('text=Login');
        await expect(page).toHaveURL(/.*login/);

        // When: 유효한 자격증명 입력
        await page.fill('[name=email]', 'user@example.com');
        await page.fill('[name=password]', 'SecurePass123!');
        await page.click('button[type="submit"]');

        // Then: 대시보드로 리디렉션
        await expect(page).toHaveURL(/.*dashboard/);
        await expect(page.locator('text=Welcome')).toBeVisible();
    });

    test('login with invalid credentials', async ({ page }) => {
        await page.click('text=Login');
        await page.fill('[name=email]', 'invalid@example.com');
        await page.fill('[name=password]', 'wrongpassword');
        await page.click('button[type="submit"]');

        // 에러 메시지 확인
        await expect(page.locator('.error'))
            .toContainText('Invalid email or password');
    });

    test('login form validation', async ({ page }) => {
        await page.click('text=Login');
        await page.click('button[type="submit"]');

        // 필드별 에러 확인
        await expect(page.locator('[name=email] + .error'))
            .toContainText('Email is required');
        await expect(page.locator('[name=password] + .error'))
            .toContainText('Password is required');
    });
});
```

---

## Ⅴ. 기대효과 및 결론

### E2E 테스트 기대 효과

| 효과 | E2E 없을 시 | E2E 있을 시 |
|------|-----------|-----------|
| **전체 시나리오 검증** | 수동 QA | 자동화 |
| **Release 전 검증** | 불확실 | 확실 |
| **유지보수 비용** | - | 높음 |
| **테스트 시간** | - | 김 |

### E2E 테스트 모범 사례

1. **핵심 경로만 테스트**: Happy Path 중심
2. **불안정한 테스트 피하기**: 네트워크 의존 최소화
3. **테스트 데이터 격리**: 매번 새 데이터
4. **병렬 실행**: 실행 시간 단축
5. **Mock 활용**: External Service 의존 최소화

### 미래 전망

1. **AI Test Generation**: 자동 시나리오 생성
2. **Visual Regression**: UI 비교
3. **Self-healing Tests**: 엘리먼트 변경 자동 복구

### ※ 참고 표준/가이드
- **ISTQB**: E2E Testing
- **Google**: Testing Best Practices
- **Martin Fowler**: Test Pyramid

---

## 📌 관련 개념 맵

- [단위 테스트](./16_unit_testing.md) - 기초
- [통합 테스트](./17_integration_testing.md) - 중계
- [CI/CD](../6_devops/21_ci_cd.md) - 자동화
- [Selenium](../8_tools/22_selenium.md) - 도구
