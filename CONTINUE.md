# BrainScience PE 콘텐츠 작업 추적

- 2026-03-06: 폴더 구조 키워드 리스트에 맞체 전면 재구성 (16개 과목 모두 완료)

## ⚠️ 작업 원칙 (Rule)

1. **압도적 디테일**: 기술사 답안지 수준의 상세한 백서술. **코드 스니펫**: 가능하면 프로그래밍 코드 스니펫 없음
2. **배치 작업**: 10개 단위 작성 후 반드시 `git push` 및 `CONTINUE.md` 최신화.
3. **체계적 넘버링**: 키워드 리스트`(_keyword_list.md)` 순서를 엄격히 준수.
4. **문서 업데이트**: 진행현황 실시간으로 업데이트.
5. **병렬 처리**: 2-3개 키워드를 병렬로 작성 (한 번에 `git commit` 후 `git push`)

---

## 📊 진행현황 (2026-03-06)

### 1. 컴퓨터구조 (Computer Architecture) - Section 1 진행중
- ✅ 1-45: 전압~클럭 (기초 전기전자 및 디지털 논리회로)
  - 41: 멀티플렉서 (MUX)
  - 42: 디멀티플렉서 (DEMUX)
  - 43: 비교기 (Comparator)
  - 44: 순차 논리회로 (Sequential Logic)
  - 45: 클럭 (Clock)
- 📝 46-64: 래치, 플립플롭, 레지스터, 카운터 (예정)
- 📝 65-80: 메모리, 인터페이스 (예정)

### 2. 운영체제 (Operating System) - Section 1 진행중
- ✅ 1-16: OS 목적~인터럽트 (운영체제 개요 및 아키텍처)
  - 13: 시스템 호출 (System Call)
  - 14: API (Application Programming Interface)
  - 15: ABI (Application Binary Interface)
  - 16: 인터럽트 (Interrupt)
- 📝 17-34: 커널, 부팅, 문맥교환 (예정)

### 3. 데이터통신/네트워크 (Network) - Section 1 진행중
- ✅ 1-4, 7-12: 통신구성요소~동기식전송 (데이터통신 기초)
  - 5: 비트 시간 / 심볼 시간
  - 6: 아날로그 통신 vs 디지털 통신
  - 11: 비동기식 전송 - 시작/정지 비트
  - 12: 동기식 전송 - 문자 동기 / 비트 동기
- 📝 13-25: 대역폭, 채널용량, 잡음 (예정)

### 4. 소프트웨어공학 (Software Engineering) - Section 1 진행중
- ✅ 1-12, 13-17: SE 기초~프로세스 자산
  - 13: ISO/IEC 12207 (소프트웨어 생명주기 공정)
  - 14: ISO/IEC 15504 (SPICE)
  - 15: CMMI (Capability Maturity Model Integration)
  - 16: CMMI 5단계
  - 17: 프로세스 자산 (Process Assets)
- 📝 18-35: PSP/TSP, 재공학, 형상관리 (예정)

### 5. 데이터베이스 (Database) - Section 1 진행중
- ✅ 1-16: DIKW~망형모델 (데이터베이스 기초 및 아키텍처)
  - 12: 메타데이터 (Metadata)
  - 13: 데이터 디렉터리 (Data Directory)
  - 14: 데이터 모델 (Data Model)
  - 15: 계층형 데이터 모델 (Hierarchical Model)
  - 16: 망형 데이터 모델 (Network Model)
- 📝 17-34: 관계형모델, DBMS언어 (예정)

### 6-16. 기타 과목 (예정)
- ICT 융합, 기업시스템, 알고리즘/통계, 보안, AI 등

---

## 📝 다음 작업 (Next Batch)

**우선순위:**
1. CA 46-50: 래치, 플립플롭 (SR, D, JK, T, 마스터-슬레이브)
2. OS 17-21: ISR, 핸들러, 커널 타입 (ISR, Handler, Monolithic, Microkernel)
3. NW 13-17: 대역폭, 채널용량 (Bandwidth, Throughput, Nyquist, Shannon)
4. SE 18-22: PSP/TSP, 재공학 (PSP, TSP, Re-engineering, Reverse Engineering)
5. DB 17-21: 관계형모델, DBMS언어 (Relational Model, DDL, DML, DCL, TCL)

---

## 📈 통계 (Statistics)

| 과목 | 완료 | 진행중 | 전체 | 비율 |
|------|------|--------|------|------|
| CA   | 45   | -      | 1000+ | 4.5% |
| OS   | 16   | -      | 800+  | 2.0% |
| NW   | 12   | -      | 1200+ | 1.0% |
| SE   | 17   | -      | 800+  | 2.1% |
| DB   | 16   | -      | 800+  | 2.0% |
| **합계** | **106** | - | **~4800** | **2.2%** |

---

## 📁 최근 커밋

- `ed3697f` - feat: add 22 PE keywords across 5 subjects (2026-03-06)
- `abc313c` - feat: add 20 PE keywords across 5 subjects (2026-03-06)
