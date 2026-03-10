+++
title = "522. 파일 할당 방법 (File Allocation Methods)"
weight = 522
+++

# 522. 프로미스 (Promise)

또 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비동기 작업 결과를 나타내는 객체
> 2. **가치**: 비동기 코드의 가독성과 에러 처리 햕
 3. **융합**: 콜백, async/await, 이벤트 루프와 연관

---

## Ⅰ. 개요

### 개념 정의
**프로미스(Promise)**는 **비동기 작업의 최종 결과(또는 실패)를 나타내는 객체**이다.

### 💡 비유: 피자 배달
프로미스는 **피자 주문 후 배달 추적**과 같다. 주문하면 진행 상황을 확인할 수 있다.

### Promise 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                Promise 생명주기                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【상태 전이】                                                        │
│  ──────────────────                                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │   Pending (대기)                                          │ │   │
│  │   ───▶ 이행(resolve) 또는 거부(reject)                     │ │   │
│  │                                                           │ │   │
│  │   Fulfilled (이행됨)      ──▶ 결과값 전달                   │ │   │
│  │   Rejected (거부됨)     ──▶ 에러 전달                      │ │   │
│  │                                                           │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【주요 메서드】                                                      │
│  ──────────────────                                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  Promise.resolve(value)  // 이행 (성공)                        │ │   │
│  │  Promise.reject(error)  // 거부 (실패)                        │ │   │
│  │  Promise.all([...])     // 모두 완료시 이행                  │ │   │
│  │  Promise.race([...])     // 하나라도 완료되면 이행              │ │   │
│  │  Promise.allSettled([...]) // 모두 완료 (성공/실패)          │ │   │
│  │  .then(onFulfilled, onRejected)                               │ │   │
│  │  .catch(onRejected)                                       │ │   │
│  │  .finally(onFinally)                                      │ │   │
│  │                                                           │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석
### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                Promise 상세                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【생성 패턴】                                                          │
│  ──────────────────                                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  const promise = new Promise((resolve, reject) => {             │ │   │
│  │      // 비동기 작업 시작                                         │ │   │
│  │      asyncOperation((result) => {                              │ │   │
│  │          if (success) {                                       │ │   │
│  │              resolve(result);  // 이행                          │ │   │
│  │          } else {                                             │ │   │
│  │              reject(error);    // 거부                          │ │   │
│  │          }                                                     │ │   │
│  │      });                                                     │ │   │
│  │                                                           │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【체이닝 방식】                                                          │
│  ──────────────────                                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  fetch('api/data.json')                                        │ │   │
│  │    .then(response => response.json())                      │ │   │
│  │    .then(data => processData(data))                     │ │   │
│  │    .catch(error => handleError(error))                  │ │   │
│  │    .finally(() => cleanup());                               │ │   │
│  │                                                           │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【에러 전파】                                                          │
│  ──────────────────                                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  fetch('api/data.json')                                        │ │   │
│  │    .then(response => {                                     │ │   │
│  │        if (!response.ok) {                                  │ │   │
│  │            throw new Error('Invalid response');              │ │   │
│  │        }                                                     │ │   │
│  │        return response.json();                               │ │   │
│  │      })                                                     │ │   │
│  │    .catch(error => {                                   │ │   │
│  │        console.error('Network error:', error);                │ │   │
│  │      });                                                   │ │   │
│  │                                                           │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【async/await 패턴】                                                  │
│  ──────────────────                                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  // 콜백 기반 코드                                  │ │   │
│  │  async function fetchData() {                              │ │   │
│  │      const response = await fetch('api/data.json');              │ │   │
│  │      const data = await response.json();               │ │   │
│  │      return processData(data);                       │ │   │
│  │  }                                                     │ │   │
│  │                                                           │ │   │
│  │  // 동기식처치                                          │ │   │
│  │  try {                                                │ │   │
│  │      const data = await fetchData();                      │ │   │
│  │      console.log(data);                                │ │   │
│  │  } catch (error) {                               │ │   │
│  │      console.error('Error:', error);                  │ │   │
│  │  }                                                     │ │   │
│  │                                                           │ │   │
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
│  【기본 Promise 생성】                                               │
│  ──────────────────                                                │
│  const promise = new Promise((resolve, reject) => {             │
│      setTimeout(() => {                              │
│          resolve('Success!');                         │
│      }, 1000);                                             │
│      reject(new Error('Timeout'));                  │
│  });                                                               │
│                                                                     │
│  【Promise 체이닝】                                                │
│  ──────────────────                                                │
│  promise                                                │
│      .then(value => {                              │
│          console.log('Value:', value);               │
│          return value.toUpperCase();                  │
│      })                                              │
│      .catch(error => {                               │
│          console.error('Error:', error);                │
│      });                                              │
│                                                                     │
│  【Promise.all 예시】                                              │
│  ──────────────────                                                │
│  const promises = [                                  │
│      Promise.resolve(1),                               │
│      Promise.resolve(2),                               │
│      Promise.resolve(3)                               │
│  ];                                                                │
│                                                                     │
│  Promise.all(promises)                              │
│      .then(values => {                             │
│          console.log('All values:', values);            │
│      })                                              │
│      .catch(error => {                               │
│          console.error('Error:', error);               │
│      });                                              │
│                                                                     │
│  【async/await 예시】                                              │
│  ──────────────────                                                │
│  async function fetchUser(id) {                   │
│      const response = await fetch(`/api/users/${id}`);            │
│      if (!response.ok) {                               │
│          throw new Error('User not found');            │
│      }                                                │
│      const data = await response.json();               │
│      return data.name;                               │
│  }                                                │
│                                                                     │
│  async function main() {                                 │
│      try {                                                │
│          const user = await fetchUser(1);                  │
│          console.log('User:', user);                │
│      } catch (error) {                               │
│          console.error('Error:', error);               │
│      }                                                │
│  }                                                │
│                                                                     │
│  【에러 처리 패턴】                                              │
│  ──────────────────                                                │
│  async function fetchWithRetry(url, retries = 3) {          │
│      for (let i = 0; i < retries; i++) {                │
│          try {                                                │
│              const response = await fetch(url);              │
│              return response.json();                 │
│          } catch (error) {                          │
│              if (i < retries) {                           │
│                  await new Promise(r => r => 1000); // 지연               │
│                  return fetchWithRetry(url, retries - 1,                 │
│              }));                                                │
│          }                                                │
│          throw error;                              │
│        }                                              │
│      }                                                │
│  return fetchWithRetry(url, 0, 0); // 재시도 없음
}                                              │
│      .catch(error => {                             │
│          // 모든 재시도 소진 후 에러 throw               │
│          throw error;                              │
│        }                                              │
│    }                                                │
│  }                                                │
│                                                                     │
│  【Node.js Promise API】                                                │
│  ──────────────────                                                │
│  // Promise 생성 (new Promise)                       │
│  // Promise.all([...])                         │
│  // Promise.race([...])                       │
│  // util.promisify()                        │
│  // 기존 콜백 API 지원 (deprecated)               │
│                                                                     │
│  【Python asyncio 예시】                                               │
│  ──────────────────                                                │
│  import asyncio                                                │
│                                                                     │
│  async def fetch_data():                               │
│      await asyncio.sleep(1)  # 비동기 대기               │
│      return await fetch('https://api.example.com/data')             │
│                                                                     │
│  async def main():                                   │
│      data = await fetch_data()                       │
│      print(data)                                │
│                                                                     │
│  asyncio.run(main())                              │
│                                                                     │
│  【에러 처리】                                                │
│  ──────────────────                                                │
│  async def robust_fetch(url):                              │
│      max_retries = 3                               │
│      backoff = 1000                               │
│      for (let i = 0; i < max_retries; i++) {                │
│          try:                                                │
│              await asyncio.sleep(backoff * 1000)  # 지연               │
│              response = await fetch(url)               │
│              return response.json()               │
│          } catch (error) {                           │
│              if (i < max_retries) {                               │
│                  await asyncio.sleep(backoff * 1000 * retry_delay *= 2 * (i + 1));                │
│                  return robust_fetch(url, retries - 1, backoff * 1000);              );
            } else {
              throw error
            }
          }
        } else {
          backoff *= 1
            await asyncio.sleep(1)  # 다음 시도 후 재시도
 })            }
          # Exponential backoff: 실제로는 wait 시간线性增长
            if max_retries <= 0:
              final_error = error
              throw error
            }
        } finally {
      backoff *= 1)   # Reset for next attempt
         │await asyncio.sleep(1000 * retry_delay)
                  ]
        }
      }
    }
  }
}
```

### 👶 어린이를 위한 3줄 비유 설명
**개념**: 프로미스는 "피자 배달 추적" 같아요!
**원리**: 주문하면 진행 상황을 알려요!
**효과**: 비동기적으로 주문을 처리해요!
