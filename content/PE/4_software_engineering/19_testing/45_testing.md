+++
title = "45. 소프트웨어 테스트 (Software Testing)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Testing", "TDD", "Unit-Testing", "Integration-Testing", "E2E-Testing"]
draft = false
+++

# 소프트웨어 테스트 (Software Testing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 테스트는 **"소프트웨어**가 **요구사항**을 **만족**하는 **것**을 **검증**하는 **활동\\\"**으로, **Unit **Test**(단위 **테스트)**, **Integration **Test**(통합 **테스트)**, **E2E **Test**(종단 **간 **테스트)**, **System **Test**(시스템 **테스트)**가 **있다.
> 2. **테스트 수준**: **Unit **Test**가 **함수/클래스**를 **테스트**하고 **Integration **Test**가 **모듈 **간 **상호작용**을 **테스트**하며 **E2E **Test**가 **전체 **시스템**을 **테스트**한다.
> 3. **TDD**(Test-**Driven **Development)**는 **Red**(실패 **하는 **테스트)** → **Green**(통과 **하는 **코드)** → **Refactor**(개선)**의 **사이클**로 **개발**하고 **Coverage**(테스트 **커버리지)**를 **측정**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
소프트웨어 테스트는 **"품질 보증 활동"**이다.

**테스트 피라미드**:
| 수준 | 범위 | 속도 | 비용 | 개수 |
|------|------|------|------|------|
| **E2E** | 전체 시스템 | 느림 | 높음 | 적음 |
| **Integration** | 모듈 간 | 중간 | 중간 | 중간 |
| **Unit** | 함수/클래스 | 빠름 | 낮음 | 많음 |

### 💡 비유
테스트는 ****건물 **검사 ****와 같다.
- **재료**: Unit Test
- **조립**: Integration Test
- **완성**: E2E Test

---

## Ⅱ. 아키텍처 및 핵심 원리

