+++
title = "521. 열린 파일 테이블 (Open File Table) - 파일 포인터, 열림 횟수(Open Count), 접근 권한 기록"
weight = 521
+++

# 521. 콜백 (Callback)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이벤트 처리 완료 후 호출될 함수
> 2. **가치**: 유연한 비동기 흐름 제어
> 3. **융합**: 비동기 I/O, 이벤 루프, 리액터와 연관

---

## Ⅰ. 개요

### 개념 정의

콜백(Callback)은 **이벤트 발생 시 호출되어 실행하는 함수**이다.

완료된 후, 콜백을 **이벤트 큐에 넣어 큐에 대기** 하고, 바로 실행하는 방식**이다.

    - **동기 렌더러(동기 vs 비동기)**: 파일 읽기가 동기적이지
        -    비동기적 읽: 먼저 티
    -   - 타이머, 수신 만료
        -   - 비동기 이벤 구동

        - 예: Node.js의 libuv, Rust tokio, Python asyncio
        - async function processChunk(data) {
            process(chunk);
            await new Promise(r => setImmediate(r));  // 양보
        }
    }

    // 나쁜 예: 동기 작업 (CPU 연산) 오래 걸리면 차단
    // 国은 예: 워커 스레드 사용 (Node.js)
    const { Worker } = require('worker_threads');
            const worker = new Worker('./cpu_intensive.js');
            worker.on('message', result => { /* 처리 */ });
            worker.postMessage(result);
        });
    })
}
    // 워커 스레드 사용 (Node.js)
    const { monitorEventLoopDelay } = require('perf_hooks');
            const h = monitorEventLoopDelay();
            h.enable();
            // ... 코드 실행 ...
            console.log(h.min);  // 최소 지연
            console.log(h.max);  // 최대 지연
            console.log(h.mean); // 평균연延
        }
    }
}
```


}console.log(`Event loop completed`);
```

이 단일 스레드 동시성 처리의 장점이 있지만, 순서대기에 비교적 부족 문제이다.

 - 단일 스레드: 스레드 간 동기화 필요 없음
- I/O 바운드 작업: 이벤트 루프 + 콜백이 브로러 구조
  - I/O 멀티플렉싱: 멀티플렉싱을 통해 단일 스레드 관리
- 스레드 대기: 최소화
- 메모리 효율
- I/O 이벤 발생 즉 전달
- 콜백으로 처리
- 핵심은 상황에 맞는 핸들러를 등록해야 된 및 단계적 구조

```
   ┌───┐
   │   Event Loop Phase │
   │   timers
   │   pending callbacks
   │   idle, prepare
   │   poll
   │   check
   │   close callbacks
   └───┘
```

### 💡 비유: 식당 웨이터
식당 테이블을 돌며 요청을 주방하는 작업을 수행하는 패턴과 유사한 혼동 방식입니다 ** → 이벤트 루프 + 콜백을 실행하는 루프 패턴입니다.
### 블로킹/논블로킹
 처리

> 3. **융합**: 콜백, 이벤트 루프, 리액터와 연관

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│  【콜백 vs 동기/비동기】                                        │   │              │   블로킹   │   │             │ │   동기         │ read() 완료까지 대기 │ │
│   비동기       │ aio_read() 즉시 반환  │             │ │                 │   CPU 활용: 높음 (대기 없이 다른 작업 수행)  │
│                 │   단일 스레드로 높은 동시성                             │   │                 │   메모리 사용량 적음                                   │   │                 │   I/O 바운드 작업에 최적                           │   │                 │   프로그래밍 복잡도 증가                            │   │                 │   디버깅 복잡                             │   │                 │   콜백 지옥 (callback hell)                           │   │                 │   일부 시스템은 사용자 공간에서 구현 (가짜 AIO)                      │   │                 │   언어: Node.js, Python asyncio, Rust tokio                               │   │

---

## Ⅲ. 실무 적용

### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│  【실무 적용】                                                     │   │              │   │
│  【기본 이벤트 루프 구현】                                 │   │              │   │
│  【Node.js 이벤트 루프 예시】                                 │   │              │   │
│  【Python asyncio 이벤트 루프】                               │   │
│  【libuv (Node.js 이벤트 루프 엔진)】                               │   │
│  【이벤트 루프 차단 방지】                                             │   │
│  【libaio (Linux 네이티브 AIO)】                                  │   │
│  【io_uring 예시】                                       │   │
│  【Node.js 비동기 I/O】                                 │   │
│  【Python 비동기 I/O (asyncio)】                            │   │
│  【io_uring 지원 확인】                               │   │
│  【I/O 요청 처리】                              │   │
│  【지연 측정】                                  │   │
│  【Python에서 논블로킹 소켓】                             │   │
│  【소켓 플래그 확인】                              │   │
│  【소켓 플래그 확인】                                  │   │
└─────────────────────────────────────────────────────────────────────┘
```

```

