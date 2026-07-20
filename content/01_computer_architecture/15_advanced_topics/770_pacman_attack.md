---
title: "ARM PAC"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 770
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PACMAN 공격은 Arm의 PAC (Pointer Authentication Code)을 암호학적으로 깨는 것이 아니라, 투기적 실행 (Speculative Execution) 중 PAC 검증 결과를 부채널로 바꿔 "이 PAC 추측값이 맞는가"를 조용히 묻는 <strong>PAC oracle 공격</strong>이다.
> 2. **가치**: PAC은 원래 포인터 변조 시 즉시 fault를 내는 하드웨어 CFI (Control-Flow Integrity) 장치였지만, PACMAN은 그 fault가 건축적으로 확정되기 전 transient window를 이용해 무음 브루트포스를 가능하게 했다.
> 3. **판단 포인트**: PACMAN은 PAC 단독 무력화라기보다 memory corruption bug, gadget, side channel이 결합된 복합 공격이므로, 방어도 PAC + BTI (Branch Target Identification) + MTE (Memory Tagging Extension) + speculation barrier를 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

PACMAN 공격은 Arm 아키텍처의 포인터 인증 기능을 우회하는 대표적인 transient-execution 공격이다. PAC은 AArch64 (64-bit Arm execution state) 포인터의 미사용 상위 비트에 PAC을 붙이고, 사용 직전에 검증함으로써 리턴 주소나 함수 포인터 위변조를 막는다. 정상 설계라면 PAC이 틀린 포인터는 즉시 trap이 나므로 공격자가 조용히 여러 값을 시험하기 어렵다.

문제는 현대 CPU가 성능을 위해 예외와 분기 결과가 확정되기 전에 명령을 앞당겨 실행한다는 점이다. PACMAN은 바로 이 투기적 실행 창을 이용한다. PAC 검증이 건축적으로는 실패할 값이라도, 그 실패가 retire 단계에서 확정되기 전까지는 미세구조 상태, 특히 캐시 흔적이 남을 수 있고, 공격자는 그 흔적으로 정답 여부를 추정한다.

이 공격이 중요한 이유는 PAC이 "메모리 손상 이후의 마지막 하드웨어 방어선"으로 받아들여졌기 때문이다. PACMAN은 PAC 자체를 쓸모없게 만들었다기보다, PAC만 믿고 메모리 안전이나 speculative side-channel 통제를 소홀히 하면 하드웨어 보호도 우회될 수 있음을 보여 줬다. 또한 이 공격은 보통 추가적인 memory corruption primitive 없이는 완전한 익스플로잇으로 이어지지 않는다는 점도 같이 기억해야 한다.

- **📢 섹션 요약 비유**: 틀린 열쇠를 넣으면 경보가 울리는 자물쇠라도, 경보가 울리기 0.1초 전에 문틈 센서가 반응하는지를 보면 맞는 열쇠인지 조용히 시험해 볼 수 있는 셈이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PACMAN의 핵심은 "PAC 검증 성공 여부를 side channel로 바꾸는 gadget"이다. 공격자는 이미 존재하는 버그를 이용해 PAC가 붙은 포인터를 어느 정도 제어하고, PAC 값을 하나씩 추측해 본다. 이후 `AUT*` 계열의 authenticate 명령과 그 뒤에 이어지는 메모리 접근이 투기적으로 실행되는 순간, 맞는 추측이면 특정 캐시 라인이 채워지고 틀리면 그렇지 않다는 차이를 측정한다.

PAC 비트 수는 가상 주소 폭, Top Byte Ignore 설정, 구현 세부에 따라 제한되므로 대개 수십 비트 이하에서 결정된다. 그래서 강력한 yes/no oracle만 있으면 "비밀 키"를 모르더라도 유효한 PAC 값을 찾는 브루트포스가 현실적인 범위로 내려온다. 중요한 점은 PACMAN이 키를 복원하는 것이 아니라, 특정 포인터 문맥에 맞는 PAC 값을 찾아내는 데 초점을 둔다는 것이다.

| 구성 요소 | 역할 | 공격 성립 조건 |
| :--- | :--- | :--- |
| memory corruption primitive | 공격자가 포인터 후보를 주입 | 버퍼 오버플로우, UAF (Use-After-Free) 등 선행 취약점이 필요하다. |
| `AUT*` 인증 명령 | PAC 일치 여부 검증 | 실패가 architecturally retire되기 전 transient window가 있어야 한다. |
| PAC oracle gadget | 성공 시 캐시 흔적을 남김 | 인증 결과에 따라 다른 미세구조 상태가 만들어져야 한다. |
| cache timing side channel | 정답 여부 관찰 | hit/miss를 안정적으로 구분할 수 있어야 한다. |
| 제한된 PAC 비트 공간 | 브루트포스 비용 감소 | 구현에 따라 16~24비트 안팎이 흔하다. |