### 테스트 피라미드

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Test Pyramid                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ▲                                                                                      │  │
    │  │                     ┌────────────────────────────────────────────┐                    │  │
    │  │ E2E Tests (10%)    │  • UI/UX flows                               │                    │  │
    │  │  (Slow, Expensive) │  • Critical user journeys                   │                    │  │
    │  │                     │  • API integration                          │                    │  │
    │  │                     └────────────────────────────────────────────┘                    │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │ Integration Tests (20%)   │  • Module interactions                                    │  │  │
    │  │  (Medium Speed)            │  • Database access                                       │  │  │
    │  │                           │  • External services                                     │  │  │
    │  │                           └───────────────────────────────────────────────────────────┘  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │ Unit Tests (70%)         │  • Functions, classes                                    │  │  │
    │  │  (Fast, Cheap)             │  • Business logic                                        │  │  │
    │  │                           │  • Edge cases                                            │  │  │
    │  │                           └───────────────────────────────────────────────────────────┘  │  │
    │  │                                                                                       │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────────►  │
    │     Speed: Fast → Slow    Cost: Low → High    Feedback: Quick → Slow                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Unit Testing

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Unit Testing (Example: Calculator)                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Code Under Test:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // calculator.ts                                                                        │  │
    │  export class Calculator {                                                               │  │
    │      add(a: number, b: number): number {                                                 │  │
    │          return a + b;                                                                   │  │
    │      }                                                                                   │  │
    │                                                                                          │  │
    │      divide(a: number, b: number): number {                                              │  │
    │          if (b === 0) {                                                                  │  │
    │              throw new Error("Division by zero");                                        │  │
    │          }                                                                               │  │
    │          return a / b;                                                                   │  │
    │      }                                                                                   │  │
    │  }                                                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Unit Tests:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // calculator.test.ts                                                                   │  │
    │  import { Calculator } from './calculator';                                              │  │
    │                                                                                          │  │
    │  describe('Calculator', () => {                                                          │  │
    │      let calc: Calculator;                                                               │  │
    │                                                                                          │  │
    │      beforeEach(() => {                                                                  │  │
    │          calc = new Calculator();                                                        │  │
    │      });                                                                                 │  │
    │                                                                                          │  │
    │      describe('add', () => {                                                             │  │
    │          it('should add two positive numbers', () => {                                    │  │
    │              expect(calc.add(2, 3)).toBe(5);                                             │  │
    │          });                                                                             │  │
    │                                                                                          │  │
    │          it('should add negative numbers', () => {                                       │  │
    │              expect(calc.add(-2, -3)).toBe(-5);                                          │  │
    │          });                                                                             │  │
    │                                                                                          │  │
    │          it('should handle zero', () => {                                                │  │
    │              expect(calc.add(5, 0)).toBe(5);                                             │  │
    │              expect(calc.add(0, 5)).toBe(5);                                             │  │
    │          });                                                                             │  │
    │      });                                                                                 │  │
    │                                                                                          │  │
    │      describe('divide', () => {                                                          │  │
    │          it('should divide numbers', () => {                                              │  │
    │              expect(calc.divide(10, 2)).toBe(5);                                          │  │
    │          });                                                                             │  │
    │                                                                                          │  │
    │          it('should throw error when dividing by zero', () => {                            │  │
    │              expect(() => calc.divide(10, 0)).toThrow("Division by zero");                │  │
    │          });                                                                             │  │
    │      });                                                                                 │  │
    │  });                                                                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Integration Testing

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Integration Testing (API + Database)                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Scenario: Create User via API, Save to Database
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // user.integration.test.ts                                                            │  │
    │  import request from 'supertest';                                                        │  │
    │  import { app } from '../app';                                                            │  │
    │  import { Database } from '../database';                                                  │  │
    │                                                                                          │  │
    │  describe('User API Integration', () => {                                                │  │
    │          let db: Database;                                                                │  │
    │                                                                                          │  │
    │          beforeAll(async () => {                                                          │  │
    │              db = new Database();                                                         │  │
    │              await db.migrate();                                                          │  │
    │          });                                                                             │  │
    │                                                                                          │  │
    │          afterEach(async () => {                                                          │  │
    │              await db.cleanup();                                                          │  │
    │          });                                                                             │  │
    │                                                                                          │  │
    │          afterAll(async () => {                                                           │  │
    │              await db.close();                                                            │  │
    │          });                                                                             │  │
    │                                                                                          │  │
    │          it('should create user via API and save to database', async () => {                │  │
    │              const response = await request(app)                                          │  │
    │                  .post('/api/users')                                                      │  │
    │                  .send({                                                                  │  │
    │                      name: 'John Doe',                                                    │  │
    │                      email: 'john@example.com'                                            │  │
    │                  });                                                                      │  │
    │                                                                                          │  │
    │              expect(response.status).toBe(201);                                           │  │
    │              expect(response.body).toHaveProperty('id');                                  │  │
    │              expect(response.body.name).toBe('John Doe');                                  │  │
    │                                                                                          │  │
    │              // Verify in database                                                        │  │
    │              const user = await db.users.findById(response.body.id);                       │  │
    │              expect(user).not.toBeNull();                                                 │  │
    │              expect(user.email).toBe('john@example.com');                                  │  │
    │          });                                                                             │  │
    │  });                                                                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### E2E Testing

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         E2E Testing (Playwright)                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Scenario: User Login Flow
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // login.spec.ts (Playwright)                                                          │  │
    │  import { test, expect } from '@playwright/test';                                        │  │
    │                                                                                          │  │
    │  test.describe('Authentication', () => {                                                 │  │
    │          test('should login user with valid credentials', async ({ page }) => {             │  │
    │              // Navigate to login page                                                    │  │
    │              await page.goto('/login');                                                   │  │
    │              await expect(page).toHaveTitle('Login');                                     │  │
    │                                                                                          │  │
    │              // Fill login form                                                          │  │
    │              await page.fill('[name="email"]', 'user@example.com');                       │  │
    │              await page.fill('[name="password"]', 'password123');                         │  │
    │                                                                                          │  │
    │              // Submit form                                                               │  │
    │              await page.click('[type="submit"]');                                         │  │
    │                                                                                          │  │
    │              // Verify login success                                                      │  │
    │              await expect(page).toHaveURL('/dashboard');                                  │  │
    │              await expect(page.locator('h1')).toContainText('Welcome');                    │  │
    │          });                                                                             │  │
    │                                                                                          │  │
    │          test('should show error with invalid credentials', async ({ page }) => {            │  │
    │              await page.goto('/login');                                                   │  │
    │              await page.fill('[name="email"]', 'user@example.com');                       │  │
    │              await page.fill('[name="password"]', 'wrongpassword');                       │  │
    │              await page.click('[type="submit"]');                                         │  │
    │                                                                                          │  │
    │              // Verify error message                                                      │  │
    │              await expect(page.locator('.error')).toHaveText('Invalid credentials');       │  │
    │              await expect(page).toHaveURL('/login');  // Still on login page              │  │
    │          });                                                                             │  │
    │  });                                                                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 테스트 전략 비교

| 전략 | 목적 | 도구 | 실행 시간 | 피드백 |
|------|------|------|-----------|--------|
| **Unit** | 버그 조기 발견 | Jest, JUnit | 초-분 | 빠름 |
| **Integration** | 모듈 간 상호작용 | Supertest, Testcontainers | 분-시간 | 중간 |
| **E2E** | 사용자 시나리오 | Playwright, Cypress | 분-시간 | 느림 |

