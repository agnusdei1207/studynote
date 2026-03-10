+++
title = "620. SELinux (Security-Enhanced Linux)"
weight = 620
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SELinux는 NSA(미 국가안보국)가 개발한 **"Type Enforcement(TE) 기반의 강제적 접근 제어(MAC) 구현체"**로서, 모든 프로세스와 객체(Object)에 **보안 컨텍스트(Security Context: user:role:type:level)**를 부여하고, 이를 기반으로 **정책(Policy)**에 따른 강제적 접근 통제를 수행한다. 루트 권한을 가졌더라도 SELinux 정책을 위반하면 접근이 거부된다.
> 2. **가치**: DAC만으로는 **"트로이 목마 취약성"**을 극복할 수 없지만, SELinux는 **"프로세스 도메인(Domain)과 객체 타입(Type) 간의 허용 관계를 정책"**으로 정의하여, 웹 서버가 탈취되더라도 `/etc/shadow`나 시스템 설정 파일에 접근하는 것을 원천 봉쇄할 수 있다.
> 3. **융합**: RHEL/CentOS/Fedora의 기본 보안 모듈이며, 최신 커널(5.x 이후)에서는 **eBPF LSM**와 결합하여 사용자 공간에서도 보안 정책을 개발할 수 있게 확장되고 있다. 도커, systemd의 임시 파일시스템(`tmpfs.d`)도 SELinux로 보호된다.

---

## Ⅰ. 개요 (Context & Background)

- **개념**: SELinux(Security-Enhanced Linux)는 **"리눅스 커널에 통합된 강제적 접근 제어(MAC) 시스템"**으로서, 전통적인 DAC(Discretionary Access Control)를 보완하는 커널 레벨 보안 계층이다. 모든 프로세스와 파일, 소켓, IPC 객체 등에 **보안 컨텍스트(Security Context)**를 부여하고, **"Type Enforcement(TE)"**라 불리는 도메인-타입 간 접근 제어 정책을 강제한다.

- **💡 비유**: SELinux는 **"모든 국민에게 신분증을 발급하고, 직업별로 출입할 수 있는 장소를 제한하는 국가 보안 시스템"**과 같다. 국민(프로세스)은 **신분증(보안 컨텍스트: user:role:type:level)**을 소지하며, 직장별(도메인)로 출입 가능한 장소(파일 타입)이 정해져 있다. 예를 들어 **"웹 서버 직원(httpd_t)은 병원 기록(shadow_t) 구역에는 출입 불가"**하며, 이는 국가 보안법(SELinux 정책)에 의해 강제된다.

- **등장 배경**:
  1. **DAC의 한계 극복(1990s)**: 기존 UNIX의 DAC(rwx 권한)는 **"소유자가 속으면 전권한 상속"**되어 트로이 목마 공격에 취약했다. NSA는 이를 해결하기 위해 MAC를 연구하기 시작했다.
  2. **Flask 프로젝트(1992-2000)**: NSA는 DAC를 보완하는 MAC 시스템을 개발했으며, 이를 **"Flask"**라고 불렀다. 이후 오픈 소스로 전환되면서 SELinux로 이름이 바뀌었다.
  3. **리눅스 커널 통합(2003)**: 리눅스 커널 2.6에 SELinux가 통합되었고, RHEL 4부터 기본 활성화되었다. 현재는 대부분의 주요 리눅스 배포판(RHEL, CentOS, Fedora)에서 기본으로 제공된다.

SELinux의 보안 컨텍스트 구조를 시각화하면 다음과 같다. 각 프로세스와 객체는 **`user:role:type:level`** 형식의 보안 컨텍스트를 가진다.

