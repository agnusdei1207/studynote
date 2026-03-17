+++
title = "02. 운영체제 키워드 목록"
date = "2026-03-04"
[extra]
categories = "studynotes-operating-system"
+++

# 운영체제 심화 키워드 목록 (기술사 최적화 800제)

정보관리기술사, 컴퓨터응용시스템기술사 시험에 가장 적합한 범위로 엄선한 800여 개의 운영체제 핵심 및 심화 키워드입니다. 

기본적인 프로세스/메모리 관리를 넘어 **최신 커널 아키텍처, 병렬 처리 및 동기화 심화, 분산 OS, 가상화/컨테이너 시스템, 실시간 운영체제(RTOS), 모바일/임베디드 OS, 그리고 시스템 보안 및 성능 튜닝**에 초점을 맞추어 전면 재구성하였습니다.

---

## 1. 운영체제 개요 및 아키텍처 (80개)
1. 운영체제 (Operating System)의 목적 - 자원 관리, 편의성, 성능 향상
2. 다중 프로그래밍 (Multiprogramming) - CPU 활용도 극대화
3. 시분할 시스템 (Time-sharing System) - 응답 시간 최소화, 인터랙티브
4. 다중 처리 시스템 (Multiprocessing System)
5. 비대칭 다중 처리 (ASMP, Asymmetric Multiprocessing)
6. 대칭 다중 처리 (SMP, Symmetric Multiprocessing)
7. 강결합 시스템 (Tightly Coupled System)
8. 약결합 시스템 (Loosely Coupled System) / 분산 시스템
9. 실시간 시스템 (Real-time System) - Hard vs Soft
10. 임베디드 시스템 (Embedded System)
11. 듀얼 모드 (Dual Mode) - 사용자 모드(User Mode)와 커널 모드(Kernel Mode)
12. 모드 비트 (Mode Bit)
13. 시스템 호출 (System Call) - 커널 서비스 요청 인터페이스
14. API (Application Programming Interface), POSIX 표준
15. ABI (Application Binary Interface)
16. 인터럽트 (Interrupt) 메커니즘
17. 하드웨어 인터럽트 (비동기적)
18. 소프트웨어 인터럽트 / 트랩 (Trap) / 예외 (Exception)
19. 인터럽트 벡터 (Interrupt Vector)
20. 인터럽트 서비스 루틴 (ISR, Interrupt Service Routine)
21. 인터럽트 핸들러 (Interrupt Handler)
22. 커널 (Kernel)의 역할
23. 모놀리식 커널 (Monolithic Kernel) - 리눅스, 고성능
24. 마이크로 커널 (Microkernel) - Mach, Minix, 높은 확장성과 신뢰성
25. 하이브리드 커널 (Hybrid Kernel) - Windows NT, macOS(XNU)
26. 엑소 커널 (Exokernel) - 하드웨어 추상화 최소화
27. 유니커널 (Unikernel) - 라이브러리 OS 기반 단일 주소 공간
28. 부트스트랩 프로그램 (Bootstrap Program)
29. 부트로더 (Bootloader) - GRUB, LILO
30. UEFI (Unified Extensible Firmware Interface) vs BIOS
31. 시스템 생성 (System Generation, SYSGEN)
32. 펌웨어 (Firmware)
33. 문맥 (Context) - CPU 레지스터, 프로세스 상태 등
34. 문맥 교환 (Context Switch) 오버헤드
35. 코어 덤프 (Core Dump)
36. 패닉 (Panic) / 커널 패닉 (Kernel Panic) / 블루 스크린 (BSOD)
37. 시스템 데몬 (System Daemon) / 백그라운드 프로세스
38. init 프로세스 / systemd (리눅스 첫 번째 프로세스)
39. 운영체제 서비스 - UI, 프로그램 실행, I/O 연산, 파일 시스템, 통신
40. 오류 탐지 (Error Detection)
41. 자원 할당 (Resource Allocation)
42. 회계 (Accounting) 및 로깅
43. 보호 (Protection) 및 보안 (Security)
44. 명령어 인터프리터 (Command Interpreter) / 쉘 (Shell)
45. 클러스터 시스템 (Clustered System) - 고가용성(HA), 병렬 컴퓨팅
46. 핫 스탠바이 (Hot Standby) / 콜드 스탠바이 (Cold Standby)
47. 분산 잠금 관리자 (DLM, Distributed Lock Manager)
48. 스토리지 영역 네트워크 (SAN) 연동
49. 클라이언트-서버 시스템 (Client-Server System)
50. P2P (Peer-to-Peer) 시스템
51. 그리드 컴퓨팅 (Grid Computing)
52. 클라우드 컴퓨팅 (Cloud Computing) OS 관점
53. 가상화 (Virtualization) 아키텍처
54. 하이퍼바이저 (Hypervisor) / VMM
55. 베어메탈 (Bare-metal) 하이퍼바이저 (Type 1)
56. 호스트형 하이퍼바이저 (Type 2)
57. 전가상화 (Full Virtualization) - 이진 변환 (Binary Translation)
58. 반가상화 (Paravirtualization) - 하이퍼콜 (Hypercall)
59. 하드웨어 보조 가상화 (Intel VT-x, AMD-V)
60. 컨테이너 (Container) 기술 기반 - OS 수준 가상화
61. 네임스페이스 (Namespace) - 자원 격리
62. 컨트롤 그룹 (cgroups) - 자원 할당 제어
63. 도커 (Docker) 아키텍처
64. 루트 파일 시스템 (Root Filesystem) / 오버레이 파일 시스템 (OverlayFS)
65. 시스템 콜 래퍼 (System Call Wrapper)
66. VFS (Virtual File System)
67. 모듈 적재 (Loadable Kernel Modules, LKM)
68. 동적 커널 패치 (Live Patching) - kpatch, kGraft
69. BPF (Berkeley Packet Filter) / eBPF (Extended BPF) - 커널 내 샌드박스 프로그램
70. 하드웨어 추상화 계층 (HAL, Hardware Abstraction Layer)
71. 운영체제 타이머 (Timer) - 시스템 클럭, 카운터
72. 타이머 인터럽트 - 선점형 스케줄링의 기반
73. 틱 (Tick) / 지피스 (Jiffies)
74. 틱리스 커널 (Tickless Kernel) - 전력 소모 감소
75. ACPI (Advanced Configuration and Power Interface)
76. 시스템 전원 상태 (S-States, S0~S5)
77. 프로세서 전원 상태 (C-States)
78. 프로세서 성능 상태 (P-States)
79. 운영체제 프로파일링 및 트레이싱 도구 (perf, ftrace, DTrace)
80. 시스템 호출 차단 (Seccomp)