### TDD Cycle (Red-Green-Refactor)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         TDD Cycle (Red-Green-Refactor)                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Example: Implement FizzBuzz
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Step 1: Red (Write failing test)                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  test('should return "Fizz" for multiples of 3', () => {                              │  │  │
    │  │      expect(fizzBuzz(3)).toBe("Fizz");                                                │  │  │
    │  │  });                                                                                  │  │  │
    │  │  → Test fails (function not implemented)                                              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                               │  │
    │            ▼                                                                               │  │
    │  Step 2: Green (Write minimal code to pass)                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  function fizzBuzz(n: number): string {                                               │  │  │
    │  │      if (n % 3 === 0) return "Fizz";                                                  │  │  │
    │  │      return n.toString();                                                             │  │  │
    │  │  }                                                                                    │  │  │
    │  │  → Test passes                                                                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                               │  │
    │            ▼                                                                               │  │
    │  Step 3: Refactor (Improve code)                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  function fizzBuzz(n: number): string {                                               │  │  │
    │  │      const isMultipleOf3 = n % 3 === 0;                                               │  │  │
    │  │      const isMultipleOf5 = n % 5 === 0;                                               │  │  │
    │  │                                                                                       │  │  │
    │  │      if (isMultipleOf3 && isMultipleOf5) return "FizzBuzz";                            │  │  │
    │  │      if (isMultipleOf3) return "Fizz";                                                │  │  │
    │  │      if (isMultipleOf5) return "Buzz";                                                │  │  │
    │  │      return n.toString();                                                             │  │  │
    │  │  }                                                                                    │  │  │
    │  │  → All tests still pass, code improved                                               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                               │  │
    │            ▼ Repeat for next test case...                                                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Test Coverage

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Test Coverage Metrics                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Coverage Types:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Metric      │  Definition                                                                 │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  │  Line        │  Percentage of code lines executed                                       │  │
    │  │  Branch      │  Percentage of conditional branches taken (if/else)                      │  │
    │  │  Function    │  Percentage of functions called                                           │  │
    │  │  Statement   │  Percentage of statements executed                                        │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Coverage Report (Istanbul/nyc):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  File           │  Statements │  Branch │  Functions │  Lines  │                      │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  │  calculator.ts  │  100% (6/6) │  100% (2/2) │  100% (2/2) │  100% (6/6)  │            │  │
    │  │  user.ts        │   80% (8/10)│   75% (3/4) │   50% (1/2) │   80% (8/10) │            │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  │  Total          │   85%        │   80%       │   60%       │   85%                    │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → Target: >80% statement coverage (typical threshold)                                   │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 마이크로서비스 테스트 전략
**상황**: 10개 서비스, 컨테이너화, CI/CD
**판단**: Unit + Integration + Contract Tests

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Microservices Testing Strategy                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Testing Strategy:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Unit Tests (Fast, Local)                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Framework: Jest                                                                    │  │  │
    │  │  • Scope: Business logic, validators, utilities                                      │  │  │
    │  │  • Execution: < 1 minute per service                                                 │  │  │
    │  │  • Target: >80% coverage                                                             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  2. Integration Tests (Medium, Testcontainers)                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Framework: Supertest + Testcontainers (PostgreSQL, Redis)                         │  │  │
    │  │  • Scope: API endpoints, database access                                             │  │  │
    │  │  • Execution: < 5 minutes per service                                                │  │  │
    │  │  • Isolation: Each test uses fresh container                                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  3. Contract Tests (Consumer-Driven)                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Framework: Pact                                                                    │  │  │
    │  │  • Process:                                                                          │  │  │
    │  │  │  1. Consumer (Frontend) writes contract (expectations)                            │  │  │
    │  │  │  2. Consumer publishes contract to Pact Broker                                     │  │  │
    │  │  │  3. Provider (Backend) verifies contract                                          │  │  │
    │  │  │  4. Contract fails if API changes break expectations                              │  │  │
    │  │  → Catches breaking changes early                                                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  4. E2E Tests (Slow, Critical Paths Only)                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Framework: Playwright                                                              │  │  │
    │  │  • Scope: Critical user journeys (login, checkout, payment)                           │  │  │
    │  │  • Execution: < 15 minutes (whole suite)                                              │  │  │
    │  │  • Environment: Staging (not production)                                              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 테스트 기대 효과

| 테스트 유형 | 버그 발견률 | 수정 비용 | 실행 빈도 |
|-------------|------------|-----------|-----------|
| **Unit** | 70-80% | 낮음 | Every commit |
| **Integration** | 15-20% | 중간 | Every PR |
| **E2E** | 5-10% | 높음 | Daily |

### 모범 사례

1. **TDD**: Red-Green-Refactor
2. **Isolation**: 독립적 테스트
3. **Fast**: 초 단위 실행
4. **Maintainable**: 명확한 이름

### 미래 전망

1. **AI Testing**: 테스트 자동 생성
2. **Chaos Engineering**: 장애 주입
3. **Visual Testing**: UI 회귀
4. **Property-Based**: QuickCheck

### ※ 참고 표준/가이드
- **ISTQB**: Test Certification
- **IEEE**: 829 Standard
- **Google**: Testing Blog

---

## 📌 관련 개념 맵

- [CI/CD](./18_cicd/44_cicd.md) - 파이프라인
- [리팩토링](./16_refactoring/42_refactoring.md) - 코드 개선
- [코드 리뷰](./15_code_review/41_code_review.md) - 품질