```text
 ┌──────────────────────────────────────────────────────────────────────┐
 │               SELinux 보안 컨텍스트(Security Context)                   │
 ├──────────────────────────────────────────────────────────────────────┤
 │                                                                      │
 │  [보안 컨텍스트 형식]                                               │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │                                                                 │  │
 │  │   user:role:type:level[:category]                             │  │
 │  │                                                                 │  │
 │  │   예: system_u:system_r:httpd_t:s0-s0:c0.c255                   │  │
 │  │       └─┬──┘ └──┬──┘ └───┬─┘ └──────────┬──────┘              │  │
 │  │         │       │        │            │                     │  │
 │  │         │       │        │            └─ MLS Level           │  │
 │  │         │       │        └─ Type                             │  │
 │  │         │       └─ Role                                    │  │
 │  │         └─ User                                           │  │
 │  │                                                                 │  │
 │  └────────────────────────────────────────────────────────────────┘  │
 │                                                                      │
 │  [요소별 의미]                                                      │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │                                                                 │  │
 │  │  • User: SELinux 사용자 (system_u, user_u, staff_u, root_u)  │  │
 │  │    – 리눅스 UID와는 별개의 개념                               │  │
 │  │                                                                 │  │
 │  │  • Role: 역할 (system_r, staff_r, object_r, unconfined_r)       │  │
 │  │    – 도메인 간 전이를 제어                                   │  │
 │  │                                                                 │  │
 │  │  • Type: 타입 (httpd_t, shadow_t, etc_t)                       │  │
 │  │    – Type Enforcement(TE)의 핵심                               │  │
 │  │    – 프로세스는 _t(Type) 접미사, 파일은 _t(Type)로 레이블  │  │
 │  │                                                                 │  │
 │  │  • Level: MLS 등급 (s0~s15)                                   │  │
 │  │    – Bell-LaPadula/Biba 모델 구현                             │  │
 │  │    – s0-s0: 단일 등급, s0-s15: 등급 범위                       │  │
 │  │                                                                 │  │
 │  │  • Category: 카테고리 (c0.c1023)                             │  │
 │  │    – 프로젝트별 분리(Compartment)                             │  │
 │  │                                                                 │  │
 │  └────────────────────────────────────────────────────────────────┘  │
 │                                                                      │
 └──────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** SELinux의 보안 컨텍스트는 **"사용자:역할:타입:등급"**의 4가지 요소로 구성된다. **User**는 리눅스 UID와 별개로 SELinux 사용자(`system_u`, `user_u`, `staff_u`, `root_u`)를 정의한다. **Role**은 도메인 간 전이를 제어하며, 예를 들어 `staff_r` 역할은 `unconfined_t` 도메인에서 `httpd_t` 도메인으로 전이할 수 있다. **Type**은 Type Enforcement(TE)의 핵심으로서, `httpd_t`(웹 서버 프로세스)와 `httpd_sys_content_t`(웹 콘텐츠) 간의 허용 관계를 정의한다. **Level**과 **Category**는 MLS(Multi-Level Security)와 Compartment를 구현한다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **보안 컨텍스트(Security Context)** | 주체/객체의 보안 레이블 | `user:role:type:level` | sid, pid, inode | 신분증 |
| **도메인(Domain)** | 프로세스의 보안 영역 | `httpd_t`, `unconfined_t` | Type Enforcement | 직장 |
| **타입(Type)** | 객체의 보안 분류 | `shadow_t`, `etc_t` | Type Enforcement | 출입 허가 구역 |
| **정책(Policy)** | 도메인-타입 간 허용 규칙 | TE 정책, MLS 정책 | `.te`, `.if` 파일 | 보안 규정 |
| **AVC(Access Vector Cache)** | 정책 검색 결과 캐시 | 빠른 허가/거부 판단 | `avc.c` | 검색 기록 |
| **별도(Permissive) 모드** | 정책 위반 시 로그만 남기고 차단하지 않음 | 개발/디버깅용 | `setenforce 0` | 훈련 모드 |

---

### Type Enforcement(TE) — 도메인-타입 간 접근 제어

SELinux의 핵심인 Type Enforcement(TE)는 **"프로세스 도메인(Domain)과 객체 타입(Type) 간의 허용 관계를 정책"**으로 정의한다.

```text
 ┌──────────────────────────────────────────────────────────────────────┐
 │            SELinux Type Enforcement — 도메인-타입 간 접근 제어          │
 ├──────────────────────────────────────────────────────────────────────┤
 │                                                                      │
 │  [정책 예시 — 웹 서버]                                             │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │                                                                 │  │
 │  │  # 웹 서버 프로세스(httpd_t)가 웹 콘텐츠를 읽기           │  │
 │  │  type = httpd_sys_content_t;                                  │  │
 │  │                                                                 │  │
 │  │  allow httpd_t httpd_sys_content_t:file { read open getattr }; │  │
 │  │  allow httpd_t httpd_sys_content_t:dir { search getattr };   │  │
 │  │                                                                 │  │
 │  │  # 웹 서버 프로세스(httpd_t)는 /etc/shadow를 읽을 수 없음   │  │
 │  │  type = shadow_t;                                             │  │
 │  │                                                                 │  │
 │  │  dontaudit httpd_t shadow_t:file read;  (거부 로그 생략)      │  │
 │  │  # (기본적으로 거부, 명시적인 허용 규칙이 없으므로)     │  │
 │  │                                                                 │  │
 │  │  # 웹 서버 프로세스(httpd_t)가 사용자 홈에 쓰기 허용     │  │
 │  │  type = user_home_t;                                          │  │
 │  │                                                                 │  │
 │  │  allow httpd_t user_home_t:file { write create unlink };   │  │
 │  │                                                                 │  │
 │  └────────────────────────────────────────────────────────────────┘  │
 │                                                                      │
 │  [접근 검사 흐름]                                                    │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │                                                                 │  │
 │  │   요청: httpd 프로세스(PID=1234)가 /var/www/html/index.html 읽기│  │
 │  │                                                                 │  │
 │  │   ① 프로세스 보안 컨텍스트 확인                               │  │
 │  │      ┌──────────────────────────────────────────────────┐    │  │
 │  │      │  current->cred:                                     │    │  │
 │  │      │    security: system_u:system_r:httpd_t:s0           │    │  │
 │  │      └──────────────────────────────────────────────────┘    │  │
 │  │                                                                 │  │
 │  │   ② 파일 보안 컨텍스트 확인                                 │  │
 │  │      ┌──────────────────────────────────────────────────┐    │  │
 │  │      │  inode->i_security:                                 │    │  │
 │  │      │    security: system_u:object_r:httpd_sys_content_t:s0 │    │  │
 │  │      └──────────────────────────────────────────────────┘    │  │
 │  │                                                                 │  │
 │  │   ③ AVC(Access Vector Cache) 검색                               │  │
 │  │      ┌──────────────────────────────────────────────────┐    │  │
 │  │      │  Key: {httpd_t, httpd_sys_content_t, file, read}     │    │  │
 │      │  │  → Value: ALLOW (캐시되어 있어 정책 DB 재검색 불필요)   │    │  │
 │  │      └──────────────────────────────────────────────────┘    │  │
 │  │                                                                 │  │
 │  │   ④ 결과: ALLOW                                                │  │
 │  │                                                                 │  │
 │  └────────────────────────────────────────────────────────────────┘  │
 │                                                                      │
 │  [거부 예시 — /etc/shadow]                                        │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │                                                                 │  │
 │  │   요청: httpd 프로세스가 /etc/shadow 읽기                       │  │
 │  │                                                                 │  │
 │  │   ① 프로세스: system_u:system_r:httpd_t:s0                       │  │
 │  │   ② 파일:    system_u:object_r:shadow_t:s0                       │  │
 │  │                                                                 │  │
 │  │   ③ AVC 검색                                                 │  │
 │  │      Key: {httpd_t, shadow_t, file, read}                        │  │
 │  │      → Value: DENY (정책에 허용 규칙 없음)                     │  │
 │  │                                                                 │  │
 │  │   ④ 결과: DENY                                                 │  │
 │  │      audit.log: "avc: denied { read } for pid=1234             │  │
 │  │       comm=httpd path=/etc/shadow scontext=...               │  │
 │  │       tcontext=system_u:object_r:shadow_t:s0"               │  │
 │  │                                                                 │  │
 │  └────────────────────────────────────────────────────────────────┘  │
 │                                                                      │
 └──────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** SELinux의 AVC(Access Vector Cache)는 **"정책 검색 결과를 캐싱"**하여 빠른 검색을 가능하게 한다. `{httpd_t, shadow_t, file, read}` 키로 검색하면 DENY가 반환되며, 이는 정책 데이터베이스에 **"httpd_t가 shadow_t를 읽을 수 있는 허용 규칙이 없음"**을 의미한다. AVC는 캐시되어 있으므로, 두 번째 요청부터는 정책 DB를 재검색하지 않아도 된다. 거부 로그는 `/var/log/audit/audit.log`에 기록되며, `ausearch -m avc -ts recent` 명령으로 확인할 수 있다.