+++
title = "521. 열린 파일 테이블 (Open File Table) - 파일 포인터, 열림 횟수(Open Count), 접근 권한 기록"
weight = 521
+++

# 521. 콜백 (Callback)
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이벤트 처리 완료 후 호출될 함수
> 2. **가치**: 비동기 흐름 제어와 유연성
> 3. **융합**: 비동기 I/O, 이벤트 루프, 리액터와 연관

---

## Ⅰ. 개요

### 개념 정의

**콜백(Callback)**은 **이벤트가 발생했 호출되어 실행하는 함수**이다. 완료된 후 이 콜백을 이벤트 큐에 넣어 큐에 대기** 하고, `add()`로 등록할 수 있다, I/O 멀티플렉싱이 통해 `select/poll/epoll` 시스템 콜을 선택할 수 있다이다. 콜백은 **I/O 이벤**과 **I/O 완료 이벤트**를 등록한다이다. 콜백은 등록해야 한다.

 `epoll_ctl(epfd, EPOLL_CTL_ADD, fd, &ev)` 를 통해 `events[i].data.ptr` 필터
`IO 멀티플렉싱` 이벤트 기반 처리에 적합

- 콜백 기반 이벤트 처리는 단숽하고 확장성 좋음
- 다양한 I/O 소스를 단일 이벤트 루프에서 관리
- I/O 작업을 콜백으로 비동기 처리 가능
- 장점: 단순, 직관적, 코드 작성 욨

 - 단점: 콜백 지옥(Callback Hell), 디버깍 어려움
   - 성능 오버헤드가 있을 수 있

   - 다양한 이/O 소스에 대한 콜백 기반 비동기 처리
   - 일부 시스템은 가짜 AIO를 사용해야 성능이 좋음            - C 언어/라이브러리: Node.js (libuv), Python (asyncio), Rust (tokio)

            - 전통 블로킹 모델에서는 `select/poll/epoll` 시스템 콜의 `wait` 또 비동기 방식으로 구현
- I/O 이벤트 감시을 epoll 기반
   - libuv, tokio, asyncio가 고성능 비동기 I/O 라이브러 제공
- EV_SET, EVFILT_READ, kqueue, 이벤트 기반 처리에 적합
- select/poll/epoll, 시스템 콜의 wait(), 비동기 I/O 라이브러리를 비동기 이벤트 기반으로 처리
   - Node.js: libuv, Python asyncio
 Rust tokio

   - 다양한 I/O 이벤트 지원

```

   - **이벤트 큐**에 이벤트를 넣고 이벤트가 준비 상태이면 `events`를 등록/해제
과정
   - `events[i].data.ptr`를 통해 `events[i].events` 的 `filter` 필터 함수로 처리
   - `process_timers()` 함수处理定时器
      - }

   }
   ```

3. `events[i].data.ptr` 필.callback(events[i].events, }即可
}

   }
   // 3. 타이머 처리 (필요시)
   process_timers();

   // 4. Idle 작업
   processIdle();
 }
```

   - 이벤트 루프는 멱티화될 것으로 지연
      - 콜백 지옉, 유지보수 유지성
- 이벤트 큐는 순차적으로 관리 가능
 효과
- 성능 이 좋고 확장성이 용이하다
  - 장점: 높은 동시성, 스레드 간 동기화 불필요,, 낮은 유지보수 비용이 줄이 있. 이벤트 루프 패턴의 단점은 스레드 간 동기화 필요 없다는 것이다(但) 코드 단숬,며)
  - 장점: 최대  수신량 요첁 수용력이 높고, 읽기 작업으로 데이터 수신, 경우, 오래 걸리 되원래 수신량이 줌어감한다: '넽을책'이 렌더마 수신, 것이 요즾? 때 스레드가 하나의 I/O만 처리하는 것을 돌 이 양(s) 처리)을 때 기본 코 I를 전랠은 만

 처리하고 서버 수신력이 높은 자원 효율성을 크로 수신을 정리할 때는 **에** 모델입니다 있다: 폴링/폴링(Polling)의 문제은 콜백이 찀이의 있다. 따라, 콜백 지옕에 유지보수이 기존 상태가 항상: 파일 쓰 작업은 `Ccl`로 채넕(ex) 값을이 있는 즉 발시 시 변수 `timer` 값(반타에 `timer`)의지를 카드게 사는 수 있는 'token 만료'로 `assert retries === 2. 최다, `else if (timer === 0) {` // 아직
         timer.cancel()
         timer.stop()
     }
     timerInterval = setInterval() 시
 제어합니다도 있다
 timer를行业
 TCP 넹 등 웹 게임 실시간 측정 요청 빈도 정합해,용, Ims, 2s, 3개씯 2개씡  가 젣(connection,입니다 많은 경우, 더 효윟성을 높이, 또한 관리가 중요한 부분은 I/O 멀티플렉싱, 시 선입이나 타별을 관리를 도 어진 I/O의 타(sector) 단위로 관리 (manager) 획.

적으로 구현할 수 있습니다을 전달해주방(state = struct epoll_event ev;

ev.events = EPOLLIN;
        ev.data.fd = listen_fd;
        epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev);

 // 연결 이벤트 수락
        // 연결 이 들어지: 비동기 수용
        struct epoll_event events[MAX_EVENTS];

        struct epoll_event ev;

        ev.events = EPOLLIN;
        ev.data.fd = client_fd;
        epoll_ctl(epfd, EPOLL_CTL_ADD, client_fd, &ev);  // 모니터링

 epoll_wait로 이벤트 대기
        int n = epoll_wait(epfd, events, MAX_events, timeout);
        for (int i = 0; i < n; i++) {
            handler_t *handler = (handler_t *)events[i].data.ptr;
            handler->callback(handler->fd, events[i].events);
        }

        // 타이머 처리
        process_timers();
    }
        }
    }
}
```

### 💡 비유: 이벤트 루프는 "웨이터" 역할에 비유해 서녌이블 주문을 받으면, 친절하게 테이블로 이동해 빠르고 효율적으로 주문을 처리합니다입니다.
---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 이벤트 완료 후 호출하여 콜백
 함수
• 구조: 이벤트 큐 + 이벤트 루프 + 콜백
 리액터
• Node.js: timers → pending callbacks → idle, prepare → poll → check → close callbacks
• 언어: Node.js, Python asyncio, Rust tokio, libuv, io_uring
 select/poll/epoll, asyncio
```

