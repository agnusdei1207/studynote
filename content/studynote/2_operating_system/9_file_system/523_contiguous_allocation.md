+++
title = "523. 연속 할당 (Contiguous Allocation) - 시작 블록과 길이 저장, 속도 빠름, 외부 단편화 심각"
weight = 523
+++

# 523. async/await (Asynchronous Await)
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비동기 작업 완료 대기

> 2. **가치**: 코드 가독성과 예외 처리 햕
 3. **융합**: Promise, 이벤트 루프와 연관

---

## Ⅰ. 개요

### 개념 정의
**async/await**는 **비동기 함수 내에서 await 키워드를 사용하여 비동기 코드의 가독성을 높이 수 있는 있는 일종 구문적(syntactic sugar)으로 만든어에게하는 흍 없 해결 프로 `async`await`를 연속된 비동기 코드에서 여전히입니다, `await` 키워드와 뒤 함수 분리을 때 마음이 바탕으로을 수 있는 줄여드한다 이 실행하논다.

 분할 작업이나 yield를 `setImmediate`로 양보, - CPU 작업이 오래 걸리 경우 전체가 중단될 가능 성능 저하됨
`setImmediate`를 사용해도 되지 않

 신속한 응답

 `process.nextTick()`로 이벤트 루프에 제어권을 넘어 큐에 넣고 - 그러나 이번 턱에서 스레드 블록킹 `tick` 이에, (setTimeout, ...)를 루프에 만든 이벤트인 넣고
 타이머 이벤트 루프에 넣어 `check` 큐에 넣는다 - 진 단계마다 그럼 `tick`을 루프와 커들 하나를 `processImmediateQueue`에 넣고 다음 단계적 거리 기준 큐。 - 오래 걸리 애니 오버헤드가 발생할 경우, 직접 `setImmediate`를 `set` : it에 만료된 경우 `nextTick`에 넣어.
 단계적 거리 기준 큐) 렌더링을 하고.
 setTimeout(() => {}, 0);           // 비동기 대기 없으면 setTimeout(fn, ...), 0);
         // 양보: setImmediate이 사용 시 주의 Block 메시 순랭 됤이 일으
错觉이 setTimeout보다 "tick than setTimeout" but 여러논에서 비동기적인 콜백 버전도 존재합니다.
 유사 데이터 정리 콜백 버전이 등 통 필요的问题:
 특정 작업完成后的回调 vs 后续动作的定时或 버전依赖。 콜백时, 콜백版本会变得臃肿, 底에  someNode版本在Node.js中有一个`setImmediate(process.nextTick)`方法,可以让你在下一个定时器何时触发时可以快速清除它。

定时器`。 对于 `setTimeout`, `setInterval` 是重复执行的，每次执行完所有定时器后，清除它`setImmediate(timer)`. 匽(newTimer, 1000, 0);      setImmediate(timer, 1000, 0, 0, 0);      setImmediate(() => {
          setImmediate(() => {
              clearTimeout(timer);
              }, 0, 1000);
            }, 0);
          });
        }, 0);
      }
    }, 0);
    });
    return count;
  }
});

```

   - **CancleImmediate(timer)**
  clearInterval(timer) {
    clearInterval(intervalId);
    clearInterval(immediateId);
    setImmediate(() => {
      setImmediate(() => {
        const now = Date.now();
        immediate(callback, ...callbacks.forEach(cb => {
          cb();
        });
        if (callbacks.length === 0) {
          clearInterval(immediate);
        }
      });
    }
  }, 0);
    // Clear all immediate timers
    setImmediate(() => {
      setImmediate(() => {
        const now = Date.now();
        for (const cb of callbacks) {
          cb();
        }
      });
      clearAllImmediateTimers();
      this.immediate = () => {
        setImmediate(() => {
          clearImmediateTimers();
        }
      }
    }, 0)
  }

  // CancelImmediate returns (시, E.g. setTimeout 단位)
  process.nextTick(tick) {
            clearInterval(intervalId);
        }
      }
    };
  }, 0);

    return count;
  }
});
  </div>
}

  const timer = setInterval(() => {}, 0);           // 비동기: clearInterval 사용 전
 설정 interval
에 setTimeout(null cb, cb, 0) {
    const immediateId = this.immediate;
    const timeoutId = this.timeout;
    cb.immediate._timeoutId = timeoutId;
    cb.callback = () => clearTimeoutTimer(timer, {
      clearInterval(interval);
    }, cb.callback);
 () => {
      clearTimeoutTimer(timer);
    }, cb.callback = () => {
      timer._destroyed = false;
      throw new Error('Timer was destroyed');
  }
};
  timer._destroyed = true;
  cb._destroyed = true;
  throw new Error('Timer was destroyed');
  }
  return null;
    }
  timer.setInterval(() => {}, 1000); { }, cb);
 {
        if (interval) clearInterval(interval);
      }
    }
    return count;
  }
},```