---

### 관리 명령어 및 도구

SELinux를 관리하기 위한 주요 명령어는 다음과 같다.

```text
 ┌──────────────────────────────────────────────────────────────────────┐
 │               SELinux 관리 명령어 및 도구                                 │
 ├──────────────────────────────────────────────────────────────────────┤
 │                                                                      │
 │  [상태 확인]                                                         │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │  $ sestatus                                                     │  │
 │  │  SELinux status:                 enabled                         │  │
 │  │  Current mode:                   enforcing                       │  │
 │  │  Mode from config file:          enforcing                       │  │
 │  │  SELinux fs mount:                /sys/fs/selinux           │  │
 │  │  SELinux root context:             system_u:system_r:s0-s0:c0.c1023│  │
 │  │                                                                 │  │
 │  │  $ getenforce                                                   │  │
 │  │  1  (Enforcing)                                                 │  │
 │  │                                                                 │  │
 │  │  $ ps -Z                                                        │  │
 │  │  system_u:system_r:init_t:s0-s0:c0.c1023 1 1234 ...  │  │
 │  │  system_u:system_r:kernel_t:s0-s0:c0.c1023 2 5678 ... │  │
 │  │  system_u:system_r:httpd_t:s0-s0:c0.c1023 3 9012 ...  │  │
 │  │                                                                 │  │
 │  └────────────────────────────────────────────────────────────────┘  │
 │                                                                      │
 │  [컨텍스트 관리]                                                     │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │  $ ls -Z /etc/shadow                                            │  │
 │  │  -rw-r-----  root root system_u:object_r:shadow_t:s0:c0      │  │
 │  │                                                                 │  │
 │  │  $ chcon -R -t httpd_sys_content_t /var/www/html             │  │
 │  │  $ restorecon -R -v /var/www/html                              │  │  │
 │  │                                                                 │  │
 │  └────────────────────────────────────────────────────────────────┘  │
 │                                                                      │
 │  [정책 관리]                                                         │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │  $ semanage fcontext -a -t httpd_sys_rw_content_t "/web(/.*)?"│  │
 │  │  $ semanage permissive -a httpd_t  (permissive 모드로 변경)   │  │
 │  │  $ semanage port -a -t http_port_t 8080                         │  │
 │  │                                                                 │  │
 │  └────────────────────────────────────────────────────────────────┘  │
 │                                                                      │
 │  [감사 로그 확인]                                                   │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │  $ ausearch -m avc -ts recent | grep denied                    │  │
 │  │  $ ausearch -m avc -ts recent | grep httpd                       │  │
 │  │                                                                 │  │
 │  └────────────────────────────────────────────────────────────────┘  │
 │                                                                      │
 │  [디버깅 도구]                                                       │  │
 │  ┌────────────────────────────────────────────────────────────────┐  │
 │  │  • audit2allow -w /var/log/audit/audit.log (허용 규칙 생성)   │  │
 │  │  • sealert (실시간 SELinux 거부 알림)                        │  │
 │  │  • setroubleshoot (문제 해결 가이드)                           │  │
 │  │                                                                 │  │
 │  └────────────────────────────────────────────────────────────────┘  │
 │                                                                      │
 └──────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** SELinux 관리에서 가장 중요한 것은 **"permissive 모드"**다. 새로운 서비스를 배포할 때는 `setenforce 0`로 permissive 모드로 설정하고, AVC 거부 로그를 분석하여 필요한 허용 규칙을 추가(`audit2allow`)한 후, 다시 `setenforce 1`로 enforcing 모드로 복귀한다. permissive 모드에서는 **"거부 로그만 기록하고 실제로는 차단하지 않는다"**는 점에 주의해야 한다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교 1: SELinux vs AppArmor

| 비교 항목 | SELinux | AppArmor |
|:---|:---|:---|
| **기반 모델** | 레이블 기반(Label-based) | 경로 기반(Path-based) |
| **정책 언어** | TE 언어(C 유사) | 프로필� 경로 기반 |
| **설정 난이도** | 매우 복잡 | 간단 |
| **성능** | AVC 캐시로 빠름 | 경로 검색으로 약간 느림 |
| **주 용도** | 대규모 서버, 클라우드 | 데스크톱, 소규모 서버 |
| **대표 OS** | RHEL, CentOS, Fedora | Ubuntu, Debian, SUSE |
| **학습 곡선** | 가파름 | 완만 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 웹 서버 보안 강화**: Apache httpd가 `/etc/shadow`를 읽지 못하게 하려면:
   ① 웹 서버는 기본적으로 `httpd_t` 도메인으로 실행
   ② `/etc/shadow`는 `shadow_t` 타입
   ③ SELinux 정책에는 `httpd_t`가 `shadow_t`를 읽는 허용 규칙 없음
   → httpd가 탈취되더라도 `/etc/shadow`는 읽을 수 없음

2. **시나리오 — 사용자 홈 공유**: `user_home_t` 타입을 사용하여 사용자 홈 디렉터리(`~/public_html`)을 웹 서버가 읽을 수 있게 하려면:
   ① `semanage fcontext -a -t httpd_sys_content_t "/home/[^/]+/public_html(/.*)?"`
   ② `restorecon -R -v /home`
   → 각 사용자의 `~/public_html`은 웹 서버가 읽을 수 있지만, `/etc/shadow`는 여전히 차단

### 도입 체크리스트
- **기술적**: SELinux가 enforcing 모드인가?(`sestatus`) AVC 거부 로그를 정기적으로 점검하는가?
- **운영·보안적**: 새로운 애플리케이션 배포 시 permissive 모드로 테스트하는가?

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 최적화 전 | 최적화 후 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | DAC만 사용 | SELinux enforcing | **제로데이 공격 벡터 90%+ 차단** |
| **정량** | 웹 서버 침해 시 /etc/shadow 유출 | MAC로 차단 | **데이터 유출 경로 95%+ 감소** |
| **정성** | "보안 레이블 무엇?" 불명확 | 정책 기반 명확한 보안 | **규정 준거(Compliance) 달성** |

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[MAC (Mandatory Access Control)](./616_mac.md)**: SELinux는 MAC의 구현체
- **[LSM (Linux Security Modules)](./619_lsm.md)**: SELinux는 LSM 기반 모듈
- **[AppArmor](./621_apparmor.md)**: LSM 기반 경로 MAC 모듈
- **[Bell-LaPadula 모델](./617_bell_lapadula.md)**: SELinux MLS의 기반 모델
- **[트로이 목마 (Trojan Horse)](./624_trojan_wrapper.md)**: DAC의 취약성, SELinux가 방어

---

## 👶 어린이를 위한 3줄 비유 설명
1. SELinux는 **"국가의 출입 통제 시스템"**이에요. 모든 시민(프로세스)은 신분증(보안 컨텍스트)을 소지하고, 직장별(도메인)로 출입할 수 있는 장소(파일 타입)가 정해져 있어요.
2. 예를 들어 **"웹 서버 직원(httpd_t)은 병원 기록(shadow_t) 구역에는 절대 출입 불가"**예요. 이건 국가 보안법(SELinux 정책)으로 정해진 규칙이라, 웹 서버 관리자(root)라도 바꿀 수 없어요.
3. 그래서 해커가 웹 서버를 해킹해도, 중요한 파일(비밀번호, 시스템 설정)에는 접근할 수 없어요. SELinux는 커널 차원에서 강력한 보안을 제공하는 "국가 보안 시스템"이랍니다!
