+++
title = "578. 임의적 접근 제어 (DAC, Discretionary Access Control)"
date = "2026-03-25"
[extra]
categories = ["studynote-operating-system"]
+++

# 임의적 접근 제어 (DAC, Discretionary Access Control) - 파일 소유자가 접근 권한을 자발적으로 부여하는 자율적 접근 제어 방식

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DAC은 파일의 **소유자(Owner)**가 자기 파일에 대한 접근 권한을 **자유재량(Discretionary)**에 따라 타인에게 부여하거나 회수할 수 있는 방식이다. Unix/Linux의 `chmod` 명령어가 대표적이다.
> 2. **가치**: 파일 공유 시 관리자의 개입 없이 **소유자가 직접 권한을 설정**하므로, 소규모 환경에서는 유연하고迅速(신속)한 협업이 가능하다.
> 3. **한계**: Trojan Horse(트로이 목마)와 같은 악성코드가 DAC 권한을 악용하면, 시스템 전체가 침해될 수 있다. 따라서 **강제적 접근 제어(MAC)와의 이중 구조**가 권장된다.

---

## 1. 개요 및 배경 (Context & Necessity)

### 1.1 DAC의原理

DAC의 핵심 원칙은 **"자신이 소유한 객체에 대한 권한은 자발적으로 부여/회수 가능"**이다:

```bash
# Alice가 소유한 파일
-rw-r--r--  alice  alice  /home/alice/document.txt

# Alice가 Bob에게 읽기 권한 부여
$ chmod 744 /home/alice/document.txt
# 결과: alice만 읽기/쓰기, others는 읽기만
```

### 1.2 Unix/Linux의 파일 권한 구조

```text
[ 9비트 구조 ]
所有者(Owner)  Group   Others
   rwx          r-x     r--

[ 예시: chmod 750 ]
rwx r-x --- : Owner는 읽기/쓰기/실행, Group은 읽기/실행, Others는 접근 불가
```

---

## 2. Trojan Horse 공격과 DAC의脆弱性

### 2.1 Trojan Horse의動作

1. 사용자가 악성 프로그램을 실행
2. 프로그램이 사용자의 **DAC 권한을 상속**받음
3. 악성 코드가 사용자 권한으로 시스템 자원에 접근

### 2.2 공격 시나리오

```text
[ 공격 흐름 ]
1. Alice가 malicious_program 실행
2. malicious_program이 Alice의 권한(Root)으로 실행 (DAC 상속)
3. 프로그램이 /etc/shadow 파일에 무단 접근 시도
4. Alice의 권한으로는 /etc/shadow에 접근 가능하므로 -> 공격 성공
```

---

## 3. DAC vs MAC: 보안 모델比較

| 구분 | DAC (임의적) | MAC (강제적) |
|:---|:---|:---|
| **권한 결정** | 파일 소유자가自行(자신) 결정 | 시스템 정책이強制(강제) 결정 |
| **대표 예시** | Unix `chmod`, Windows ACL | SELinux, AppArmor |
| **분산 관리** | 용이 (소유자 직접 관리) | 어려움 (중앙 관리자 필요) |
| **보안 수준** | 상대적 낮음 | 높음 |
| **유연성** | 높음 | 낮음 |

---

## 4. 기대효과 및 결론

- **소규모 환경**에서는 DAC만으로 충분한 보안 수준을 달성할 수 있음
- **대규모/고보안 환경**에서는 DAC와 MAC의 이중 방어 체계가 필수적
- **클라우드 환경**에서는 IAM(Identity and Access Management)을 통해 DAC 원칙을 세밀하게 제어

---

## 관련 개념 맵 (Knowledge Graph)

| 관련 개념 | 설명 |
|:---|:---|
| **ACL (575장)** | DAC를 구현하는 객체 중심의 자료구조 |
| **MAC (579장)** | DAC와 대칭되는 강제적 접근 제어 |
| **Trojan Horse (586장)** | DAC의脆弱性(취약점)을 악용하는 공격 |
| **chmod 명령어** | Unix/Linux DAC의 대표적 구현 |

---

## 👶 어린이를 위한 3줄 비유 설명

1. **DAC**는 아파트의 **"자가 관리 시스템"**과 같다. 각 세대의 소유자가 열쇠를 가지고 있고, 원하는 사람에게 열쇠를複製(복제)하여 줄 수 있다.

2. **보안 문제**는 악의 있는 세입자가 **"집 주인에게 받은 열쇠"**를 악용하여 금고에 침입하는 것과 같다. 열쇠를 받은 입幌(사람)이 악용하면 시스템이 이를 차단할 수 없다.

3. **DAC와 MAC의二重(이중) 방어**는 **"자가 관리 + 건물 전체 경비 시스템"**과 같다. 세대 주인이 열쇠를 줘도, 경비원이 "이 사람은 금고 출입이 불가하다"고 차단할 수 있다.