## 2. 프로세스와 스레드 (80개)
81. 프로그램 (Program) vs 프로세스 (Process)
82. 프로세스 메모리 구조 - Text(Code), Data, BSS, Heap, Stack
83. BSS (Block Started by Symbol) 영역 - 초기화되지 않은 전역 변수
84. 힙 (Heap) 영역 - 동적 할당 (malloc/free)
85. 스택 (Stack) 영역 - 지역 변수, 매개변수, 리턴 주소
86. 프로세스 상태 (Process State)
87. 생성 (New) -> 준비 (Ready) -> 실행 (Running) -> 대기 (Waiting/Blocked) -> 종료 (Terminated)
88. 준비 큐 (Ready Queue)
89. 대기 큐 (Wait Queue / Device Queue)
90. 프로세스 제어 블록 (PCB, Process Control Block) / 태스크 제어 블록 (TCB)
91. PCB 요소 - PID, 상태, PC, 레지스터, 스케줄링 정보, 메모리 정보, 회계 정보, I/O 상태 정보
92. 스레드 (Thread) - 경량 프로세스 (LWP)
93. 스레드의 자원 공유 - Code, Data, Heap, 열린 파일
94. 스레드의 독립 자원 - Thread ID, PC, 레지스터 집합, 스택
95. 다중 스레드 (Multithreading)의 장점 - 응답성, 자원 공유, 경제성, 다중 처리기 활용
96. 사용자 수준 스레드 (User-level Thread) - 스레드 라이브러리가 관리, 커널 비개입
97. 커널 수준 스레드 (Kernel-level Thread) - OS가 직접 관리
98. 다대일 (Many-to-One) 스레드 모델
99. 일대일 (One-to-One) 스레드 모델
100. 다대다 (Many-to-Many) 스레드 모델
101. 두 수준 (Two-level) 모델
102. 암묵적 스레딩 (Implicit Threading) - 스레드 풀, OpenMP, Grand Central Dispatch(GCD)
103. 스레드 풀 (Thread Pool)
104. 프로세스 생성 (Process Creation) - fork(), exec() 시스템 콜
105. 부모 프로세스 (Parent Process) / 자식 프로세스 (Child Process)
106. Copy-on-Write (COW) - fork() 최적화 기법
107. 프로세스 종료 (Process Termination) - exit(), wait()
108. 연쇄적 종료 (Cascading Termination)
109. 좀비 프로세스 (Zombie Process) - 종료되었으나 부모가 wait()하지 않은 상태
110. 고아 프로세스 (Orphan Process) - 부모가 먼저 종료된 상태 (init 프로세스가 입양)
111. 스레드 취소 (Thread Cancellation) - 비동기식 취소, 지연 취소
112. 취소 점 (Cancellation Point)
113. 스레드 로컬 저장소 (TLS, Thread-Local Storage)
114. 스케줄러 액티베이션 (Scheduler Activation) / 경량 프로세스(LWP)
115. 상향 호출 (Upcall)
116. 협력적 프로세스 (Cooperating Process) vs 독립적 프로세스 (Independent Process)
117. 프로세스 간 통신 (IPC, Inter-Process Communication)
118. 공유 메모리 (Shared Memory) 방식 - 빠름, 동기화 문제 발생
119. 메시지 전달 (Message Passing) 방식 - 안전, 커널 개입(시스템 콜) 오버헤드
120. 직접 통신 (Direct Communication) - 수신자 명시
121. 간접 통신 (Indirect Communication) - 메일박스/포트 사용
122. 동기식 통신 (Blocking) vs 비동기식 통신 (Non-blocking)
123. 파이프 (Pipe) - 단방향(Half-duplex), 부모-자식 간
124. 지명 파이프 (Named Pipe / FIFO) - 양방향 가능, 부모-자식 관계 무관
125. 소켓 (Socket) 통신 - 네트워크, 서로 다른 시스템 간 통신
126. RPC (Remote Procedure Call) - 분산 시스템 함수 호출
127. XDR (External Data Representation)
128. 마샬링 (Marshalling) / 언마샬링 (Unmarshalling)
129. 로컬 프로시저 호출 (LPC, Local Procedure Call) / ALPC (Windows)
130. 신호 (Signal) - 소프트웨어 인터럽트 방식 IPC (kill, SIGINT, SIGKILL)
131. 메모리 맵 파일 (Memory-Mapped File, mmap) 기반 IPC
132. 시스템 V IPC - 공유 메모리, 세마포어, 메시지 큐
133. POSIX IPC
134. D-Bus (Desktop Bus) - 리눅스 데스크톱 환경 IPC
135. 안드로이드 바인더 (Android Binder) - 객체 지향적 경량 IPC
136. 좀비 스레드 (Zombie Thread)
137. 멀티프로세스 아키텍처 (크롬 브라우저 등)
138. 멀티스레드 아키텍처 오버헤드 (락 경합 등)
139. 액터 모델 (Actor Model) - Erlang, Akka 동시성 모델
140. 고루틴 (Goroutine) - Go 언어의 경량 스레드 (M:N 모델)
141. 코루틴 (Coroutine)
142. 이벤트 루프 (Event Loop) 기반 비동기 처리 (Node.js)
143. 컨텍스트 스위칭 최소화를 위한 스레드 고정 (Thread Affinity/Pinning)
144. CPU 친화성 (CPU Affinity) - Soft Affinity vs Hard Affinity
145. NUMA-인식 스레드 스케줄링
146. 실시간 프로세스 (Real-time Process)
147. 스레드 안전 (Thread-safe) 함수 및 라이브러리
148. 재진입 가능 코드 (Reentrant Code / Pure Code)
149. 클론 (clone) 시스템 콜 (리눅스 프로세스/스레드 생성 범용 API)
150. 태스크 (Task) - 리눅스의 프로세스/스레드 통일된 용어
151. 네임스페이스 격리 프로세스
152. 데몬화 (Daemonization) 절차 - fork, setsid, umask, 파일 디스크립터 닫기
153. 좀비 사냥 (Reaping Zombies)
154. 스레드 스택 오버플로우 방지 (Guard Page)
155. 동적 링킹 프로세스 (ld.so) 로딩 과정
156. 환경 변수 (Environment Variables) 상속
157. OOM (Out Of Memory) Killer 프로세스 종료 정책
158. oom_score_adj - OOM 킬러 우선순위 조정
159. 프로세스 그룹 (Process Group)
160. 세션 (Session) 및 제어 터미널 (Controlling Terminal)

## 3. CPU 스케줄링 (60개)
161. 단기 스케줄러 (Short-term Scheduler) / CPU 스케줄러
162. 중기 스케줄러 (Medium-term Scheduler) - 스와핑 (Swapping)
163. 장기 스케줄러 (Long-term Scheduler) - 다중 프로그래밍 정도 조절
164. I/O 바운드 프로세스 (I/O Bound Process)
165. CPU 바운드 프로세스 (CPU Bound Process)
166. 선점형 스케줄링 (Preemptive Scheduling)
167. 비선점형 스케줄링 (Non-preemptive Scheduling)
168. 디스패처 (Dispatcher) - 문맥 교환 수행 모듈
169. 디스패치 지연 (Dispatch Latency)
170. 스케줄링 기준 (Scheduling Criteria) - CPU 이용률, 처리량, 반환시간, 대기시간, 응답시간
171. CPU 이용률 (CPU Utilization) / 처리량 (Throughput)
172. 반환 시간 (Turnaround Time) / 대기 시간 (Waiting Time) / 응답 시간 (Response Time)
173. FCFS (First-Come, First-Served) 스케줄링 - 비선점
174. 호위 효과 (Convoy Effect) - FCFS의 단점
175. SJF (Shortest Job First) 스케줄링 - 최적의 평균 대기 시간
176. 지수 평균법 (Exponential Averaging) - 다음 CPU 버스트 길이 예측
177. SRTF (Shortest Remaining Time First) 스케줄링 - SJF의 선점형 버전
178. 라운드 로빈 (Round Robin, RR) 스케줄링 - 시분할 시스템, 선점형
179. 시간 할당량 (Time Quantum / Time Slice) 의 크기와 문맥 교환 오버헤드
180. 우선순위 스케줄링 (Priority Scheduling) - 무한 대기 문제 발생 가능
181. 기아 상태 (Starvation / Indefinite Blocking)
182. 노화 (Aging) - 기아 상태 해결책 (우선순위 점진적 상승)
183. 다단계 큐 스케줄링 (Multilevel Queue Scheduling)
184. 큐 간 스케줄링 (고정 우선순위 vs 시간 할당)
185. 다단계 피드백 큐 스케줄링 (Multilevel Feedback Queue, MLFQ) - 프로세스의 큐 이동 허용
186. MLFQ 파라미터 - 큐의 개수, 알고리즘, 승급/강등 기준
187. HRN (Highest Response Ratio Next) 스케줄링 - (대기시간+서비스시간)/서비스시간
188. 보장 스케줄링 (Guaranteed Scheduling)
189. 복권 스케줄링 (Lottery Scheduling) - 확률적 스케줄링
190. 공평 몫 스케줄링 (Fair-share Scheduling)
191. 스레드 스케줄링 - 프로세스 경쟁 범위(PCS) vs 시스템 경쟁 범위(SCS)
192. LWP 디스패치
193. 다중 처리기 스케줄링 (Multiprocessor Scheduling)
194. 비대칭 다중 처리 (ASMP) 스케줄링
195. 대칭 다중 처리 (SMP) 스케줄링
196. 부하 균등화 (Load Balancing) - Push Migration vs Pull Migration
197. 프로세서 친화성 (Processor Affinity) - 캐시 최적화
198. 멀티코어 스케줄링 (Multicore Scheduling) - 메모리 스톨 (Memory Stall) 대응
199. 하이퍼스레딩 (Hyper-threading) / SMT (Simultaneous Multithreading) 스케줄링
200. 이기종 다중 처리기 스케줄링 (HMP) - ARM big.LITTLE 구조
201. 실시간 스케줄링 (Real-time Scheduling)
202. 연성 실시간 (Soft Real-time) 시스템
203. 경성 실시간 (Hard Real-time) 시스템
204. 지연 시간 (Latency) - 인터럽트 지연 (Interrupt Latency) + 디스패치 지연 (Dispatch Latency)
205. 주기적 태스크 (Periodic Task) - 주기(p), 마감시간(d), 실행시간(t)
206. RM (Rate-Monotonic) 스케줄링 - 주기가 짧을수록 높은 우선순위 (정적 우선순위)
207. EDF (Earliest Deadline First) 스케줄링 - 마감시간이 빠를수록 높은 우선순위 (동적 우선순위)
208. 비례 배분 스케줄링 (Proportionate Share Scheduling)
209. POSIX 스케줄링 API - SCHED_FIFO, SCHED_RR, SCHED_OTHER
210. 리눅스 O(1) 스케줄러 - 두 개의 배열 (Active, Expired)
211. 리눅스 CFS (Completely Fair Scheduler) - 가상 실행 시간 (vruntime) 기반, 레드-블랙 트리 사용
212. 대상 지연 시간 (Target Latency) / 최소 입자 (Minimum Granularity)
213. 윈도우 스케줄링 - 디스패처 (Dispatcher), 우선순위 기반 선점형, 32단계 우선순위
214. 동적 우선순위 승급 (Priority Boost) - I/O 완료 시, GUI 전경 프로세스
215. 태스크 스케줄링의 캐시 일관성 (Cache Coherence) 문제
216. 에너지 인지 스케줄링 (Energy-Aware Scheduling, EAS)
217. 코-스케줄링 (Co-scheduling / Gang Scheduling) - 밀접한 스레드 동시 스케줄링
218. 컨테이너 스케줄링 (cgroups cpu.shares, cpu.cfs_quota_us)
219. 실시간 리눅스 (PREEMPT_RT 패치)
220. 무중단 라이브 마이그레이션 스케줄링 고려사항