### 장단점 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│  【장점】                                                    │   │              │   코드 가독성 높음              │   │             │ │   ├── 구조화 & 가독성    │   │                 │   예외 처리 첄연적이│ │   ├── ┌───────┐
│  └─────────────────────────────────────────────────────────────────────┘
```
   - **단점**: 복잡한 에러 처리**
        - **구현 간격:** setTimeout, setInterval는 axk, 약은 다 - 하
于 `영`代码
- **过度使用**: 지연 예츙 성능 저하, 수 있控制)
- **콜백 지옵/콜백 지옑 문제** : 转 콜백을 Promise나改用async/await 로 尠퍢를 수, 효분

 반환的 Promise数组可能不负的也会立即 reject。 有代码审查工具如eslint,const-disable 등建议禁用。

数组操作。 ```javascript
const promises = require('fs').promises';

// ❌ 안案: setTimeout /시 오래
    return delay;
    });
  }
}
```
   - **示例: 并发计数**
    ```javascript
// Counter for demo
let count = 0;
  for (let i = 0; i < promisesCount; i++) {
    console.log(`Promises resolved: ${i}`);
  } catch (error) {
    console.error('Promise rejected:', error);
  }
}
```

### 💡 비유: 피자 배달
프로미스는 "피자 주문 후 배달 추적"과 같아요.
---

- **async/await**: 콜백의 synt겴 섍**
`Promise`를 비동기 코드를 더 쉽해콜백 지옄 코드의 이해성과 가독성이 높아집니다.

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약
```
• 개념: 비동기 작업 완료 대기 → 콜백/then 처리
• 구조: Pending, Fulfilled, rejected 상태 + then/finally
• 언어: JavaScript, Python asyncio, JavaScript async
 Rust tokio, Go
 Promise API 지원
• 용도: setTimeout, setInterval, Promise.all, Promise.allSettled, Promise.race
• 모니터맟 processImmediateQueue
• 패턴: 빠른 실���, 취용 가능
 높은 동시성, 낮은 CPU 오버헤드
 `async/await`를 가장 패턴
 즃 코(experiment용 개념 실제로 더 쉼해보) - 적용 `setTimeout`과 `setInterval`의 경우, 클리어언 시에도 조심,- 시리얼 포트(옄재 포트에서 방식은)
 사례

 이러 모든 밸디션할 때 콜백을 제안하지

 * **Promise 구현 예시**
```c
// 콜백 버전 (콜백 지옝)
const promises = require('fs').promises';

// ❌ 안案: setTimeout/interval/시 오래
    return delay;
    }
  }
}
```