아래 그림은 PACMAN이 fault를 직접 내지 않고 "캐시 흔적"으로 정답을 묻는 방식을 보여 준다.

```text
+--------------------------------------------------------------------+
| PACMAN speculative PAC oracle                                     |
+--------------------------------------------------------------------+
| attacker-controlled pointer + guessed PAC                         |
|                  |                                                 |
|                  v                                                 |
|             AUT* verification                                      |
|                  |                                                 |
|       transient window before architectural trap                   |
|          |                                  |                      |
|          +- correct guess --> cache line touched                    |
|          +- wrong guess   --> no useful cache effect                |
|                  |                                                 |
|                  v                                                 |
|        timing probe reveals whether guess was accepted            |
+--------------------------------------------------------------------+
```

즉 PACMAN은 "틀리면 즉시 크래시"라는 PAC의 장점을 "틀려도 조용히 흔적만 남기고 롤백"으로 뒤집는다. 다만 여기서 얻는 것은 PAC 자체의 유효 여부이지, 임의의 코드 실행이 자동으로 따라오는 것은 아니다. 실제 악용에는 여전히 포인터를 원하는 위치에 배치하는 메모리 손상, 쓸 만한 gadget, 적절한 권한 경계가 함께 필요하다.

- **📢 섹션 요약 비유**: 선생님이 답안지를 걷기 전에 맞는지 틀리는지 얼굴 표정이 잠깐 드러난다면, 학생은 제출 전에 답을 하나씩 바꿔 보며 정답을 맞혀 갈 수 있다.

---

## Ⅲ. 비교 및 연결

PACMAN은 Spectre류와 자주 같이 언급되지만 목표가 다르다. Spectre는 다른 문맥의 데이터를 읽는 정보 유출에 초점이 있고, PACMAN은 PAC 보호 장치의 "정답 판별기"를 만드는 데 초점이 있다. 즉 둘 다 speculative execution을 쓰지만, 하나는 비밀 바이트를 읽고 다른 하나는 유효한 보호 토큰을 찾는다.

| 항목 | Spectre 계열 | PACMAN |
| :--- | :--- | :--- |
| 주된 목표 | 타 문맥 데이터 누설 | PAC 유효값 판별 |
| 직접 산출물 | 비밀 데이터 조각 | yes/no PAC oracle |
| 전형적 결과 | 정보 유출 | PAC 우회 후 제어 흐름 공격 발판 |
| 추가 필요 조건 | gadget + side channel | gadget + side channel + memory corruption |
| 무너뜨리는 가정 | speculative read는 안전하다 | PAC 실패는 조용히 시험 불가하다 |

또한 PACMAN은 PAC이 메모리 안전의 대체재가 아님을 선명하게 보여 준다. PAC이 포인터 진위를 높여도, 선행하는 버퍼 오버플로우나 UAF가 존재하면 공격자는 여전히 통제 가능한 포인터를 만든다. 여기에 BTI가 착지 지점을 제한하고, MTE가 메모리 태그 불일치를 잡아 주며, 메모리 안전 언어가 원인 자체를 줄여야 비로소 방어가 입체적으로 완성된다.

따라서 PACMAN의 교훈은 "PAC이 약하다"가 아니라 "PAC도 speculative side-effect와 결합하면 단독 방어선이 될 수 없다"이다. 포인터 인증, 분기 보호, 메모리 태깅, 메모리 안전은 서로 대체 관계가 아니라 서로 다른 층을 지키는 보완 관계다.

- **📢 섹션 요약 비유**: PAC이 위조 방지 도장이라면, PACMAN은 도장을 뜯어 보는 것이 아니라 검사관의 눈빛을 읽어 어떤 도장이 진짜인지 추측하는 기술이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무 대응은 "PAC 유지"와 "PAC에 과신하지 않기"를 동시에 해야 한다. PAC은 여전히 포인터 변조 비용을 크게 높여 주므로 끄는 것이 답이 아니다. 대신 커널과 런타임의 민감한 경로에서는 authenticated pointer가 speculative load의 주소로 바로 쓰이지 않도록 barrier나 데이터 의존성을 배치하고, 컴파일러 수준에서는 `pac-ret`와 BTI를 함께 활성화해 우회 이후 이동 공간을 줄이는 것이 좋다.

### 실무 체크리스트