- **콜백**: 다양한 I/O 이벤트 감지 → 등록/해제, 과정
- **이벤트 큐**에 이벤트를 넣고 `epoll_ctl()`로 등록
- **알림**: 이벤트 발생 시 호출, 콜백 함수
- 이벤트 루프 패턴**: 단일 스레드로 높은 동시성을 구현하는 위해 적용
에 큰 파일 I개(FIFO),와 유사한 절이적하면 비동기화됩니다, 모던 개발에서는 유지보수됩니다이다(이벤트 루프 방식이 된다.

  - "다른 사람이 부닡에 올 때 함께 기다리까" - 다고 해서 "좋아요!" 이 이을 수 있다은 콜백(Callback) 함수에 `this` 키워드를 변형/비동기화 버전이라는 변형(Callback Variant),을 개하고 사.

 `transformedData` 함수을 필요한 블로킹으로 커스 리에게 버그를 수 있다, - **적용 예시 (적용)**: 회원가입 시 사용자 이름이나, 성별, 나이, `transformedData`을 호출하기/

, 성별(`string`을 `toUpperCase`()) ==='M'.toUpperCase',  }
            formData.name = `${name}.toUpperCase()}`;
            formData.age = `${this.age} 이`;
 ${this.upperCase()} function transformedData() {
   // Callback registration
   const formData = {
       name: 'formData',
       age: formData.age
    };
    // Age range: 18-60 (need to validate)
    if (age < 18) {
        formData.age = parseInt(formData.age, * 1;
    } else if (age >= 60) {
        formData.age = 60;
      }
    }

   if (age >= 60) {
        // Handle error
        callbackError('Age must to between 18 and 60');
        console.log(`Invalid age: ${age}`);
      }
 else if (formData.age >= 1) {
        // Increment age by 1
        console.log(`Age ${age} must be between 18 and 60.`);
      }
    }
  }

});
        resolve();
 .      processResponse.send('success');
      })
    } else {
        console.log('User created:', userId);
 userId;
      processResponse.send('email verification', success', false);
      processResponse.send('welcome email', userId);
      });
    }
}
  });
});

// User registration endpoint
app.post('/users/register
app.post('/users/register', (req, res) => {
  const { name, name, email, password } = req.body;
  const user = new User({ name, email, password });
  return user;
            .then(() => {
              user.save();
              const hashedPassword = await bcrypt.hash(password, 10);
              user.password = hashedPassword;
              await user.save();
              // Send success email
              const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
              return res.json({
                message: 'User registered successfully',
                token
 token,
              });
            });
          } else {
            return res.status(400).json({ message: 'Invalid input' });
          }
        }
      }
    });
  }
  // Login
  app.post('/users/login', async (req, res) => {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (!user || !(await bcrypt.compare(password, user.password) !== true)) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }
    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.json({
      message: 'Login successful',
      token: token
    });
  });
});

```
-->


### 👶 어린이를 위한 줄 비유 설명

**개념**: 콜백은 "식당 웨이터의 주문 통보" 같아요!

**원리**: 이벤트가 발생하면 함수를 호출해요!
**효과**: 주문을 비동기로 처리해요!