## 4. 병행성 (Concurrency) 및 동기화 (70개)
221. 경쟁 조건 (Race Condition) - 실행 순서에 따라 결과가 달라지는 현상
222. 임계 구역 (Critical Section) - 공유 데이터 접근 코드 영역
223. 임계 구역 문제 해결의 3조건 - 상호 배제(Mutual Exclusion), 진행(Progress), 한정된 대기(Bounded Waiting)
224. 선점형 커널 (Preemptive Kernel) vs 비선점형 커널 (Non-preemptive Kernel)
225. 피터슨의 해결책 (Peterson's Algorithm) - 플래그(flag)와 턴(turn) 변수 활용, 2 프로세스 한정
226. 메모리 장벽 (Memory Barrier / Memory Fence) - 메모리 연산 순서 보장 명령어
227. 하드웨어 명령어 기반 동기화
228. Test-and-Set 명령어 - 원자적(Atomic) 읽기-수정
229. Compare-and-Swap (CAS) 명령어
230. 원자적 변수 (Atomic Variable) - Lock-free 프로그래밍 기초
231. 뮤텍스 락 (Mutex Lock / Mutual Exclusion Lock)
232. acquire() / release() 함수
233. 스핀락 (Spinlock) - 바쁜 대기(Busy Waiting), 다중 코어에서 문맥 교환 오버헤드 없음
234. 세마포어 (Semaphore) - S 정수 변수, wait(P), signal(V) 원자적 연산
235. 이진 세마포어 (Binary Semaphore) = 뮤텍스와 유사
236. 카운팅 세마포어 (Counting Semaphore) - 유한한 자원 풀 관리
237. 블로킹 세마포어 - 대기 큐 (Sleep & Wakeup) 사용, 바쁜 대기 없음
238. 모니터 (Monitor) - 추상 자료형 구조, 상호 배제 자동 보장 (High-level 구조)
239. 조건 변수 (Condition Variable) - x.wait(), x.signal()
240. 모니터 시그널 의미론 - Signal and Wait vs Signal and Continue
241. 라이브락 (Livelock) - 진행은 하나 유효한 작업 불가 (양보만 반복)
242. 우선순위 역전 (Priority Inversion) - 하위 프로세스가 락을 쥐고 있어 상위 프로세스 대기
243. 우선순위 상속 (Priority Inheritance Protocol) - 락을 쥔 프로세스에 임시로 우선순위 부여
244. 우선순위 올림 (Priority Ceiling Protocol)
245. 고전적 동기화 문제들
246. 유한 버퍼 문제 (Bounded-Buffer Problem) / 생산자-소비자 (Producer-Consumer) 문제
247. 독자-저자 문제 (Readers-Writers Problem) - 제1유형(독자 우선), 제2유형(저자 우선)
248. 식사하는 철학자 문제 (Dining-Philosophers Problem) - 교착상태 및 기아 상태 예방
249. 자바 동기화 - synchronized 키워드, 모니터 락, wait()/notify()
250. Pthreads 동기화 - pthread_mutex_t, pthread_cond_t, 스핀락, 배리어
251. 윈도우 동기화 - 크리티컬 섹션 객체(유저모드), 디스패처 객체(커널모드 - 이벤트, 뮤텍스, 세마포어)
252. 이벤트 객체 (Event Object) - 스레드 간 신호 전달
253. 리눅스 동기화 - 원자적 정수, 스핀락, 세마포어, 락 메커니즘
254. RCU (Read-Copy-Update) - 리눅스 고성능 동기화 (읽기는 락 프리, 쓰기는 복사 후 갱신)
255. SeqLock (순차 락) - 읽기-쓰기 락의 대안, 카운터 기반
256. 락-프리 (Lock-free) 자료구조 - CAS 연산 적극 활용
257. 웨이트-프리 (Wait-free) 알고리즘
258. 스케줄러 일드 (sched_yield) - 락 경합 시 자발적 CPU 양보
259. ABA 문제 - CAS 연산 시 값이 변경되었다가 원복된 것을 인지하지 못하는 오류
260. ABA 문제 해결책 - 태그/버전 관리
261. 장벽 (Barrier) 동기화 - 여러 스레드가 특정 지점에 도달할 때까지 대기
262. 양방향 랑데부 (Rendezvous)
263. 티켓 락 (Ticket Lock) - FIFO 보장 스핀락
264. 큐잉 스핀락 (MCS Lock / qspinlock) - NUMA 환경 스핀락 최적화
265. 낙관적 병행성 제어 (Optimistic Concurrency Control)
266. 비관적 병행성 제어 (Pessimistic Concurrency Control)
267. 원자적 트랜잭션 (Atomic Transaction) 개념
268. 소프트웨어 트랜잭셔널 메모리 (STM)
269. 하드웨어 트랜잭셔널 메모리 (HTM - Intel TSX)
270. 락 엘리전 (Lock Elision) - 하드웨어 지원 락 우회
271. 스레드 풀 스케줄링 락 경합 (Work Stealing)
272. 더블 체크드 락킹 (Double-Checked Locking) 안티패턴 및 해결 (volatile)
273. 세큐어 코딩에서의 동기화 약점 (TOCTOU: Time of Check to Time of Use)
274. 임계 구역 크기 최소화 기법
275. 락 경합 (Lock Contention) 모니터링 도구
276. 데드락 회피를 위한 Lock Hierarchy (락 순서화)
277. 세마포어를 이용한 순서 제어 (Ordering)
278. 이진 세마포어 vs 뮤텍스 차이 (소유권 유무)
279. 재진입 가능 락 (Reentrant Lock / Recursive Lock)
280. 읽기-쓰기 락 (Read-Write Lock) - 다중 읽기 허용, 쓰기 배타적

## 5. 교착 상태 (Deadlock) (40개)
281. 교착 상태 (Deadlock) 정의 - 대기 중인 프로세스들이 자원을 점유한 채로 결코 일어나지 않을 사건을 기다리는 상태
282. 교착 상태 발생 4가지 필요조건 (모두 만족해야 발생)
283. 상호 배제 (Mutual Exclusion) - 자원은 비공유 모드로만 사용 가능
284. 점유하며 대기 (Hold-and-Wait) - 자원을 보유한 상태로 다른 자원 대기
285. 비선점 (No Preemption) - 다른 프로세스의 자원을 강제로 뺏을 수 없음
286. 순환 대기 (Circular Wait) - 대기 그래프가 사이클(Cycle)을 형성
287. 자원 할당 그래프 (Resource-Allocation Graph) - 정점(프로세스, 자원)과 간선(요청, 할당)
288. 단일 인스턴스 자원 환경 - 사이클 존재 = 교착 상태
289. 다중 인스턴스 자원 환경 - 사이클 존재 != 교착 상태 (필요 조건일 뿐)
290. 교착 상태 처리 방법 3가지 - 예방/회피, 탐지/복구, 무시
291. 타조 알고리즘 (Ostrich Algorithm) - 대부분의 OS가 채택하는 무시 전략
292. 교착 상태 예방 (Deadlock Prevention) - 4조건 중 하나를 원천적 부정 (효율성 매우 낮음)
293. 상호 배제 부정 - 모든 자원 공유 (현실성 없음)
294. 점유 대기 부정 - 실행 전 모든 자원 일괄 할당, 또는 자원 없을 때만 요청 (기아 가능성, 자원 낭비)
295. 비선점 부정 - 자원 요청 대기 시 보유 자원 강제 반납
296. 순환 대기 부정 - 자원에 고유 번호(순서) 부여, 오름차순으로만 요청 (가장 현실적 예방책)
297. 교착 상태 회피 (Deadlock Avoidance) - 실행 전 자원 할당 상태를 검사하여 안전한 경우에만 승인
298. 안전 상태 (Safe State) - 모든 프로세스가 정상 종료될 수 있는 안전 순서(Safe Sequence)가 존재
299. 불안전 상태 (Unsafe State) - 교착 상태가 발생할 가능성이 있는 상태
300. 단일 인스턴스 환경의 회피 - 자원 할당 그래프 알고리즘 (예약 간선/Claim Edge 활용)
301. 다중 인스턴스 환경의 회피 - 은행원 알고리즘 (Banker's Algorithm, 에츠허르 데이크스트라 제안)
302. 은행원 알고리즘 자료구조 - Available, Max, Allocation, Need 행렬
303. 은행원 알고리즘 한계 - 프로세스 수, 최대 자원량 사전 숙지 불가, 오버헤드 큼
304. 교착 상태 탐지 (Deadlock Detection) - 알고리즘을 주기적으로 실행하여 데드락 확인
305. 대기 그래프 (Wait-for Graph) - 자원 정점을 제거하고 프로세스 간 간선만 남긴 그래프 (단일 자원 탐지용)
306. 탐지 알고리즘의 오버헤드 - 언제, 얼마나 자주 실행할 것인가?
307. 교착 상태 복구 (Recovery from Deadlock) - 데드락 해소 조치
308. 프로세스 종료 방식 - 교착 상태 프로세스 전체 강제 종료 (Abort all)
309. 프로세스 순차 종료 방식 - 하나씩 종료하며 사이클 해소 여부 확인
310. 종료 대상 선택 (희생자 선택) 기준 - 프로세스 중요도, 연산 시간, 보유 자원 수
311. 자원 선점 (Resource Preemption) 방식 - 다른 프로세스의 자원을 강제로 뺏음
312. 희생자 선택 (Victim Selection) 최소 비용 기준
313. 후퇴 (Rollback) - 프로세스를 안전한 상태로 롤백 후 재시작
314. 기아 상태 (Starvation) 발생 방지 (희생자 선택에 횟수 제한)
315. 라이브락 (Livelock)과 교착 상태의 차이점
316. 동기화 결함 (순환 의존성) 코드 레벨 디버깅 기법
317. 락 오더링 (Lock Ordering) 다이나믹 검증 도구 (Lockdep in Linux)
318. 분산 시스템에서의 교착 상태 탐지 - 분산 교착 상태 그래프
319. 교착 상태 예방 메커니즘을 위한 타임아웃 (Timeout) 활용
320. 2단계 잠금 프로토콜 (2PL)과 데드락 (데이터베이스 연관)

## 6. 메인 메모리 관리 (70개)
321. 메모리 계층 구조 (Memory Hierarchy)와 레지스터-캐시-메인메모리 접근
322. 논리 주소 (Logical/Virtual Address) - CPU가 생성하는 주소
323. 물리 주소 (Physical Address) - 메모리 장치가 보는 주소
324. 주소 바인딩 (Address Binding) 3단계 시점
325. 컴파일 시간 바인딩 (Compile Time) - 절대 코드 (Absolute Code) 생성
326. 적재 시간 바인딩 (Load Time) - 재배치 가능 코드 (Relocatable Code)
327. 실행 시간 바인딩 (Execution Time) - 실행 중 주소 변경, MMU 필요 (현대 OS 기본)
328. MMU (Memory-Management Unit) - 논리 주소를 물리 주소로 동적 변환하는 하드웨어
329. 베이스 레지스터 (Base/Relocation Register) - 물리 시작 주소 보유
330. 한계 레지스터 (Limit Register) - 메모리 보호, 주소 범위 검사
331. 동적 적재 (Dynamic Loading) - 루틴 호출 시점에 메모리 적재 (효율성)
332. 동적 연결 (Dynamic Linking) - 실행 시점에 라이브러리 연결 (.dll, .so)
333. 공유 라이브러리 (Shared Library) 스터브 (Stub) 코드
334. 정적 연결 (Static Linking)
335. 스와핑 (Swapping) - 메모리 부족 시 프로세스를 디스크 백킹 스토어(Backing Store)로 쫓아냄
336. 스왑 아웃 (Swap out) / 스왑 인 (Swap in)
337. 표준 스와핑 (전체 프로세스) vs 페이징 시스템 스와핑 (페이지 단위)
338. 연속 메모리 할당 (Contiguous Memory Allocation)
339. 고정 분할 방식 (Fixed Partition)
340. 가변 분할 방식 (Variable Partition)
341. 내부 단편화 (Internal Fragmentation) - 할당된 공간 내 남는 공간
342. 외부 단편화 (External Fragmentation) - 가용 공간은 충분하나 불연속적이라 할당 불가
343. 동적 메모리 할당 문제 (가변 분할 배치 알고리즘)
344. 최초 적합 (First-Fit) - 첫 번째 충분한 공간 할당 (속도 빠름)
345. 최적 적합 (Best-Fit) - 가장 크기가 비슷한 공간 (자투리 최소화, 검색 시간 소요)
346. 최악 적합 (Worst-Fit) - 가장 큰 공간 할당 (큰 가용 공간 남김)
347. 압축 (Compaction) - 외부 단편화 해결, 동적 재배치 시에만 가능, 오버헤드 막심
348. 버디 시스템 (Buddy System) 할당기 - 2의 승수로 분할 및 병합 (외부 단편화 절충)
349. 슬랩 할당기 (Slab Allocator) - 커널 객체 캐싱, 단편화 방지 및 속도 향상
350. 비연속 메모리 할당 (Non-contiguous Memory Allocation)
351. 페이징 (Paging) - 물리 메모리를 프레임(Frame), 논리 메모리를 페이지(Page)로 고정 크기 분할
352. 페이지 크기 (Page Size) - 주로 4KB. 커지면 내부 단편화 증가, 테이블 크기 감소
353. 페이지 테이블 (Page Table) - 페이지 번호를 프레임 번호로 매핑
354. PTBR (Page-Table Base Register) / PTLR (Page-Table Length Register)
355. 페이징의 메모리 보호 - 유효-무효 비트 (Valid-Invalid Bit)
356. 페이징에서의 공유 페이지 (Shared Pages) - 읽기 전용 코드(Reentrant code) 공유
357. TLB (Translation Look-aside Buffer) - 주소 변환 캐시(SRAM 연관 메모리 하드웨어)
358. TLB 적중 (TLB Hit) / TLB 미스 (TLB Miss)
359. TLB 적중률 (Hit Ratio) / 실질 메모리 접근 시간 (EAT, Effective Access Time)
360. ASID (Address-Space Identifier) - TLB 내 프로세스 식별, 플러시(Flush) 최소화
361. 다단계 페이징 (Hierarchical Paging) - 페이지 테이블 크기 문제 해결 (2단계, 3단계...)
362. 해시 페이지 테이블 (Hashed Page Table) - 주소 공간이 64비트 이상일 때 사용
363. 역 페이지 테이블 (Inverted Page Table) - 시스템 내 단 하나의 페이지 테이블, 프레임 중심
364. 세그멘테이션 (Segmentation) - 사용자 관점의 가변 크기 논리적 단위(함수, 객체) 분할
365. 세그먼트 테이블 (Segment Table) - 기준(Base) 주소와 한계(Limit) 길이
366. 세그멘테이션과 외부 단편화 (가변 크기이므로 재발생)
367. 세그멘테이션 기반 페이징 (Paged Segmentation) - 인텔 x86 아키텍처 (세그먼트를 다시 페이지로)
368. 커널 메모리 할당 방식 (kmalloc, vmalloc)
369. 메모리 풀 (Memory Pool) 기법
370. 파편화 관리 및 조각 모음 - 리눅스 메모리 컴팩션 (Memory Compaction)
371. 거대 페이지 (Huge Pages / Transparent Huge Pages) - TLB 미스 감소
372. 아키텍처 종속적인 MMU 인터페이스
373. ARM / x86의 메모리 매핑 아키텍처 차이
374. 주소 공간 무작위 배치 (ASLR, Address Space Layout Randomization)
375. 메모리 보호 키 (Memory Protection Keys)
376. 캐시 인식 데이터 구조 (Cache-aware Data Structures)
377. NUMA (Non-Uniform Memory Access) 아키텍처와 메모리 할당 정책
378. 로컬 노드 할당 vs 인터리브 할당
379. 캐시 컬러링 (Cache Coloring) / 페이지 컬러링
380. 가비지 컬렉션 (Garbage Collection) 기초 - 참조 카운팅, Mark-and-Sweep

## 7. 가상 메모리 관리 (60개)
381. 가상 메모리 (Virtual Memory) 개념 - 물리 메모리보다 큰 프로그램 실행 가능
382. 가상 주소 공간 (Virtual Address Space)
383. 요구 페이징 (Demand Paging) - 필요한 페이지만 메모리에 적재
384. 순수 요구 페이징 (Pure Demand Paging) - 시작할 때 아무것도 안 올림
385. 선행 페이징 (Prepaging) - 페이지 부재 감소를 위해 미리 묶어 올림
386. 유효-무효 비트 (Valid-Invalid Bit) - 적재 여부 표시
387. 페이지 부재 (Page Fault) - 무효 페이지 접근 시 발생하는 트랩(인터럽트)
388. 페이지 부재 처리 과정 6단계 (OS 트랩, 레지스터 저장, 디스크 읽기, 문맥교환 등)
389. 페이지 부재율 (Page Fault Rate) 와 실질 접근 시간 (EAT) 성능 관계
390. 스왑 공간 (Swap Space) / 베이킹 스토어 (Backing Store)
391. 익명 메모리 (Anonymous Memory) - 파일 시스템과 무관한 힙/스택 데이터 (스왑 영역 사용)
392. 파일 지원 메모리 (File-backed Memory) - 실행 파일, 공유 라이브러리
393. 쓰기 시 복사 (COW, Copy-on-Write) - fork() 시 자원 공유하다 쓸 때 페이지 복제
394. vfork() - COW 조차 없는 초경량 포크 (즉시 exec() 호출 조건)
395. 페이지 교체 (Page Replacement)의 필요성 - 프레임 가용 공간 부족 시 (Over-allocation)
396. 변경 비트 (Modify Bit / Dirty Bit) - 교체 시 디스크 기록 여부 결정, 디스크 I/O 최적화
397. 프레임 할당 (Frame Allocation) 알고리즘
398. 균등 할당 (Equal Allocation) vs 비례 할당 (Proportional Allocation)
399. 전역 교체 (Global Replacement) - 전체 프로세스 프레임 대상 (처리량 높음, 주로 사용)
400. 지역 교체 (Local Replacement) - 자신의 프레임 풀 내에서만 교체
401. 페이지 교체 알고리즘 (Page Replacement Algorithms)
402. 최적 교체 알고리즘 (OPT, Optimal) - 앞으로 가장 오랫동안 안 쓸 페이지 교체 (구현 불가, 비교 기준)
403. 벨라디의 모순 (Belady's Anomaly) - 프레임을 늘렸는데 오히려 페이지 부재가 증가하는 현상
404. FIFO (First-In, First-Out) 교체 - 가장 먼저 들어온 페이지 교체 (벨라디 모순 발생)
405. LRU (Least Recently Used) 교체 - 가장 오랫동안 사용되지 않은 페이지 교체 (타임스탬프, 스택 하드웨어 지원 필요)
406. LRU 근사 알고리즘 (LRU Approximation) - 참조 비트 (Reference Bit) 사용
407. 2차 기회 알고리즘 (Second-Chance / Clock Algorithm) - 참조 비트가 1이면 0으로 바꾸고 통과, 0이면 교체
408. 개선된 2차 기회 알고리즘 - 참조 비트와 변경 비트의 조합 (0,0 -> 0,1 -> 1,0 -> 1,1 우선순위 교체)
409. LFU (Least Frequently Used) 알고리즘 - 참조 횟수가 가장 적은 페이지 교체
410. MFU (Most Frequently Used) 알고리즘
411. 에이징 (Aging) 기반 페이지 교체 로직
412. 스래싱 (Thrashing) - 프로세스가 실제 실행보다 페이징(스와핑)에 더 많은 시간을 보내는 현상
413. 다중 프로그래밍 정도 (Degree of Multiprogramming)와 CPU 이용률 관계 그래프
414. 스래싱 원인 - 각 프로세스가 필요로 하는 최소 프레임 확보 실패
415. 지역성 모델 (Locality Model) - 시간적, 공간적 지역성
416. 워킹 셋 모델 (Working-Set Model) - 특정 시간 구간(윈도우) 동안 참조된 페이지 집합 보장
417. 페이지 부재 빈도 (PFF, Page-Fault Frequency) 모델 - 상한/하한 설정하여 동적 프레임 할당 조절
418. 메모리 매핑 파일 (Memory-Mapped Files, mmap)
419. 파일 I/O를 메모리 접근으로 변환, 버퍼 캐시 활용, 프로세스 간 공유 메모리로 사용 가능
420. 메모리 맵 I/O (Memory-Mapped I/O) - 디바이스 레지스터 매핑
421. 커널 메모리 할당의 특징 - 물리적으로 연속되어야 함 (주로 버디 시스템 + 슬랩 할당기)
422. 페이지 고정 (Page Pinning / Locking) - I/O 대기 중인 페이지가 스왑아웃되지 않게 고정 (mlock)
423. 대형 페이지 (Large Page / Transparent Hugepage)의 가상 메모리 성능 이점
424. ZRAM / 커널 스왑 압축 기술 - 스왑 디스크 I/O 대신 메모리 내 데이터 압축 보관
425. OOM Killer (Out-of-Memory) 작동 우선순위 점수 (oom_score) 매커니즘
426. NUMA 환경의 가상 메모리 스케줄링 (NUMA 노드 별 페이지 할당 / numactl)
427. 캐시 친화적 가상 메모리 관리 배치
428. VMA (Virtual Memory Area) 구조체 (리눅스 커널 프로세스 주소 공간 매핑)
429. 마이너 페이지 폴트 (Minor Page Fault) vs 메이저 페이지 폴트 (Major Page Fault / 디스크 I/O 동반)
430. 수요 페이지 제로화 (Demand Zero Paging) - BSS 영역 보안 할당
431. 더티 페이지 쓰기 (Dirty Page Writeback) 메커니즘 (pdflush / flusher 스레드)
432. 캐시 컬러링 (Cache Coloring)에 의한 페이지 매핑 최적화
433. 역 페이지 테이블 탐색 최적화 해시 함수
434. 비동기식 페이지 폴트 (Asynchronous Page Faults) 핸들링
435. TLB 슛다운 (TLB Shootdown) - 멀티코어 환경에서 타 코어의 TLB 무효화 오버헤드
436. 커널 페이지 테이블 격리 (KPTI, Kernel Page-Table Isolation) - Meltdown 취약점 대응망
437. 메모리 암호화 가상화 (AMD SME/SEV, Intel SGX)
438. 파일시스템 버퍼 캐시(Buffer Cache)와 가상 메모리 페이지 캐시(Page Cache)의 통합 원리
439. Cgroups 메모리 서브시스템의 자원 제한 (Memory Limit) 동작
440. eBPF 기반 메모리 할당 트레이싱

## 8. 저장장치 및 입출력 (I/O) 시스템 (60개)
441. I/O 장치의 분류 - 블록 장치 (Block Device) vs 문자 장치 (Character Device)
442. 블록 장치 - 하드 디스크, SSD (블록 단위 읽기/쓰기, 랜덤 액세스 가능)
443. 문자 장치 - 키보드, 마우스, 직렬 포트 (스트림 단위, 순차 접근)
444. 네트워크 장치 (소켓 인터페이스)
445. I/O 하드웨어 인터페이스 요소 - 데이터 레지스터, 상태 레지스터, 제어 레지스터
446. 포트 (Port) / 버스 (Bus) - PCIe, USB, SATA, NVMe
447. 메모리 맵 I/O (Memory-mapped I/O) vs 분리된 I/O (Isolated I/O / Port I/O)
448. 폴링 (Polling / Programmed I/O) - 상태 비트를 지속적으로 호스트가 읽음 (바쁜 대기)
449. 인터럽트 구동 I/O (Interrupt-driven I/O) - 완료 시 장치가 CPU에 인터럽트 발생
450. 직접 메모리 접근 (DMA, Direct Memory Access) - CPU 개입 없이 장치와 메모리 간 직접 데이터 전송
451. 사이클 스틸링 (Cycle Stealing) - DMA 컨트롤러가 CPU의 버스 사용을 일시 중지시키고 전송
452. DMA 산란-수집 (Scatter-Gather) - 불연속적 물리 메모리 블록을 한 번의 DMA로 전송
453. I/O 서브시스템의 커널 서비스 - I/O 스케줄링, 버퍼링, 캐싱, 스풀링, 오류 처리
454. 버퍼링 (Buffering) - 송수신자 간 데이터 전송 속도 차이, 전송 단위 차이 극복
455. 이중 버퍼링 (Double Buffering)
456. 캐싱 (Caching) - 자주 사용하는 데이터 복사본 유지 (속도 빠른 메모리 활용)
457. 스풀링 (Spooling, Simultaneous Peripheral Operation On-Line) - 디스크를 대형 버퍼로 사용 (프린터 큐)
458. 예약 및 단독 장치 접근 제어
459. 블로킹 I/O (Blocking I/O) - I/O 완료 시까지 프로세스 대기
460. 논블로킹 I/O (Non-blocking I/O) - 데이터가 없어도 즉시 반환 (오류/0 바이트 반환)
461. 비동기 I/O (Asynchronous I/O, AIO) - I/O 요청 후 즉시 작업 진행, 완료 시 시그널/콜백 알림
462. I/O 완료 포트 (IOCP, I/O Completion Port) - Windows 비동기 I/O 스케일링
463. epoll / kqueue - 리눅스/BSD 다중 I/O 이벤트 통지 (고성능 소켓 서버)
464. io_uring - 최신 리눅스 커널 비동기 I/O 프레임워크 (링 버퍼 기반, 제로 시스템콜 목표)
465. 하드 디스크 드라이브 (HDD) 구조 - 플래터, 트랙, 실린더, 섹터, 헤드
466. 논리적 블록 주소 (LBA, Logical Block Address) - 1차원 배열로 매핑
467. 디스크 접근 시간 = 탐색 시간(Seek Time) + 회전 지연(Rotational Latency) + 전송 시간(Transfer Time)
468. 디스크 스케줄링 (Disk Scheduling) 목적 - 탐색 시간 최소화, 처리량 극대화
469. FCFS (First-Come, First-Served) 스케줄링
470. SSTF (Shortest Seek Time First) - 현재 헤드 위치에서 가장 가까운 요청 처리 (기아 발생 가능)
471. SCAN 스케줄링 (엘리베이터 알고리즘) - 한 방향으로 이동하며 끝까지 처리 후 역방향
472. C-SCAN (Circular SCAN) - 한 방향으로만 처리하고 끝에 도달하면 시작점으로 빠르게 복귀 (대기 시간 균등화)
473. LOOK 및 C-LOOK - 양 끝까지 가지 않고 마지막 요청까지만 이동 후 턴 (SCAN/C-SCAN 최적화)
474. 리눅스 I/O 스케줄러 - NOOP, CFQ(Completely Fair Queuing), Deadline, BFQ
475. 솔리드 스테이트 드라이브 (SSD, Solid State Drive) 구조 - NAND 플래시, 페이지(Page), 블록(Block)
476. 플래시 메모리 한계 - 덮어쓰기 불가(Erase-before-write), 쓰기 횟수 제한(Wear-out)
477. 가비지 컬렉션 (Garbage Collection in SSD) - 유효 페이지 복사 후 블록 전체 지우기
478. FTL (Flash Translation Layer) - LBA를 플래시의 물리 주소(PBA)로 매핑하는 펌웨어
479. 마모 평준화 (Wear Leveling) - 수명 연장을 위해 쓰기 작업을 전체 블록에 고르게 분산
480. 쓰기 증폭 (Write Amplification) 현상
481. TRIM 명령어 - OS가 삭제된 파일의 LBA를 SSD에 알려주어 GC 효율 향상
482. NVMe (Non-Volatile Memory Express) - PCIe 버스 기반 고속 플래시 프로토콜 (다중/깊은 큐 지원)
483. RAID (Redundant Array of Independent Disks) - 성능 향상 및 신뢰성(중복성) 확보
484. RAID 0 (스트라이핑, Striping) - 블록 분산 저장, 성능 최고, 신뢰성 없음
485. RAID 1 (미러링, Mirroring) - 데이터 중복 복사, 신뢰성 최고, 용량 효율 50%
486. RAID 4 (블록 단위 스트라이핑 + 단일 패리티 디스크) - 병목 발생
487. RAID 5 (블록 단위 스트라이핑 + 분산 패리티) - 성능/신뢰성 절충, 가장 대중적, 디스크 1개 고장 허용
488. RAID 6 (분산 이중 패리티) - 디스크 2개 고장 허용
489. RAID 10 (1+0) / RAID 01 (0+1) 혼합형 구조
490. 소프트웨어 RAID vs 하드웨어 RAID (컨트롤러 캐시/BBU 장착)
491. 핫 스페어 (Hot Spare) 디스크 자동 재구성
492. NAS (Network Attached Storage) - 파일 단위 접근 (NFS, SMB/CIFS)
493. SAN (Storage Area Network) - 블록 단위 전용 네트워크 접근 (Fibre Channel, iSCSI)
494. 오브젝트 스토리지 (Object Storage) - 플랫 네임스페이스, REST API 기반 클라우드 (Amazon S3)
495. 장치 드라이버 (Device Driver) 커널 인터페이스 구현
496. 인터럽트 공유 (Interrupt Sharing) 및 MSI/MSI-X (Message Signaled Interrupts)
497. SR-IOV (Single Root I/O Virtualization) - 가상 머신에 물리적 PCIe 장치 직접 매핑
498. 컴퓨테이셔널 스토리지 (Computational Storage / Smart SSD) - I/O 노드 연산 오프로딩
499. NVMe over Fabrics (NVMe-oF) - RDMA 기반 네트워크 SSD 고속 연결 프로토콜
500. 이중 경로 (Multipath) I/O 페일오버 및 로드밸런싱 구조

## 9. 파일 시스템 (File System) 관리 (70개)
501. 파일 (File)의 정의 - 논리적 레코드의 연속, OS가 관리하는 정보의 기본 단위
502. 파일 속성 (Attributes) - 이름, 식별자, 타입, 위치, 크기, 보호(권한), 타임스탬프
503. 매직 넘버 (Magic Number) - 파일 확장자 외 내용 식별자
504. 파일 접근 방법 - 순차 접근 (Sequential Access), 직접 접근 (Direct Access / Random Access)
505. 색인 접근 (Indexed Access)
506. 디렉터리 (Directory) 구조 - 심볼 테이블 (이름 -> 항목 번역)
507. 1단계 디렉터리 / 2단계 디렉터리 (사용자별 UFD)
508. 트리 구조 디렉터리 (Tree-structured Directory) - 계층 구조, 현재 디렉터리 개념
509. 절대 경로 (Absolute Path) / 상대 경로 (Relative Path)
510. 비순환 그래프 디렉터리 (Acyclic Graph Directory) - 링크를 통한 디렉터리/파일 공유
511. 하드 링크 (Hard Link) - 동일한 물리 데이터(i-node) 가리킴, 디렉터리 링크 불가
512. 심볼릭 링크 (Symbolic Link / Soft Link) - 경로명을 값으로 가짐, 윈도우의 바로가기
513. 일반 그래프 디렉터리 (순환 허용) - 무한 루프 탐색 방지 알고리즘 (가비지 컬렉션 필요)
514. 파티션 (Partition) / 슬라이스 / 볼륨 (Volume)
515. MBR (Master Boot Record) vs GPT (GUID Partition Table)
516. 마운트 (Mount) 메커니즘 - 다른 파일 시스템을 디렉터리 트리의 특정 지점에 연결
517. VFS (Virtual File System) - 다양한 파일 시스템(ext4, NTFS, FAT)을 추상화하는 공통 인터페이스 객체 모델
518. VFS 객체 - 슈퍼블록 (Superblock), 아이노드 (inode), 덴트리 (dentry), 파일 객체 (file object)
519. 디스크 상의 구조 - 부트 제어 블록, 볼륨 제어 블록(슈퍼블록), 디렉터리 구조, FCB(아이노드)
520. 메모리 내의 구조 - 마운트 테이블, 시스템 전체 열린 파일 테이블 (System-wide Open File Table), 프로세스별 열린 파일 테이블
521. 열린 파일 테이블 (Open File Table) - 파일 포인터, 열림 횟수(Open Count), 접근 권한 기록
522. 파일 할당 방법 (File Allocation Methods)
523. 연속 할당 (Contiguous Allocation) - 시작 블록과 길이 저장, 속도 빠름, 외부 단편화 심각
524. 연결 할당 (Linked Allocation) - 블록들이 포인터로 연결됨, 외부 단편화 없음, 랜덤 접근 불가, 포인터 오버헤드
525. FAT (File Allocation Table) - MS-DOS 기반, 포인터들을 별도의 테이블에 모아 캐싱하여 랜덤 접근 문제 완화
526. 색인 할당 (Indexed Allocation) - 모든 블록 포인터를 색인 블록(Index Block) 하나에 모아 저장
527. 색인 블록 크기 한계 해결 - 연결 색인, 다중 수준 색인 (Multilevel Index)
528. 유닉스 i-node (Index Node) 매커니즘 - 파일 메타데이터 및 다중 접근 포인터 보유
529. i-node 직접 블록 (Direct Blocks) - 보통 12~15개, 작은 파일 고속 접근
530. i-node 단일/이중/삼중 간접 블록 (Indirect Blocks) - 대용량 파일 확장 지원 체계
531. 익스텐트 (Extent) - 연속된 여러 블록의 묶음 할당 기법 (ext4, XFS 적용 - 메타데이터 감소 효과)
532. 빈 공간 관리 (Free-Space Management) 알고리즘
533. 비트 벡터 (Bit Vector / Bitmap) - 0과 1로 표현, 1워드 크기 연속 빈 공간 탐색 최적
534. 연결 리스트 (Linked List) 빈 공간 관리
535. 그룹화 (Grouping) / 계수 (Counting) 기법
536. 버퍼 캐시 (Buffer Cache) / 페이지 캐시 (Page Cache) 통합 아키텍처
537. 미리 읽기 (Read-ahead) 및 지연 쓰기 (Delayed-write / Write-behind)
538. 동기화 I/O (O_SYNC / fsync)
539. 저널링 파일 시스템 (Journaling File System) - 시스템 크래시 시 일관성 복구 (ext3, ext4, NTFS)
540. 메타데이터 저널링 vs 데이터 저널링 모드 (순서: 로그 기록 -> 커밋 -> 실제 파일시스템 반영)
541. LFS (Log-structured File System) - 모든 쓰기를 순차적 로그 형태로만 디스크에 기록 (플래시 메모리에 적합)
542. COW (Copy-On-Write) 파일 시스템 (ZFS, Btrfs) - 스냅샷 및 롤백 기능 내장
543. NFS (Network File System) - 원격 디렉터리 마운트 프로토콜 (상태 비저장, UDP/TCP 지원)
544. AFS (Andrew File System) / SMB/CIFS (Windows 파일 공유)
545. 윈도우 NTFS - MFT (Master File Table), 권한 제어(ACL), 파일 압축 및 암호화 지원
546. 데이터 중복 제거 (Data Deduplication) 파일 시스템 기능
547. 파일 시스템 접근 제어 (Access Control) - 소유자, 그룹, 기타(Other)의 rwx 권한 (r=4, w=2, x=1)
548. SetUID (4000), SetGID (2000), Sticky Bit (1000) 특수 권한
549. ACL (Access Control List) 확장을 통한 세밀한 사용자별 파일 권한 통제
550. 리눅스 확장 속성 (Extended Attributes, xattr)
551. 할당량 (Quota) 시스템 - 유저/그룹 별 디스크 사용량 제한
552. B-Tree / B+Tree 기반 디렉터리 색인 (대규모 디렉터리 검색 최적화)
553. 분산 파일 시스템 (HDFS, Ceph, GlusterFS) 네임노드 및 데이터노드 구조
554. FUSE (Filesystem in Userspace) - 커널 수정 없이 유저 공간에서 커스텀 파일시스템 구현 (SSHFS 등)
555. 백업 (Backup) 및 복구 (Restore) / 전체 백업 vs 증분(Incremental) 백업
556. 삭제된 파일 복구 (Undelete) 및 포렌식 디스크 이미지 카빙(Carving) 원리
557. 임시 파일 시스템 (tmpfs / ramfs) - 메모리 상주 파일 시스템
558. 가상 장치 파일 시스템 (sysfs, procfs) - 커널 변수와 하드웨어 정보 노출 통로
559. 파일 시스템 일관성 검사 (fsck / chkdsk)
560. 다중 스트림 (Multi-stream) 파일 / 포크 (Forks) - 데이터 스트림과 리소스 스트림 분리
561. 암호화 파일 시스템 (eCryptfs / Windows EFS)
562. 무결성 검증 파일 시스템 (dm-verity / Android 적용 보안 파일 구조)
563. 플래시 전용 파일 시스템 (F2FS, JFFS2, YAFFS) 특성 분석
564. 데이터 파손 (Data Corruption / Bit Rot) 대응 Btrfs 자가 치유(Self-healing) 기능
565. Direct I/O (O_DIRECT) - OS 캐시를 우회하여 데이터베이스 등의 자체 캐싱 최적화
566. mmap 기반 제로 카피 (Zero-copy) 전송 기술 (sendfile) 성능 이점
567. 파일 잠금 (File Locking) - 공유 잠금(Shared lock) vs 배타적 잠금(Exclusive lock)
568. 강제적 잠금 (Mandatory Lock) vs 권고적 잠금 (Advisory Lock)
569. 스파스 파일 (Sparse File) 저장 공간 절약 기술
570. 리눅스 inotify 시스템 - 파일/디렉터리 변경 이벤트 모니터링 API

## 10. 시스템 보안, 보호, 그리고 성능/가상화 심화 (100개)
571. 보호 (Protection) vs 보안 (Security)의 개념 차이
572. 보호 도메인 (Protection Domain) - 프로세스가 접근할 수 있는 자원(객체)과 권한(Access Right)의 집합
573. 접근 제어 행렬 (Access Matrix) - 주체(행)와 객체(열) 교차점의 권한 표현 모형
574. 전역 테이블 (Global Table) 방식 구현 (행렬 희소성 문제)
575. 접근 제어 목록 (ACL, Access Control List) - 객체 중심 (해당 객체에 접근 가능한 주체 목록)
576. 자격 증명 리스트 (Capability List / Ticket) - 주체 중심 (주체가 가진 권한 리스트 토큰 방식)
577. 롤 기반 접근 제어 (RBAC, Role-Based Access Control) - 사용자 대신 역할(Role)에 권한 할당
578. 임의적 접근 제어 (DAC, Discretionary Access Control) - 소유자가 임의로 권한 위임
579. 강제적 접근 제어 (MAC, Mandatory Access Control) - 시스템/보안 관리자가 등급 라벨 기반 강제 통제
580. 벨-라파둘라 모델 (Bell-LaPadula) - 기밀성 위주 보안 정책 (No Read Up, No Write Down)
581. 비바 모델 (Biba Model) - 무결성 위주 정책 (No Read Down, No Write Up)
582. 리눅스 보안 모듈 (LSM, Linux Security Modules) - 플러그인 훅 구조
583. SELinux - 레이블 기반 MAC 구현체, 보안 컨텍스트
584. AppArmor - 경로 기반 MAC 구현 모듈
585. 시스템 보안 위협 유형 - 기밀성, 무결성, 가용성, 인증 침해
586. 트로이 목마 (Trojan Horse) / 래퍼 (Wrapper)
587. 트랩 도어 (Trap Door / Backdoor)
588. 로직 밤 (Logic Bomb) / 타이머 밤
589. 바이러스 (Virus) - 호스트 프로그램 기생
590. 웜 (Worm) - 자가 복제 네트워크 전파 독자 실행
591. 버퍼 오버플로우 (Buffer Overflow) 원리 - C언어 취약 함수 악용 리턴 주소 덮어쓰기
592. 셸코드 (Shellcode) 인젝션
593. 버퍼 오버플로우 방어 하드웨어 기술 (NX Bit / Data Execution Prevention, DEP)
594. 가상 주소 공간 구조 무작위화 (ASLR) - 버퍼/스택 라이브러리 주소 랜덤 배치 방어망
595. 카나리 (Canary) / 스택 스매싱 가드 (Stack Smashing Protector) - 컴파일러 수준 버퍼 변조 탐지
596. ROP (Return-Oriented Programming) 기법 - ASLR/DEP 우회를 위해 코드 가젯 체이닝
597. 제로 데이 (Zero-Day) 취약점 / 익스플로잇 (Exploit)
598. 스푸핑 (Spoofing) - IP/MAC 등 신분 위장
599. 서비스 거부 (DoS) 및 분산 서비스 거부 (DDoS) 네트워크 자원 고갈 공격
600. 포트 스캐닝 (Port Scanning) 도구 원리
601. 침입 탐지 시스템 (IDS) / 침입 방지 시스템 (IPS) 시스템 콜 트레이싱 기반 이상 탐지
602. 샌드박싱 (Sandboxing) 기술 커널 래퍼
603. 루트킷 (Rootkit) 커널 모듈 감염 방식 (시스템 콜 테이블 후킹)
604. 사용자 인증 (Authentication) 요소 - Something you know, have, are
605. 비밀번호 솔팅 (Salting) 기반 해시 처리 방어 구조
606. 감사 (Auditing) 로깅 프레임워크 (Linux Auditd)
607. 물리적 보안 및 하드웨어 보안 모듈 (TPM, Trusted Platform Module)
608. 보안 부팅 (Secure Boot) 인증서 체인 로딩 검증
609. 성능 모니터링 (Performance Monitoring) 및 튜닝 방법론
610. 리틀의 법칙 (Little's Law) - L = λW (대기 큐 성능 분석)
611. CPU 유휴 (Idle) 대기 루프 최적화
612. 메모리 누수 (Memory Leak) 탐지 도구 구조 (Valgrind 등)
613. 프로파일링 (Profiling) 도구 Gprof 커널 후킹 작동 원리
614. 시스템 DTrace 선언적 동적 트레이싱 엔진 메커니즘
615. eBPF 네트워크/보안/모니터링 이벤트 커널 안전 훅 매커니즘
616. 멀티코어 확장성 병목 (Amdahl's Law) 및 커널 락 경합 진단
617. I/O 성능 병목 (Bottleneck) 탐색법 (iostat, vmstat)
618. 캐시 미스 오버헤드 측정 분석망 구조 적용
619. 모바일 OS 특징 (Android vs iOS 아키텍처 비교)
620. 안드로이드 리눅스 커널 커스터마이징 (Wakelock 전력 통제 모듈)
621. ART (Android Runtime) AOT/JIT 컴파일러 혼합 실행 환경
622. iOS XNU 하이브리드 커널 및 샌드박스 앱 관리 모형
623. 임베디드 실시간 OS (RTOS: VxWorks, FreeRTOS 등) 우선순위 데드라인 절대 보장 아키텍처
624. 마이크로커널 IPC 메시지 패싱 지연 단축 기법 구조 설계
625. 하이퍼바이저 링 레벨 (Ring -1 모드 VMX Root/Non-Root 모드)
626. 쉐도우 페이지 테이블 (Shadow Page Table) vs 확장 페이지 테이블 (EPT/NPT 하드웨어 보조)
627. IOMMU (Input/Output MMU) 역할 - 가상머신 DMA 장치 할당 및 보호 격리
628. 컨테이너 런타임 (runc, containerd) OCI 규격 표준화
629. 라이브 마이그레이션 (Live Migration) 메모리 더티 페이지 프리-카피(Pre-copy) 알고리즘 방식
630. 가상 스위치 (vSwitch) 패킷 오버헤드 VNF 구조 적용 방식
631. 메모리 KSM (Kernel Samepage Merging) 가상머신 간 중복 메모리 통합 절약
632. 벌루닝 (Ballooning) 하이퍼바이저 가상머신 동적 메모리 회수 기법 구조
633. 무정전 업데이트 (Ksplice 등 커널 재부팅 없는 패치망 체계 구조)
634. 병행 프로그래밍 락 프리 스택/큐 설계 데이터 구조 메커니즘
635. 동시성 디버깅 경쟁 조건 재현 기법 퍼저/스레드 새니타이저 (ThreadSanitizer)
636. 다중 경로 I/O (Multipath I/O) 커널 모듈 아키텍처
637. ZFS 복제 및 스냅샷 (Snapshot) 카피온라이트 구현 구조 설계 모형
638. Btrfs 서브볼륨 및 압축/암호화 통합 커널 파일 시스템 동향
639. RDMA (Remote Direct Memory Access) 커널 바이패스 초고속 통신 체제
640. 유니커널 (Unikernel) 커널 분할 오버헤드 극소화 구조체 망 보안 융합 (MirageOS)
641. 분산 OS 투명성 (Transparency: 위치, 마이그레이션, 복제, 병행 투명성 보장 구조)
642. 람포트 논리적 시계 (Lamport's Logical Clocks) 분산 환경 동기화 정렬
643. 분산 락 매니저 구현 (Chubby, ZooKeeper 등 분산 코디네이션 락 알고리즘)
644. 마이크로서비스 커널 자원 제약 (Pod / Container 자원 오버커밋 킬링 정책)
645. 커널 동적 모듈 서명 (Module Signature Verification) 무결성 통제
646. 리눅스 시스템 콜 테이블 (sys_call_table) 확장 및 보안 훅 추가
647. NUMA 인지형 메모리 할당기 커널 페이지 이동 정책 프레임워크 설계
648. 프로세스 체크포인트/리스토어 (CRIU) 컨테이너 마이그레이션 도구 구조
649. 커널 메모리 컴팩션 (Compaction) 외부 단편화 런타임 제거 백그라운드 스레드 구조
650. 고가용성 클러스터 운영체제 하트비트/펜싱 (Fencing / STONITH) 뇌 분할(Split-Brain) 방어 메커니즘
651. 전력 인식(Power-aware) 스케줄러 동적 전압/주파수 스케일링(DVFS) 통합형 CPU 제어
652. 모바일 OS Out-Of-Memory (Low Memory Killer) 스코어 계산 알고리즘 및 앱 수명 주기 관리
653. 엣지 컴퓨팅 OS (초경량/고속 부팅 최적화된 리눅스 환경 구성 기술망)
654. 리얼타임 리눅스 (PREEMPT_RT) 커널 스핀락을 뮤텍스로 변환하는 선점 허용 구조 개요
655. CPU 캐시 일관성 정책 (MESI 프로토콜) 이 커널 락(Lock)에 미치는 캐시라인 핑퐁(Ping-pong) 문제
656. 하드웨어 트랜잭셔널 메모리 활용 Lock-Free 자료구조 시스템 구현 사례
657. 가상화 I/O 패스스루 (Passthrough) VFIO 프레임워크
658. Virtio - 반가상화 I/O 백엔드/프론트엔드 링버퍼(Vring) 디바이스 드라이버 구조
659. 클라우드 게스트 OS (Cloud-init 기반 부트스트랩 인스턴스 자동 초기화 스크립트)
660. 커널 덤프 (Kdump) 시스템 크래시 원인 분석 커널 구조
661. eBPF 기반 XDP (eXpress Data Path) 커널 네트워크 스택 우회 초고속 패킷 드롭/전달 프레임워크
662. 안드로이드 바인더(Binder) IPC 스레드 풀 및 객체 참조 매핑 메커니즘
663. macOS/iOS Grand Central Dispatch (GCD) 블록 및 디스패치 큐 기반 동시성 구조
664. Windows 커널 비동기 프로시저 호출 (APC) 및 지연된 프로시저 호출 (DPC)
665. 시스템 레지스트리 (Windows Registry) 및 구성 데이터베이스 관리 구조
666. 보안 엔클레이브 (TrustZone, SGX)와 OS TEE (Trusted Execution Environment) 연동 구조
667. 제로 트러스트(Zero Trust) 철학 하의 운영체제 레벨 런타임 무결성 검증망 설계
668. 부채널 공격 (Side-channel Attack, Meltdown/Spectre) 마이크로아키텍처 취약점 대응 소프트웨어 패치(KPTI, Retpoline)
669. 하드웨어 기반 무작위 난수 생성기 (TRNG) 커널 엔트로피 풀 주입 방식
670. 소프트웨어 오류 주입 (Fault Injection) 카오스 테스팅 시스템 커널 모듈 활용법

## 11. 시험 빈출 / 핵심 요약 노트 및 추가 토픽 (130개)
671. 시스템 프로그램과 응용 프로그램의 차이
672. 일괄 처리 시스템 (Batch Processing System) 성능 지표
673. 다중 프로그래밍 (Multiprogramming) 한계 자원
674. 시분할 시스템 응답 시간 최적화
675. 멀티태스킹 (Multitasking) 용어
676. 인터럽트 벡터 테이블 구조화
677. 트랩 (Trap) 기반 시스템 콜 구현
678. 커널 모드 진입 메커니즘 
679. 시스템 콜 API 래퍼
680. 모놀리식 vs 마이크로 커널 성능 비교
681. IPC 기법 성능 오버헤드 
682. 프로세스 주소 공간 분리 
683. PCB 구성 요소 필수 암기
684. 문맥 교환 TLB 플러시 
685. 단기 스케줄러 디스패치 
686. CPU 바운드 vs I/O 바운드
687. 선점 / 비선점 스케줄링 차이
688. FCFS 호위 효과 (Convoy Effect)
689. SJF 기아 (Starvation) 발생
690. 라운드 로빈 시간 할당량 (Quantum)
691. 다단계 피드백 큐 (MLFQ) 천이
692. HRN 대기 시간 공식
693. 멀티스레드 유저모드 커널모드 
694. 스레드 로컬 스토리지 (TLS) 
695. 스레드 동기화 상호 배제
696. 경쟁 조건 (Race Condition) 
697. 임계 구역 3가지 요구조건 
698. Test-and-Set 연산 하드웨어 
699. 뮤텍스 락 (Mutex Lock) 
700. 스핀락 바쁜 대기 (Busy Wait) 
701. 세마포어 P, V 연산 
702. 모니터 (Monitor) 동기화 추상화 
703. 생산자 소비자 유한 버퍼
704. 식사하는 철학자 교착 문제 
705. 교착 상태 4가지 조건 
706. 자원 할당 그래프 사이클 
707. 은행원 알고리즘 안전 상태 
708. 교착 상태 무시 (타조 알고리즘) 
709. 교착 상태 복구 (프로세스 킬) 
710. 주소 바인딩 컴파일/로드/실행 
711. 논리 주소 물리 주소 변환 MMU
712. 외부 단편화 가변 분할 
713. 내부 단편화 고정/페이징 
714. 동적 할당 First/Best/Worst Fit 
715. 페이징 시스템 프레임 테이블 
716. TLB 적중률 캐시 속도 
717. 다단계 페이지 테이블 사이즈 줄이기 
718. 세그멘테이션 외부 단편화 재발 
719. 요구 페이징 (Demand Paging) 
720. 페이지 폴트 (Page Fault) ISR 
721. 유효/무효 비트 (Valid/Invalid) 
722. 페이지 교체 LRU 원리 
723. FIFO 벨라디의 모순 
724. 최적 알고리즘 (OPT) 구현 불가 
725. 스래싱 (Thrashing) CPU 이용률 저하 
726. 워킹 셋 (Working Set) 메모리 
727. 디스크 스케줄링 SCAN 엘리베이터 
728. C-SCAN 단방향 회전
729. SSTF 기아 현상 (가운데 편중) 
730. RAID 0, 1, 5, 6 성능 신뢰성 
731. SSD FTL (Flash Translation Layer) 
732. 가비지 컬렉션 블록 지우기 
733. 파일 시스템 연속, 연결, 색인 할당 
734. FAT 방식 연결 할당 최적화 
735. i-node 직접/간접 포인터 인덱스 
736. 하드 링크 / 심볼릭 링크 차이 
737. VFS 가상 파일 시스템 
738. 버퍼 캐시 파일 입출력 지연 
739. 접근 제어 목록 (ACL) 
740. 보호 도메인 최소 권한 원칙 
741. 버퍼 오버플로우 공격 스택 
742. 스푸핑, 백도어 악성코드 
743. 가상화 하이퍼바이저 
744. 컨테이너 네임스페이스 격리 
745. 시스템 클럭 타이머 틱 
746. I/O 직접 메모리 접근 (DMA)
747. I/O 풀링 (Polling) 오버헤드 
748. 스풀링 (Spooling) 버퍼
749. 메모리 매핑 파일 (mmap)
750. 쓰기 시 복사 (COW) 
751. SMP 캐시 일관성 폴스 셰어링 
752. 인터럽트 구동 입출력 
753. 우선순위 역전 (Priority Inversion) 방지 
754. 문맥 교환 비용 (레지스터 저장 복원) 
755. 고아 좀비 프로세스 init 처리 
756. 시스템 콜 오버헤드 이유
757. 파일 지연 쓰기 (Delayed Write)
758. 저널링 파일 시스템 트랜잭션 로그
759. 블로킹 / 논블로킹 / 비동기 I/O
760. 슬랩 (Slab) 할당기 객체 캐싱 
761. 디바이스 드라이버 모듈 인터페이스 
762. 인터럽트 처리 상프/하프 메커니즘
763. 루트킷 탐지 무결성 스캔
764. ASLR 메모리 레이아웃 난수화 
765. SELinux 보안 강제 접근 통제 
766. 실시간 스케줄링 마감 시간 (Deadline) 
767. 스핀락 멀티 프로세서 전용 활용 
768. CAS (Compare And Swap) 명령어 기초 
769. 데드락 희생자 롤백 복구망
770. 역 페이지 테이블 전역 해시 매핑 
771. 플래시 메모리 마모 평준화 (Wear Leveling)
772. 다중 큐 SSD NVMe 프로토콜 장점
773. 오브젝트 스토리지 메타데이터 분리
774. 네트워크 파일 시스템 (NFS) 무상태 (Stateless)
775. 파티션 MBR GPT 크기 제한
776. 클라우드 컴퓨팅 OS 자원 풀링 
777. OOM 킬러 메모리 보호 정책 
778. 프로세스 친화성 (Affinity) 스케줄링 
779. 부하 균등화 (Load Balancing) 큐 이주
780. eBPF 동적 커널 트레이싱 프레임워크 성능 
781. ZFS Copy-on-Write 볼륨 관리 통합 
782. LFS (Log-structured File System) 랜덤 쓰기 순차화
783. 모바일 환경 에너지 인지 스케줄러 
784. 하이퍼스레딩 물리 코어 논리 코어 분할 구조 
785. 클론(clone) 시스템 콜 스레드 공유 플래그
786. cgroups 메모리, CPU 자원 제한 격리 컨테이너
787. 안드로이드 LMK (Low Memory Killer) 작동 
788. iOS 앱 샌드박싱 구조 
789. 라이브 패칭 (Kpatch) 커널 정지 없는 보안
790. POSIX 스레드 (pthreads) 표준 API 
791. 락 엘리전 하드웨어 트랜잭션 메모리 활용 
792. RCU 다중 독자 락 프리 고성능 기법 
793. 워킹 셋 윈도우 사이즈 동적 조절 
794. 페이지 컬러링 캐시 경합 회피 물리 할당
795. 틱리스 커널(Tickless) 모바일 배터리 보존
796. NUMA 로컬 메모리 원격 메모리 지연차 
797. 유니커널 보안과 가벼운 부팅 특성 망 적용
798. 분산 락 주키퍼(ZooKeeper) 합의 동기화 
799. 람포트 타임스탬프 인과 관계 정렬
800. 시스템 아키텍처 결함 허용 (Fault Tolerance) 듀얼 구성

---
**총합 요약 : 총 800개 핵심 키워드 수록**
(기본 OS 프로세스/메모리/파일시스템 뿐만 아니라 최신 리눅스 커널, 가상화/컨테이너 인프라 기술, 락프리 알고리즘, SSD/NVMe 스토리지 구조까지 기술사 시험에 완벽 대비할 수 있도록 800여 개의 심화 토픽을 총망라했습니다.)