1. PAC 보호와 함께 BTI, MTE, Shadow Stack 계열 보호를 병행하고 있는가?
2. 커널·하이퍼바이저의 authenticated pointer 사용 경로에 speculation barrier가 필요한 지점을 검토했는가?
3. PACMAN의 전제인 memory corruption bug를 줄이기 위해 Rust, Swift, sanitizers, fuzzing을 적극 활용하고 있는가?
4. PAC oracle gadget이 될 수 있는 코드 패턴을 감사하고 있는가?

실무 관점에서는 "하드웨어 보안 기능이 있으니 unsafe C/C++ 코드도 괜찮다"는 판단이 가장 위험하다. PACMAN은 하드웨어 보안을 꺼 버리라는 뜻이 아니라, 하드웨어 보호를 최후 방어선으로 놓되 그 앞단의 메모리 안전과 speculative-execution 통제를 반드시 같이 설계하라는 경고에 가깝다. 이미 출하된 하드웨어에서는 완전한 근본 패치가 어렵기 때문에, 실제 운영에서는 계층형 방어와 gadget 축소가 핵심이다.

- **📢 섹션 요약 비유**: 지문 인식 도어락을 달았다고 창문을 열어 둬도 되는 것은 아니다. 문은 계속 잠가 두되, 창문 잠금장치와 CCTV까지 함께 갖춰야 집이 안전해진다.

---

## Ⅴ. 기대효과 및 결론

PACMAN을 계기로 얻는 실무적 효과는 제어 흐름 보호를 더 입체적으로 설계하게 된다는 점이다. PAC만 켜 두는 것보다 PAC + BTI + MTE + 메모리 안전 도입 전략을 함께 세우면, 공격자는 한 번에 여러 층을 동시에 넘어야 하므로 비용이 크게 올라간다. 또한 speculative execution이 만드는 미세구조 흔적도 보안 검토 범위에 포함하게 되어, 하드웨어 기능 평가가 더 현실화된다.

한계도 분명하다. PACMAN은 만능 원격 공격이 아니고, 구현 세부·가젯 존재·선행 취약점에 크게 의존한다. 그럼에도 의미가 큰 이유는 "건축적으론 안전해 보여도 transient path가 새면 보호 의미가 달라진다"는 점을 보여 줬기 때문이다. 앞으로는 PAC 실패 시 더 이른 시점에 의존 경로를 무효화하거나, 인증 완료 전에는 민감한 load가 절대 transient하게 진행되지 않도록 하는 설계가 중요해질 것이다.

결론적으로 PACMAN은 Arm PAC을 부정한 사건이 아니라, PAC을 포함한 하드웨어 CFI가 speculative execution과 함께 설계되어야 함을 입증한 사건이다. 이 주제는 "PAC 우회 공격"으로만 외우기보다, 포인터 인증과 transient side-channel의 충돌 사례로 기억하는 편이 기술적으로 더 정확하다.

- **📢 섹션 요약 비유**: 훌륭한 문지기도 복도 거울에 비친 표정이 다 보이면 속일 수 있다. 그래서 앞으로는 문지기만 세우는 것이 아니라, 표정이 새지 않게 복도 구조까지 바꿔야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| PAC (Pointer Authentication Code) | PACMAN이 우회하려는 Arm의 포인터 서명 메커니즘이다. |
| `AUT*` 명령 | 포인터 사용 직전 PAC 검증을 수행하는 명령 경로다. |
| Speculative Execution | PAC 실패가 확정되기 전 transient side effect를 만드는 기반이다. |
| PAC oracle gadget | PAC 추측의 성공/실패를 캐시 흔적으로 바꾸는 코드 조각이다. |
| BTI (Branch Target Identification) | PAC 우회 후 간접 분기 착지점을 더 좁혀 주는 보완 방어다. |
| MTE (Memory Tagging Extension) | PACMAN의 선행 조건인 메모리 손상 자체를 줄이는 보완 기법이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
메모리 손상 취약점
        |
        v
PAC (Pointer Authentication Code)
        |
        v
PACMAN speculative PAC oracle
        |
        v
PAC 우회 가능성 + control-flow hijack 발판
        |
        v
PAC + BTI + MTE + speculation barrier
```

이 흐름은 "포인터 보호 도입"에서 끝나지 않고, "보호 검증 과정 자체의 transient 안전성"까지 검토 범위가 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 중요한 주소표에 비밀 도장을 찍어 두고, 맞는 도장인지 확인한 뒤에만 문을 열어 줘요.
2. 그런데 PACMAN은 문이 완전히 닫히기 전에 바닥 발자국을 보고 "이 도장이 맞는가?"를 몰래 알아내는 도둑이에요.
3. 그래서 이제는 도장만 확인할 게 아니라, 발자국이 남지 않게 복도까지 더 조심해서 만들어야 해요.
