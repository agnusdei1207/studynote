+++
title = "416-420. TCP 연결 설정 및 종료 (Handshake)"
description = "신뢰성 있는 연결을 위한 3-Way Handshake와 안전한 종료를 위한 4-Way Handshake 과정 상세 분석"
date = 2026-03-14
[extra]
subject = "NW"
category = "Transport Layer"
id = 416
+++

# 416-420. TCP 연결 설정 및 종료 (Handshake)

> **핵심 인사이트**: TCP 통신은 '예의 바른 대화'이다. 시작할 때는 서로의 존재와 번호를 세 번 확인(3-Way)하고, 끝낼 때는 남아있는 짐이 없는지 꼼꼼히 챙기며 네 번 확인(4-Way)한다. 특히 종료 후 잠시 기다리는 TIME_WAIT은 통신의 결벽증에 가까운 완벽함을 상징한다.

---

## Ⅰ. 연결 설정: 3-Way Handshake
데이터를 보내기 전, 송수신자 간의 논리적 통로를 개설하는 과정입니다.

1. **[Step 1] SYN (Client $\rightarrow$ Server)**: 
   - 클라이언트가 서버에게 연결을 요청합니다. 이때 임의의 숫자인 **ISN (Initial Sequence Number)** 을 생성해 보냅니다.
   - 클라이언트 상태: `SYN_SENT`
2. **[Step 2] SYN + ACK (Server $\rightarrow$ Client)**:
   - 서버가 요청을 수락합니다. 클라이언트의 번호에 1을 더해 확인(`ACK = ISN+1`)하고, 자신도 자신의 번호(`SYN`)를 보냅니다.
   - 서버 상태: `SYN_RECEIVED`
3. **[Step 3] ACK (Client $\rightarrow$ Server)**:
   - 클라이언트가 서버의 수락을 확인합니다. 서버의 번호에 1을 더해 보냅니다.
   - 클라이언트/서버 상태: `ESTABLISHED` (연결 완료!)

* **ISN을 무작위로 만드는 이유**: 이전 연결에서 늦게 도착한 패킷과 혼동되지 않도록 하고, 해커가 다음 번호를 예측하여 세션을 가로채는(Session Hijacking) 것을 방지하기 위함입니다.

---

## Ⅱ. 연결 종료: 4-Way Handshake
데이터 전송을 마치고 연결을 안전하게 끊는 과정입니다.

1. **[Step 1] FIN (Client $\rightarrow$ Server)**:
   - 클라이언트가 "나 이제 더 보낼 거 없어"라고 말합니다. (상태: `FIN_WAIT_1`)
2. **[Step 2] ACK (Server $\rightarrow$ Client)**:
   - 서버가 "알겠어, 확인했어. 그런데 나 아직 보낼 게 남았을 수도 있으니 잠시만 기다려줘."라고 답합니다. (상태: `CLOSE_WAIT`)
   - 클라이언트는 서버의 남은 데이터를 받을 준비를 합니다. (상태: `FIN_WAIT_2`)
3. **[Step 3] FIN (Server $\rightarrow$ Client)**:
   - 서버도 보낼 데이터를 다 보낸 후, "나도 이제 끝났어!"라고 말합니다. (상태: `LAST_ACK`)
4. **[Step 4] ACK (Client $\rightarrow$ Server)**:
   - 클라이언트가 "응, 너도 수고했어!"라고 마지막 인사를 보냅니다. (서버 상태: `CLOSED`)

---

## Ⅲ. 종료 후의 결벽증: TIME_WAIT
클라이언트가 마지막 ACK를 보낸 직후 바로 연결을 끊지 않고, 일정 시간(**기본 2MSL, 약 1~4분**) 동안 대기하는 상태입니다.

* **존재 이유**:
  1. **마지막 ACK 유실 대비**: 만약 마지막 인사가 서버에 안 갔다면, 서버는 다시 FIN을 보낼 것입니다. 이때 클라이언트가 이미 종료되었다면 서버는 정상 종료를 못 하게 됩니다.
  2. **지연 패킷 처리**: 이전에 전송되었던 패킷이 아주 늦게 도착했는데, 마침 똑같은 포트로 새로운 연결이 맺어져 있다면 데이터가 꼬일 수 있습니다. 이를 방지하기 위해 이전 패킷들이 네트워크에서 모두 소멸할 때까지 기다려주는 것입니다.

---

## Ⅳ. 개념 맵 및 요약

```ascii
[TCP 3-Way / 4-Way Handshake 흐름]

(시작) Client           Server         (종료) Client           Server
        | ---- SYN ----> |                     | ---- FIN ----> |
        | <---SYN+ACK--- |                     | <---- ACK ---- |
        | ---- ACK ----> |                     | (Wait...)      |
        |                |                     | <---- FIN ---- |
        | (ESTABLISHED)  |                     | ---- ACK ----> |
                                               | (TIME_WAIT)    |
                                               | (CLOSED)       | (CLOSED)
```

📢 **섹션 요약 비유**: **3-Way Handshake**는 "전화받으세요(SYN)" $\rightarrow$ "네, 들려요. 제 목소리도 들리나요?(SYN+ACK)" $\rightarrow$ "네, 잘 들립니다(ACK)"라고 통화 품질을 확인하는 과정입니다. **4-Way Handshake**는 "저 끊을게요(FIN)" $\rightarrow$ "네, 잠깐만요 하던 말 다 하고요(ACK)" $\rightarrow$ (남은 말 다 한 뒤) "저도 이제 끊을게요(FIN)" $\rightarrow$ "네, 그럼 진짜 끊습니다(ACK)"라고 인사하는 정중한 종료 예절입니다.