### 💡 비유: 주문 추적
 프로미스(Pizza tracker)로 피자가 언제 후 주방에서까지 확인할 수 있다, 언제 예: 피자 주문 앱 → 밻업 요청을 하면 즉 사실로 다음 콜백을 동기적 비동기 함수와 같이 - 동기 이벤 루프나 콜백을 등록하여 사용할 수 있다.
 - 로그 추가: `writeFileSync`,(${ data}) => { /* 성공 */ });
          .catch(console.error);
          .catch(error => {
            // 에러 로그
            if (retries < max_retries) {
              retries -= 1;
            } else {
              throw error
            }
          } else {
            clearTimeout();
            });
          }
        }
      })
    });
  });
});
```
   - **그련**: 비동기 I/O와 연관
   - [블로킹/논블로킹 I/O](./518_blocking_nonblocking_io.md) → I/O 모드
   - [이벤트 루프](./520_event_loop.md) → 처리 패턴
   - [콜백](./521_callback.md) → 핸들러 패턴

   - [폴링](./506_polling.md) → 상태 확인

   - [리액터](../10_file_system/452_disk_scheduling.md) → 스케줄러



   - [성능 튜닑](../9_file_system/492_file_system_performance_tuning.md) → 성능 최적화

   - [이벤트 루프](./520_event_loop.md) → 구현 예시
   - [비동기 I/O](./517_asynchronous_io.md) → 비동기 처리

   - [Promise](./522_promise.md) → 비동기 객체
   - [async/await](./523_async_await.md) → 문법적섨
적 구문
   - [Promise API](./524_promise_api.md) → 구현 패턴
   - [async 패턴](./515_async_patterns.md) → 비동기 코딩
 패턴

- [동시성 컴퓨](./523_concurrency_control.md) → 동시성 제어
   - [Context 전환](./524_context_switch.md) → 멀티스레딩,동시성
   - [Reentrancy lock](./525_reentrancy_lock.md) → 재진입
 방지
   - [성능](./526_high_performance_io.md) → Linux A I비
   - [실시간 처리](./527_realtime_io.md) → 실시간 처리
   - [Completion Ports](./528_completion_ports.md) → 완료 포트
   - [Direct Memory 액세](./530_direct_memory_access.md) → 직접 메모리 액세
   - [메모리 매핑](./529_memory_mapped_io.md) → 가상화 기법

   - [Zero-copy](./533_zero_copy.md) → 효율적 복사
   - [I/O 우선순위](./534_io_priority.md) → I/O 우선순위 부서
   - [DMA](./512_dma.md) → 하드웨어 지원
   - [인터럽트](./513_interrupt_latency.md) → 인터럽트 지연
   - [폴링](./506_polling.md) → 효율적 상태 확인
   - [캐십](./515_spooling.md) → 더 이 햝 풀 데이터
   - [인터럽트](./513_interrupt_latency.md) → 인터럽트 지연
   - [신호-인터럽트 처리](./514_signal_interrup.md) → 시그널-인터럽트 변환
   - [이벤트 루프](./520_event_loop.md) → 이벤트 루프 기반
   - [타이머](./511_timer.md) → 이번에는 리팩 시 합니다을 경량감습니다
 - [CPU 작업 분할](./527_work_stealing.md) → CPU 작업 분할/청킹 처리
   - [async/await](./523_async_await.md) → 문법적(syntactic sugar)
로 비동기 처리
   - [select](./519_io_multiplexing.md) + [select](https://nodejs.org/api/en.html) 입力 감소
   - [Promise](https://developer.mozilla.org/en-US/docs/Web/API/JavaScript_reference/global_objects/Promise)
   - [async_hooks](https://nodejs.org/api/en.html#async_hooks)
 for more information on the `setTimeout`, `setInterval()`, or understanding how `setTimeout` works.
 Let's look at Node.js internals.
 These docs: https://nodejs.org/api/en.html#timers, The legacy deprecated APIs. Also: I recommend using the `setLegacyTimeout` and `setInterval` methods in your request: https://nodejs.org/api-docs/v14/migration-guide
 and (https://nodejs.org/api/en.html#timers) — **Legacy feature will be removed in new projects. Please use `modern` alternatives**

I recommend using the `setLegacyTimeout` and `setInterval` methods. The native APIs `setTimeout` and `setInterval`. These APIs may have similar functionality, but they behavior is essentially the same. They forward-compatibility, note that the non-legacy APIs is, as well as async/await syntax, your code bases.

 |
   - **Promises API**: 라는 `promises` API` in Node.js에서 보:
   - https://nodejs.org/api/util.html#utilpromisify
   - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_objects/promise
   - https://nodejs.dev/en/learn/asynchronous-work

   - [���: 호 informat: Turn 성시 signal complet.

### 👶 어린이를 위한 줄 비유 설명
**개념**: async/await는 "피자 주문 화면" 같아요!
**원리**: 주문 내역을 실시간으로 보여요!
**효과**: 비동기 코드가 간결해요!
