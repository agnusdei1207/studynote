---
title: "Protection & Security"
date: "2026-04-05"
tags:
  - "studynote-operating-system"
weight: 43
---
> **핵심 인사이트**
> 1. OS에서 보호(Protection)는 "합법적인 사용자가 리소스에 올바르게 접근하도록 제어"하는 메커니즘이고, 보안(Security)은 "외부 위협으로부터 시스템을 방어"하는 정책 — 두 개념은 목적과 대상이 다르며 계층적으로 보안이 보호를 포함한다.
> 2. 보호 도메인(Protection Domain)과 접근 행렬(Access Matrix)은 OS 보호의 이론적 기반으로, 주체(Subject)-객체(Object)-권한(Right)의 삼각 관계를 체계적으로 모델링하며 ACL(Access Control List)과 Capability List로 구현된다.
> 3. 링 구조(Ring Architecture)는 x86 CPU의 권한 레벨(Ring 0~3)을 통해 OS 커널(Ring 0)과 사용자 프로그램(Ring 3)을 분리하는 하드웨어 보호 메커니즘으로, 특권 명령어 실행, 메모리 접근, I/O 제어를 계층적으로 제어한다.

---

## Ⅰ. 보호 vs 보안 개념 구분

```
보호 (Protection):
  목적: 프로세스/사용자 간 리소스 격리 및 접근 제어
  대상: 내부 위협 (프로그램 오류, 권한 오남용)
  메커니즘: 하드웨어 + OS 커널 기능
  예: 프로세스 A가 프로세스 B의 메모리 접근 방지

보안 (Security):
  목적: 시스템 전체를 외부 위협으로부터 방어
  대상: 외부 위협 (해커, 악성코드, DoS)
  메커니즘: 인증, 암호화, 방화벽, 감사
  예: 네트워크 침입 탐지, 악성코드 차단

계층 관계:
  보안 (Security) ⊃ 보호 (Protection)

  외부 위협 방어 (보안)
        v
  내부 접근 제어 (보호)
        v
  하드웨어 격리 (링 구조, MMU)

OS 보안 요구사항 (CIA):
  C - Confidentiality (기밀성): 인가된 자만 읽기
  I - Integrity (무결성): 인가된 방식으로만 수정
  A - Availability (가용성): 서비스 지속 제공
```

> 📢 **섹션 요약 비유**: 보호 vs 보안은 건물 내부 잠금 vs 외벽 보안 — 보호는 내부 회의실 문 잠금(내부 격리), 보안은 외부 침입자 방어(외벽, CCTV).

---

## Ⅱ. 보호 도메인과 접근 행렬

```
보호 도메인 (Protection Domain):
  주체(Subject)가 가진 권한 집합

  도메인 D = { (객체, 권한) 쌍의 집합 }

  예:
  Domain 1 (root): { (file1, rw), (file2, rwx), (mem, rw) }
  Domain 2 (user): { (file1, r), (file3, rw) }

접근 행렬 (Access Matrix):
  행: 도메인 (주체)
  열: 객체 (파일, 포트, 메모리 세그먼트)
  셀: 허용 권한 집합

         | 파일A | 파일B | 프린터 | 세그먼트1
---------+-------+-------+--------+----------
도메인1  |  rw   |  rwx  |  print |   rw
도메인2  |   r   |       |        |    r
도메인3  |       |  rx   |  print |

구현 방법:

1. ACL (Access Control List) — 열 기준:
   파일A: { (도메인1, rw), (도메인2, r) }
   장점: 객체별 접근자 목록 관리 쉬움
   단점: 특정 주체의 모든 권한 확인 어려움

2. Capability List — 행 기준:
   도메인1: { (파일A, rw), (파일B, rwx), (프린터, print) }
   장점: 주체 관점에서 권한 관리
   단점: 권한 취소(revoke) 어려움
```

> 📢 **섹션 요약 비유**: 접근 행렬은 학교 열쇠 관리 장부 — ACL은 "이 강의실에 들어갈 수 있는 사람" 목록, Capability는 "이 사람이 열 수 있는 강의실" 목록.

---

## Ⅲ. 링 구조 (Ring Architecture)

```
x86 CPU 링 구조 (Privilege Levels):

Ring 0 — 커널 모드 (Kernel Mode):
  최고 권한
  모든 명령어 실행 가능
  하드웨어 직접 접근
  OS 커널, 디바이스 드라이버 핵심 부분

Ring 1, 2 — (현재 대부분 미사용):
  원래 OS 서비스, 드라이버용
  현대 OS: Ring 0/3 양분 구조

Ring 3 — 사용자 모드 (User Mode):
  최소 권한
  특권 명령어 실행 불가
  I/O 직접 접근 불가
  일반 응용 프로그램

권한 이동:
  Ring 3 -> Ring 0:
    시스템 콜 (INT, SYSCALL 명령어)
    예외 처리 (Exception Handler)
    인터럽트 (Interrupt)

  Ring 0 -> Ring 3:
    IRET, SYSRET 명령어
    스케줄러에 의한 사용자 프로세스 복귀

보호 메커니즘:
  특권 명령어: Ring 0에서만 실행
    (LGDT, LIDT, IN/OUT, HLT, MOV CR0 등)
  메모리: 페이지 테이블로 Ring 3 접근 격리
  I/O: IOPL(I/O Protection Level) 비트로 제어

가상화와 Ring:
  VMware/VirtualBox: Ring -1 (Hypervisor)
  Intel VT-x: VMX root/non-root 모드
```

