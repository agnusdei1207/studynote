+++
title = "590. 웜 (Worm) - 자율적 침투자"
date = "2026-03-25"
[extra]
categories = "studynote-operating-system"
+++

# 웜 (Worm) - 자율적 침투자

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Worm은 컴퓨터virus와 달리 별도의 숙주 프로그램 없이 독립적으로 실행되어 네트워크를 통해 빠른 속도로 자기복제를 확산하는 악성 소프트웨어다. 사용자의 개입 없이도 시스템에서 시스템으로 전파되어, 단기간 내에 대규모 감염을 야기할 수 있다.
> 2. **가치**:worm의 가장 큰 특징은 1988년 Robert Morris가作成した(만든) Morris Worm에서 확인되듯, 인터넷 역사상 최초의大规模(대규모) 감염 사건을 일으켰으며, 감염 속도가 指數的(지수적)으로 증가하여 6,000대의 컴퓨터 중 10%인 600대가 피해를 입었다.
> 3. **한계**:worm은 네트워크 대역폭을 Consumption(소모)시키고, 취약점 패치로永恒(영구)적으로 차단될 수 있으며, 현대 Firewalls(방화벽), IPS/IDS, 분산 네트워크 보안 기술의 발전으로 탐지 및 차단 능력이 크게 향상되었다.

---

## 1. 개요 및 역사

### Morris Worm 사건 (1988)
Robert Morris가仕組(심화)한Morris Worm은 인터넷 역사상 첫 번째 대규모worm 감염 사건이다. 1988년 11월 2일Unix 시스템의 finger 및 sendmail 취약점을 利用(약용)하여 6,000대의 컴퓨터 중 약 10%(600대)가 감염되어lehre(피해)를 입었다.

```text
[Morris Worm 감염 메커니즘]

  Patient Zero: 감염된 Unix 서버 1대
      |
      +--> 취약점 스캔 (IP 주소 브로드캐스트)
      |
      +--> 10개 취약점 발견
           +--> 10개 서버 추가 감염 + 각 서버에서 병렬 스캔
           |
           +--> 10^2 --> 10^3 --> 10^4...
               Exponential 확산!
```

**[핵심 포인트]** worm의 가장 큰 특징은指數的(지수적) 감염 속도다. 각 감염主机(호스트)에서 스스로 스캔과 전파를 병렬 수행하므로, 감염이 Exponential(기하급수적)으로扩散된다.

---

## 2. 전파 방식 및 구성 요소

### 주요 전파 방식
| 방식 | 설명 | 예시 |
|---|---|---|
| **네트워크 취약점** |EternalBlue, SMB, SSH 무차별 공격 | WannaCry, NotPetya |
| **파일 공유** | SMB, NFS 등 네트워크 파일 공유 | Conficker |
| **이메일** | SMTP를 통한 악성 링크/파일 배포 | SoBig |

### 핵심 구성 요소
| 구성 요소 | 설명 |
|---|---|
| **Scanner** | 취약점IP 탐색 모듈 |
| **Exploit** | 원격 코드 실행(RCE) 취약점 공격 |
| **Replicator** | 자기복제 및 전파 엔진 |
| **Payload** | DDoS, ransomware, 데이터 탈취 등 |

---

## 3. 주요 Worm 사례

### 세계적 유행 worm Timeline
| 연도 | worm 이름 | 취약점 |Impact(영향) |
|---|---|---|---|
| 1988 | Morris Worm | Unix finger, sendmail | 6,000대 감염 |
| 2001 | Code Red | IIS Directory Traversal | 359,000대 감염 |
| 2003 | SQL Slammer | SQL Resolution Service | 75,000대 감염, 10분 이내全球(전세계) 확산 |
| 2008 | Conficker | Windows SMBv2 | 900만~1,500만 대 감염 |
| 2010 | Stuxnet | Windows LNK, USB | イ란(이란) 핵시설 타겟 |
| 2017 | WannaCry | ETERNALBLUE (SMBv1 RCE) | 150개국 20만 대 이상 감염 |
| 2017 | NotPetya | ETERNALBLUE + Mimikatz | 우크라이나 중심 + 全球(전세계) 확산 |

---

## 4. Worm vs Virus vs Trojan 비교

| 구분 |Worm|Virus|Trojan|
|---|---|---|---|
| **자기복제** | **예** | 예 | 아니오 |
| **감염 경로** | 네트워크 | 파일 | 수동 |
| **확산 속도** | **매우 빠름** | 중간 | 느림 |
| **숙주 필요** | 아니오 | 예 | 아니오 |
| **대역폭 영향** | **甚大(심대)** | 미미 | 미미 |

```text
[확산 속도 비교]

  Worm:     1 --> 10 --> 100 --> 1,000 --> 10,000 (수시간)
  Virus:    1 --> 10 --> 100 --> 1,000 (수일~수주)
  Trojan:   1 --> 10 (사용자 배포에 의존)
```

---

## 5. 실전 대응 전략

### 기술적 대응
| 구분 | 전통 대비 | 현대 대응 |効果(효과) |
|---|---|---|---|
| **네트워크 분산** | VLAN, ACL | Zero Trust Network Access | Lateral Movement 차단 |
| **패치 관리** | 수동 패치 | WSUS, SCCM, Qualys | 취약점 사전 차단 |
| **IPS/IDS** | Signature 기반 | AI 기반 이상 탐지 | 0-day 탐지 가능 |
| **SMBv1 비활성화** | N/A | 프로토콜 제거 | ETERNALBLUE 원천 차단 |

### 경영진 의사결정
- **RTO (복구 시간 목표)**: 4시간 이내 목표
- **복구 전략**: Isolated NetworkSegment(격리 네트워크 분절) 구성, 사전演练(연습)된 Incident Response 계획 실행

---

## 관련 개념 맵 (Knowledge Graph)

| 개념 | 설명 |
|---|---|
| **ETERNALBLUE** | NSA 유출 SMBv1 취약점 exploit, WannaCry/NotPetya의 주요 공격 벡터 |
| **Ransomware** |worm이 Deploy(전개)하는 주요payload 유형 |
| **Lateral Movement** | 감염 호스트에서 다른 시스템으로 이동하는 기술 |
| **Patch Management** |worm의 주요感染 경로인 취약점을 사전 차단하는방편 |

---

## 👶 어린이를 위한 3줄 비유 설명
1. Worm은virus와 달리 사람 도움 없이도勝手(胜手)에隣집(이웃집)으로 옮겨가는-spreading(확산) 벌레와 같다. 한 집에 들어가면 그 집에서도胜手에 다른 집으로 옮겨가는 것이worm의 가장 큰 특징이다.
2.worm은 한번 터지면internet를 타고短短(짧은) 시간에全世界(전세계)로扩散될 수 있어서, 정말，怕(무서운) 컴퓨터 해킹 기술이다.
3. 그래서 우리는 항상 컴퓨터 프로그램을最新(최신)으로 업데이트 하고, 이상한メール(메일)을 열지 않는 것이worm을 예방하는 가장 좋은 방법이다.