> 📢 **섹션 요약 비유**: 링 구조는 군대 계급 — Ring 0은 사령관(모든 명령 가능), Ring 3은 일반 병사(기본 임무만). 계급 외 명령 실행 -> 즉시 처벌(예외 발생).

---

## Ⅳ. 보안 위협 유형과 대응

```
OS 보안 위협 분류:

악성코드 (Malware):
  바이러스: 다른 프로그램에 기생, 자기 복제
  웜: 독립 실행, 네트워크 전파
  트로이 목마: 정상 프로그램으로 위장
  랜섬웨어: 파일 암호화 후 몸값 요구

권한 상승 공격:
  버퍼 오버플로우: 스택 리턴 주소 덮어쓰기
  -> 셸코드 실행 -> Root 권한 탈취
  대응: ASLR(주소 공간 레이아웃 랜덤화), DEP(데이터 실행 방지), Stack Canary

레이스 컨디션 (Race Condition):
  TOCTOU(Time-Of-Check-To-Time-Of-Use)
  권한 확인과 실제 사용 사이의 시간차 악용
  대응: 원자적 연산, 잠금(Lock) 사용

사이드 채널 공격:
  Spectre, Meltdown (2018):
    CPU 투기적 실행 -> 캐시 타이밍 측정 -> 비밀 데이터 추출
  대응: OS 패치, KPTI(Kernel Page Table Isolation)

보안 메커니즘:
  인증 (Authentication): 비밀번호, 생체인식, 2FA
  인가 (Authorization): DAC/MAC/RBAC
  감사 (Auditing): 접근 로그, SIEM
  암호화: 파일 시스템 암호화 (BitLocker, LUKS)
```

> 📢 **섹션 요약 비유**: OS 보안 위협은 건물 침입 방법 — 정문 뚫기(인증 우회), 창문 깨기(버퍼 오버플로우), 청소부 위장(트로이 목마), 열쇠 복사(자격증명 도용).

---

## Ⅴ. 실무 시나리오 — Linux SELinux/AppArmor

```
Linux 강제 접근 제어 (MAC) 구현:

DAC (Discretionary Access Control) 한계:
  파일 소유자가 권한 부여 결정
  root 계정 탈취 시 모든 파일 접근 가능
  -> Linux 전통 rwx 권한의 한계

MAC (Mandatory Access Control):
  시스템 정책이 모든 접근 제어
  소유자도 정책 외 권한 부여 불가

SELinux (Security-Enhanced Linux):
  NSA 개발, Red Hat/CentOS/Fedora 기본 탑재
  레이블 기반: 모든 파일/프로세스에 보안 컨텍스트

  컨텍스트 형식: user:role:type:level
  예: system_u:system_r:httpd_t:s0

  정책 유형:
    Enforcing: 정책 위반 = 차단 + 로그
    Permissive: 차단 없음 + 로그만 (개발/디버깅)
    Disabled: 비활성화

AppArmor (Ubuntu/SUSE):
  경로 기반 프로파일
  더 간단, 관리 편이

  /etc/apparmor.d/usr.sbin.nginx 예시:
    /var/www/html/** r,
    /var/log/nginx/** w,
    network tcp,

실무 적용:
  웹서버(Apache/Nginx)에 SELinux 프로파일 적용
  -> 웹 디렉토리 외 파일 접근 자동 차단
  -> 명령 실행(system()) 차단
  -> 취약점 악용 시 피해 최소화 (컨테인먼트)
```

> 📢 **섹션 요약 비유**: SELinux는 회사 보안 시스템 — 팀장(root)도 다른 팀 서버실에 못 들어가는 것처럼, 역할(Role)과 유형(Type)으로 최소 권한 강제.

---

## 📌 관련 개념 맵

```
OS 보호 & 보안
+-- 보호 (Protection)
|   +-- 보호 도메인
|   +-- 접근 행렬 (ACL, Capability)
|   +-- 링 구조 (Ring 0~3)
+-- 보안 (Security)
|   +-- CIA (기밀성, 무결성, 가용성)
|   +-- 위협: 버퍼 오버플로우, TOCTOU, 사이드채널
|   +-- 메커니즘: ASLR, DEP, KPTI
+-- MAC 구현
|   +-- SELinux (Red Hat 계열)
|   +-- AppArmor (Ubuntu 계열)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 OS 보호 (1960s~)]
IBM System/360: 특권 모드 도입
멀틱스: 링 구조 최초 구현
      |
      v
[Unix 권한 모델 (1970s)]
DAC: rwx + 소유자/그룹/기타
      |
      v
[보안 확장 (1980s~90s)]
Orange Book (TCSEC): 보안 등급화
NSA: B3급 OS 연구 -> SELinux 기반
      |
      v
[Linux 보안 (2000s)]
SELinux (2000, 2003 커널 통합)
AppArmor (2006, Ubuntu 통합)
      |
      v
[현재: 컨테이너 보안]
seccomp: 시스템 콜 필터링
cgroups + namespace: 컨테이너 격리
eBPF: 커널 내 보안 프로그램 실행
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 보호는 내부 자물쇠, 보안은 외벽 경비원 — 집 안에서 방마다 잠금(보호), 집 전체를 지키는 경비원(보안)처럼 서로 역할이 달라요!
2. 링 구조는 군대 계급 — Ring 0은 사령관(모든 명령 가능), Ring 3은 일반 병사. 사령관 명령을 병사가 내리면 즉시 경고!
3. SELinux는 초엄격 출입증 시스템 — root 계정을 가져도 출입증(SELinux 컨텍스트)이 없으면 들어갈 수 없어요.
