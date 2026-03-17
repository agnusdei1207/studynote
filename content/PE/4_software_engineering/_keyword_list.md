+++
title = "04. 소프트웨어공학 키워드 목록"
date = "2026-03-04"
[extra]
categories = "studynotes-se"
+++

# 소프트웨어공학 (Software Engineering) 키워드 목록 (심화 확장판)

정보통신기술사·컴퓨터응용시스템기술사 및 전문 SW 엔지니어를 위한 소프트웨어공학 전 영역 핵심 및 심화 키워드 800선입니다.

전통적인 소프트웨어 개발 방법론부터 최신 애자일, DevOps, 클라우드 네이티브 아키텍처, AI 기반 개발(LLM), 시큐어 코딩 및 SW 공급망 보안까지 폭넓게 다룹니다.

---

## 1. 소프트웨어 공학 기초 및 프로세스 모델 (60개)
1. 소프트웨어 공학 (Software Engineering)의 정의 및 목표 (신뢰성, 효율성, 유지보수성)
2. 소프트웨어 위기 (Software Crisis) - 비용 초과, 일정 지연, 품질 저하
3. 소프트웨어 생명주기 (SDLC, Software Development Life Cycle)
4. 폭포수 모델 (Waterfall Model) - 순차적, 문서 중심
5. V-모델 (V-Model) - 검증(Verification)과 확인(Validation)의 대응
6. 프로토타입 모델 (Prototype Model) - 요구사항 명확화, 시제품
7. 나선형 모델 (Spiral Model) - 위험 분석(Risk Analysis) 강조, 점진적 확장
8. 반복적/점진적 모델 (Iterative and Incremental Model)
9. RAD (Rapid Application Development) 모델 - JAD, CASE 도구 활용
10. 진화적 프로세스 모델 (Evolutionary Process Model)
11. 클린룸 소프트웨어 공학 (Cleanroom Software Engineering) - 통계적 품질 제어
12. 애자일 방법론 (Agile Methodology) 개요
13. ISO/IEC 12207 (소프트웨어 생명주기 공정 표준) - 기본, 지원, 조직 공정
14. ISO/IEC 15504 (SPICE) - 소프트웨어 프로세스 평가 표준
15. CMMI (Capability Maturity Model Integration) - 단계형/연속형 모델
16. CMMI 5단계 - 초기, 관리, 정의, 정량적 관리, 최적화
17. 프로세스 자산 (Process Assets) 및 조직 표준 프로세스
18. PSP (Personal Software Process) / TSP (Team Software Process)
19. 소프트웨어 제품 라인 (SPL, Software Product Line) - 도메인/어플리케이션 공학
20. 형상 관리 (SCM, Software Configuration Management)
21. 형상 식별 (Configuration Identification) - 형상 항목(CI) 선정
22. 형상 통제 (Configuration Control) - 변경 제어 위원회(CCB)
23. 형상 감사 (Configuration Audit) - 무결성 확인
24. 형상 기록/보고 (Configuration Status Accounting)
25. 기준선 (Baseline) - 기능적, 설계, 시험, 제품 기준선
26. 버전 관리 시스템 (VCS) - Centralized (SVN) vs Distributed (Git)
27. 변경 관리 (Change Management) 프로세스
28. 소프트웨어 재공학 (Re-engineering) - 분석, 재구성, 역공학, 이관
29. 역공학 (Reverse Engineering) - 소스코드에서 설계서 추출
30. 재사용 (Reuse) - 자산의 공유, 컴포넌트 기반 개발(CBD)
31. 유지보수 (Maintenance)의 4가지 유형 - 수정, 적응, 완전(개선), 예방
32. 소프트웨어 노후화 (Software Obsolescence)
33. 기술 부채 (Technical Debt) - 단기적 편의성으로 인한 장기적 비용 증가
34. 레거시 시스템 (Legacy System) 현대화 전략
35. 프로젝트 관리 (PM) 10대 지식 영역 (PMBOK)
36. WBS (Work Breakdown Structure) - 작업 분할 구조도
37. CPM (Critical Path Method) - 주공정법, 최장 경로
38. PERT (Program Evaluation and Review Technique) - 낙관, 비관, 기대치 분석
39. 간트 차트 (Gantt Chart) - 일정 시각화
40. EVM (Earned Value Management) - 성과 측정 관리 (PV, EV, AC, SV, CV, SPI, CPI)
41. 위험 관리 (Risk Management) 4단계 - 식별, 분석, 대응, 모니터링
42. 위험 대응 전략 - 회피, 전가, 완화, 수용
43. 품질 보증 (QA) vs 품질 제어 (QC)
44. 소프트웨어 비용 산정 기법 개요
45. 하향식 산정 - 전문가 감정, 델타이 기법
46. 상향식 산정 - LOC (Line of Code), 단계별 인월 산정
47. COCOMO (Constructive Cost Model) - 유기적, 준분리형, 내장형
48. COCOMO II - 응용 구성, 초기 설계, 포스트 아키텍처 모델
49. 기능점수 (FP, Function Point) 산정 - 데이터 기능(ILF, EIF), 트랜잭션 기능(EI, EO, EQ)
50. 간이법 vs 상세법 기능점수 산정
51. 델파이 기법 (Delphi Method) - 전문가 합의 기반 예측
52. 와이드밴드 델파이 (Wideband Delphi) - 팀 단위 반복적 리뷰
53. 백파이어링 (Backfiring) 기법 - LOC와 FP 간 변환
54. 브룩스의 법칙 (Brooks's Law) - 지체된 프로젝트에 인력 투입 시 더 지체됨
55. 잭맨 프레임워크 (Zachman Framework) - 전사적 아키텍처(EA) 프레임워크
56. 토가프 (TOGAF) - The Open Group Architecture Framework
57. 모델 주도 아키텍처 (MDA, Model Driven Architecture) - PIM, PSM 매핑
58. 방법론 테일러링 (Tailoring) - 표준 프로세스를 조직/프로젝트에 맞게 최적화
59. PMO (Project Management Office) - 전사 프로젝트 관리 조직
60. 브레인스토밍 4원칙 (비판금지, 자유분방, 다다익선, 결합개선)

## 2. 애자일 개발 및 최신 방법론 (70개)
61. 애자일 선언문 (Agile Manifesto) - 4가지 가치, 12가지 원칙
62. 스크럼 (Scrum) 프레임워크 - 역할, 이벤트, 산출물
63. 제품 책임자 (Product Owner) - 비즈니스 가치 극대화, 백로그 관리
64. 스크럼 마스터 (Scrum Master) - 가이드, 장애 제거
65. 개발 팀 (Development Team) - 자기 조직화, 다기능 팀
66. 제품 백로그 (Product Backlog) - 요구사항 우선순위 목록
67. 스프린트 (Sprint) - 1~4주의 개발 주기
68. 스프린트 계획 회의 (Sprint Planning)
69. 데일리 스탠드업 (Daily Scrum) - 진행 상황 공유, 장애 파악
70. 스프린트 리뷰 (Sprint Review) - 데모 및 피드백
71. 스프린트 회고 (Sprint Retrospective) - 프로세스 개선
72. 번다운 차트 (Burndown Chart) / 번업 차트 (Burnup Chart)
73. XP (e/Xtreme Programming) - 5가지 가치, 12가지 실천 방법
74. 짝 프로그래밍 (Pair Programming) - 내비게이터와 드라이버
75. 공동 코드 소유 (Collective Code Ownership)
76. 지속적 통합 (CI, Continuous Integration)
77. 테스트 주도 개발 (TDD, Test Driven Development) - Red-Green-Refactor
78. 리팩토링 (Refactoring) - 외부 동작 변경 없이 내부 구조 개선
79. 메타포 (Metaphor) - 시스템의 전체적 가이드라인
80. 소규모 릴리즈 (Small Releases)
81. 사용자 스토리 (User Story) - Who, What, Why 형식
82. 스토리 포인트 (Story Point) - 상대적 규모 산정
83. 플래닝 포커 (Planning Poker) - 다수 전문가 합의 기반 산정
84. 칸반 (Kanban) - 워크플로우 시각화, WIP(Work In Progress) 제한
85. 리드 타임 (Lead Time) / 사이클 타임 (Cycle Time)
86. 누적 흐름도 (CFD, Cumulative Flow Diagram)
87. 린 (Lean) 소프트웨어 개발 - 7대 원칙 (낭비 제거, 학습 증진 등)
88. 가치 스트림 맵 (Value Stream Mapping)
89. 린 스타트업 (Lean Startup) - 구축-측정-학습 피드백 루프
90. 최소 존립 제품 (MVP, Minimum Viable Product)
91. 피벗 (Pivot) - 전략적 방향 전환
92. 대규모 애자일 (Scaled Agile) 프레임워크
93. SAFe (Scaled Agile Framework) - 기업용 대규모 애자일
94. LeSS (Large-Scale Scrum) - 다수 팀 스크럼 확장
95. Nexus - 스크럼 팀 간 의존성 관리
96. Spotify 모델 - Tribe, Squad, Chapter, Guild
97. DevOps (Development + Operations) - 문화, 자동화, 측정, 공유
98. 인프라로서의 코드 (IaC, Infrastructure as Code)
99. 지속적 배포 (CD, Continuous Deployment / Delivery)
100. SRE (Site Reliability Engineering) - 구글의 운영 방식, 에러 예산
101. 에러 예산 (Error Budget) - 안정성 vs 속도 트레이드 오프
102. SLI (Service Level Indicator) / SLO (Service Level Objective)
103. SLA (Service Level Agreement)
104. 토일 (Toil) - SRE에서 줄여야 할 단순 반복적 운영 작업
105. DevSecOps - 보안의 좌측 이동 (Shift-Left Security)
106. FinOps - 클라우드 비용 최적화 및 관리
107. MLOps - 머신러닝 생명주기 관리
108. LLMOps - 대규모 언어 모델 운영 및 미세 조정 관리
109. 플랫폼 엔지니어링 (Platform Engineering) - 개발자 셀프 서비스 포털 (IDP)
110. 내부 개발자 플랫폼 (IDP, Internal Developer Platform)
111. 가시성 (Observability) - Metrics, Logs, Traces (3대 요소)
112. 분산 추적 (Distributed Tracing) - 마이크로서비스 간 호출 추적
113. 카오스 엔지니어링 (Chaos Engineering) - 시스템 회복력 테스트
114. 피처 플래그 (Feature Flag / Toggle) - 런타임 기능 활성/비활성
115. 카나리 배포 (Canary Deployment) - 점진적 릴리즈
116. 블루/그린 배포 (Blue/Green Deployment) - 무중단 배포 전략
117. 롤링 업데이트 (Rolling Update)
118. 섀도우 배포 (Shadow Deployment) - 실트래픽 미러링 테스트
119. GitOps - Git을 진실의 원천(Source of Truth)으로 하는 운영
120. 선언적 인프라 관리 (Declarative Infrastructure)
121. CI/CD 파이프라인 (Pipeline) 자동화
122. 컨테이너 오케스트레이션 (Kubernetes 등) 연계
123. 서버리스 (Serverless) 개발 모델 및 FaaS
124. 클라우드 네이티브 개발 (Cloud Native Development)
125. 12 팩터 앱 (12-Factor App) 아키텍처 방법론
126. 행동 주도 개발 (BDD, Behavior-Driven Development)
127. 도메인 주도 개발 (DDD)의 애자일적 접근
128. 워터스크럼폴 (Water-Scrum-Fall) 안티패턴
129. 스파이크 (Spike) - 기술적 위험 해소를 위한 짧은 조사/프로토타이핑
130. 인수 기준 (Acceptance Criteria) 명확화 (INVEST 원칙)

## 3. 요구공학 및 비즈니스 분석 (60개)
131. 요구공학 (Requirements Engineering) 정의 및 필요성
132. 요구사항의 유형 - 기능적 요구사항 vs 비기능적 요구사항
133. 비기능 요구사항 (Quality Attributes) - 성능, 보안, 가용성, 신뢰성 등
134. 요구공학 프로세스 - 도출, 분석, 명세, 확인, 관리
135. 요구사항 도출 (Elicitation) 기법 - 인터뷰, 설문, 워크숍, 관찰
136. 브레인스토밍 (Brainstorming) / JAD (Joint Application Design)
137. 페르소나 (Persona) 분석 - 가상 사용자 모델링
138. 사용자 여정 지도 (User Journey Map)
139. 프로토타이핑 (Prototyping) - Low-fidelity vs High-fidelity
140. 섀도잉 (Shadowing) - 사용자 업무 환경 직접 관찰
141. 포커스 그룹 인터뷰 (FGI)
142. 요구사항 분석 (Analysis) - 모순 해결, 범위 확정
143. 구조적 분석 (Structured Analysis) - DFD, Data Dictionary, Mini-Spec
144. 자료 흐름도 (DFD, Data Flow Diagram) - Process, Data Flow, Data Store, Terminator
145. 자료 사전 (DD, Data Dictionary) - =, +, { }, [ ], ( ), * *
146. 객체지향 분석 (OOA, Object-Oriented Analysis)
147. 유스케이스 다이어그램 (Use Case Diagram) - 액터, 유스케이스, 관계(포함, 확장)
148. 요구사항 명세 (Specification) - 정형 명세 vs 비정형 명세
149. 소프트웨어 요구사항 명세서 (SRS, Software Requirements Specification)
150. SRS의 품질 특성 - 정확성, 명확성, 완전성, 일관성, 수정 용이성, 추적 가능성
151. 요구사항 확인 및 검증 (V&V, Verification & Validation)
152. 요구사항 검토 (Review) - 인스펙션, 워크쓰루
153. 인스펙션 (Inspection) - 공식적 검토, 중재자, 체크리스트
154. 워크쓰루 (Walkthrough) - 비공식적, 지식 공유 위주
155. 동료 검토 (Peer Review)
156. 요구사항 추적성 (Traceability) - 수직적/수평적 추적성
157. 요구사항 추적 매트릭스 (RTM, Requirements Traceability Matrix)
158. 요구사항 관리 (Management) - 변경 통제, 버전 관리
159. 베이스라인 (Baseline) 설정 및 관리
160. 형상 통제 위원회 (CCB) 요구사항 변경 심사
161. 범위 크리프 (Scope Creep) - 무분별한 요구사항 확장 방지
162. 골드 플래팅 (Gold Plating) - 요구사항에 없는 기능 임의 추가 (안티패턴)
163. 비즈니스 프로세스 모델링 (BPMN)
164. 유스케이스 시나리오 (Use Case Scenario) - 기본 흐름, 대안 흐름, 예외 흐름
165. 인수 기준 (Acceptance Criteria) 정의
166. MoSCoW 기법 - Must, Should, Could, Won't 우선순위 결정
167. 카노 모델 (Kano Model) - 당연적, 일원적, 매력적 품질
168. 품질 기능 전개 (QFD, Quality Function Deployment)
169. 품질의 집 (HoQ, House of Quality) 매트릭스
170. 도메인 분석 (Domain Analysis)
171. 요구사항 일관성 검사 (Consistency Checking)
172. 비즈니스 케이스 (Business Case) 및 ROI 분석
173. 이해관계자 (Stakeholder) 식별 및 영향도 매트릭스
174. 페어와이즈 (Pairwise) 우선순위 결정 기법
175. 요구사항 명세 언어 (Z, VDM 등 정형 언어)
176. 페트리 넷 (Petri Net) - 병행 시스템 명세
177. 요구사항 도구 (Jira, DOORS 등) 활용 전략
178. AS-IS (현재 상태) / TO-BE (미래 상태) 분석
179. SWOT 분석, 3C/4C 분석 연계 요구 도출
180. 마인드 맵 (Mind Map) 및 친화도 (Affinity Diagram)
181. 역공학을 통한 요구사항 추출
182. 에픽 (Epic) - 거시적 스토리 집합
183. 유저 스토리 맵 (User Story Mapping)
184. 테마 (Theme) - 에픽들의 상위 카테고리
185. 린 캔버스 (Lean Canvas) 1페이지 비즈니스 모델
186. 가치 제안 캔버스 (Value Proposition Canvas)
187. 소프트웨어 제품 라인 (SPL) 요구사항 가변성(Variability) 분석
188. 피쳐 모델 (Feature Model) 가변성 트리
189. BDD의 Given-When-Then 문법을 이용한 명세
190. AI(LLM) 기반 요구사항 명세서 초안 자동 생성 지원

## 4. 소프트웨어 설계 및 아키텍처 (80개)
191. 소프트웨어 설계 원칙 - 추상화, 캡슐화, 모듈화, 정보 은닉
192. 모듈 (Module) - 독립적 기능을 수행하는 단위
193. 응집도 (Cohesion) - 모듈 내부 요소들의 연관 정도 (높을수록 좋음)
194. 응집도 단계 - 우연적, 논리적, 시간적, 절차적, 통신적, 순차적, 기능적 응집도
195. 결합도 (Coupling) - 모듈 간 상호 의존 정도 (낮을수록 좋음)
196. 결합도 단계 - 내용, 공통, 제어, 스탬프, 자료 결합도
197. 팬인 (Fan-in) / 팬아웃 (Fan-out) - 모듈 복잡도 지표
198. 추상화 (Abstraction) - 제어, 자료, 과정 추상화
199. 정보 은닉 (Information Hiding) - 내부 구현 상세를 숨김
200. 분할과 정복 (Divide and Conquer)
201. 소프트웨어 아키텍처 (Software Architecture) 정의
202. 아키텍처 드라이버 (Architecture Drivers) - 비즈니스 목표, 제약, 품질 속성
203. 아키텍처 뷰 모델 (4+1 View) - 논리, 구현, 프로세스, 배치 + 유스케이스 뷰
204. 아키텍처 스타일 및 패턴 개요
205. 계층형 아키텍처 (Layered Architecture) - 관심사 분리 (Presentation, Business, Data)
206. 클라이언트-서버 아키텍처 (Client-Server)
207. 파이프-필터 아키텍처 (Pipe-Filter) - 데이터 스트림 처리
208. 브로커 패턴 (Broker Pattern) - 분산 시스템 메세지 중계
209. 블랙보드 패턴 (Blackboard Pattern) - 음성/패턴 인식, 공용 데이터소스를 여러 지식 모듈이 참조
210. 모델-뷰-컨트롤러 (MVC, Model-View-Controller)
211. MVP (Model-View-Presenter) / MVVM (Model-View-ViewModel)
212. 서비스 지향 아키텍처 (SOA, Service Oriented Architecture) - ESB 기반
213. 마이크로서비스 아키텍처 (MSA, Microservices Architecture)
214. 이벤트 드리븐 아키텍처 (EDA, Event-Driven Architecture)
215. 서버리스 아키텍처 (Serverless Architecture / FaaS)
216. 헥사고날 아키텍처 (Hexagonal Architecture / Ports and Adapters)
217. 클린 아키텍처 (Clean Architecture) - Robert C. Martin (Uncle Bob)
218. 어니언 아키텍처 (Onion Architecture)
219. 도메인 주도 설계 (DDD, Domain-Driven Design) - 에릭 에반스
220. 유비쿼터스 언어 (Ubiquitous Language) - 비즈니스와 기술의 공통 언어
221. 바운디드 컨텍스트 (Bounded Context) - 경계가 명확한 컨텍스트
222. 애그리게이트 (Aggregate) - 데이터 변경의 단위가 되는 객체 묶음
223. 컨텍스트 매핑 (Context Mapping) - 컨텍스트 간의 연동 관계 정의
224. 안티 코럽션 레이어 (ACL, Anti-Corruption Layer)
225. CQRS (Command Query Responsibility Segregation) - 명령과 조회 모델 분리
226. 이벤트 소싱 (Event Sourcing) - 상태 변경 이력을 이벤트 스트림으로 저장
227. 아키텍처 평가 기법 개요
228. SAAM (Software Architecture Analysis Method)
229. ATAM (Architecture Trade-off Analysis Method) - 품질 속성 간 상충 관계 분석
230. CBAM (Cost Benefit Analysis Method) - 경제적 관점의 평가
231. ADR (Architecture Decision Record) - 아키텍처 결정 기록
232. UML (Unified Modeling Language) - OMG 표준 객체지향 모델링 언어
233. 클래스 다이어그램 (Class Diagram) - 정적 구조 표현
234. 클래스 간 관계 - 일반화(상속), 실체화(인터페이스), 의존, 연관, 집합, 합성
235. 시퀀스 다이어그램 (Sequence Diagram) - 시간 흐름에 따른 상호작용 (동적)
236. 상태 다이어그램 (State Machine Diagram) - 객체의 상태 변화 (동적)
237. 액티비티 다이어그램 (Activity Diagram) - 처리 로직 및 워크플로우 (동적)
238. 유스케이스 다이어그램 (정적/기능)
239. 컴포넌트 다이어그램 / 배치 다이어그램 (Deployment Diagram) (정적/물리)
240. 통신 다이어그램 (Communication Diagram / Collaboration Diagram)
241. 패키지 다이어그램 / 복합 구조 다이어그램
242. 객체지향 설계 원칙 (SOLID)
243. SRP (Single Responsibility Principle) - 단일 책임 원칙
244. OCP (Open-Closed Principle) - 개방-폐쇄 원칙 (확장엔 열려있고 변경엔 닫혀있음)
245. LSP (Liskov Substitution Principle) - 리스코프 치환 원칙 (자식은 부모를 대체 가능)
246. ISP (Interface Segregation Principle) - 인터페이스 분리 원칙
247. DIP (Dependency Inversion Principle) - 의존 역전 원칙 (추상화에 의존)
248. DRY (Don't Repeat Yourself) 원칙
249. KISS (Keep It Simple, Stupid) 원칙
250. YAGNI (You Aren't Gonna Need It) 원칙
251. 디자인 패턴 (Design Patterns) 개요 - GoF (Gang of Four) 23가지
252. 생성 패턴 (Creational Patterns) - 객체 생성 메커니즘
253. 싱글톤 (Singleton) - 오직 하나의 인스턴스
254. 팩토리 메서드 (Factory Method) - 서브클래스가 생성할 객체 결정
255. 추상 팩토리 (Abstract Factory) - 구체적인 클래스 지정 없이 연관 객체군 생성
256. 빌더 (Builder) - 복잡한 객체를 단계별로 생성
257. 프로토타입 (Prototype) - 원본 객체를 복사하여 생성
258. 구조 패턴 (Structural Patterns) - 클래스/객체 조합
259. 어댑터 (Adapter) - 인터페이스 호환성 제공
260. 브리지 (Bridge) - 구현부에서 추상층을 분리
261. 컴포지트 (Composite) - 부분-전체 트리 구조 (단일 객체/복합 객체 동일 취급)
262. 데코레이터 (Decorator) - 동적으로 책임(기능) 추가
263. 퍼사드 (Facade) - 서브시스템에 대한 단순한 단일 인터페이스 제공
264. 프록시 (Proxy) - 대리 객체를 통한 접근 제어
265. 플라이웨이트 (Flyweight) - 인스턴스 공유로 메모리 절약
266. 행위 패턴 (Behavioral Patterns) - 알고리즘 및 책임 할당
267. 옵저버 (Observer) - 상태 변화 시 구독자에게 자동 알림
268. 전략 (Strategy) - 알고리즘을 캡슐화하여 동적으로 교체 가능
269. 템플릿 메서드 (Template Method) - 상위 클래스는 뼈대, 하위 클래스는 세부 구현
270. 이터레이터 (Iterator) - 내부 표현 노출 없이 순차 접근

## 5. 설계 심화 및 시스템 품질 (50개)
271. 커맨드 (Command) - 요청을 객체로 캡슐화 (Undo/Redo 지원)
272. 스테이트 (State) - 상태에 따라 객체 행위 변경
273. 중재자 (Mediator) - 객체 간의 복잡한 상호작용을 캡슐화하여 결합도 저하
274. 메멘토 (Memento) - 객체 상태 저장 및 복원
275. 방문자 (Visitor) - 객체 구조 변경 없이 새로운 연산 추가
276. 책임 연쇄 (Chain of Responsibility) - 요청을 처리할 수 있는 객체를 찾을 때까지 고리 전달
277. 해석자 (Interpreter) - 문법 규칙을 정의하고 해석
278. 동시성 패턴 (Concurrency Patterns) - Active Object, Monitor Object, Thread Pool
279. 아키텍처 품질 속성 (Quality Attributes) - 시나리오 기반 정의
280. 품질 시나리오 요소 - 자극원, 자극, 환경, 대상, 응답, 응답 척도
281. 가용성 (Availability) - 결함 탐지, 복구, 예방 전술
282. 성능 (Performance) - 자원 요구 관리, 자원 관리, 스케줄링 전술
283. 보안성 (Security) - 공격 탐지, 방어, 복구 전술
284. 유지보수성/변경용이성 (Modifiability) - 국소화, 결합 방지, 의존성 지연
285. 시험 용이성 (Testability) - 관찰 가능성, 제어 가능성 향상 전술
286. 사용성 (Usability) - 사용자 인터페이스 설계 전술
287. 상호운용성 (Interoperability) - 시스템 간 정보 교환 전술
288. 개념적 무결성 (Conceptual Integrity) - 아키텍처 전반의 일관성
289. UI/UX 설계 원칙 - 직관성, 유효성, 학습성, 유연성
290. 니코보코 (Nielsen-Norman) 10대 휴리스틱 원칙
291. 정보 아키텍처 (Information Architecture) 설계
292. 접근성 (Accessibility) - KWCAG, WCAG 웹 접근성 지침
293. 반응형 웹 디자인 (Responsive Web Design)
294. 다크 패턴 (Dark Pattern) 회피 설계
295. 시스템 신뢰성 모델링 - 직렬 모델, 병렬 모델
296. 결함 허용 (Fault Tolerance) 시스템 설계
297. N-버전 프로그래밍 (N-Version Programming) 다중화 설계
298. 페일 세이프 (Fail-Safe) - 고장 시 안전한 상태로 유지
299. 페일 소프트 (Fail-Soft) - 고장 시 기능은 저하되나 시스템 자체는 유지
300. 페일 오버 (Failover) - 장애 시 예비 시스템으로 자동 전환
301. 결함 회피 (Fault Avoidance) 기법
302. 보안 아키텍처 (Security Architecture) 설계
303. 인증 (Authentication) 및 인가 (Authorization) 패턴
304. 데이터 암호화 전송 및 저장 패턴
305. 마이크로서비스 설계 - API 게이트웨이 패턴
306. 서비스 디스커버리 (Service Discovery) 패턴
307. 서킷 브레이커 (Circuit Breaker) 패턴 - 연쇄 장애 방지
308. 벌크헤드 (Bulkhead) 패턴 - 스레드 풀 격리로 장애 전파 차단
309. 백엔드 포 프론트엔드 (BFF, Backend For Frontend) 패턴
310. 스트랭글러 피그 (Strangler Fig) 패턴 - 레거시를 점진적으로 MSA로 마이그레이션
311. 데이터베이스 퍼 서비스 (Database per Service) 패턴
312. 사가 (Saga) 패턴의 코레오그래피 (Choreography) vs 오케스트레이션 (Orchestration)
313. 로그 취합 아키텍처 (Log Aggregation Pattern)
314. 트랜잭셔널 아웃박스 (Transactional Outbox) 패턴
315. 마이크로 프론트엔드 (Micro Frontends) 아키텍처
316. 서버 사이드 렌더링 (SSR) vs 클라이언트 사이드 렌더링 (CSR)
317. 단일 페이지 애플리케이션 (SPA, Single Page Application) 설계
318. 프로그레시브 웹 앱 (PWA, Progressive Web App) 아키텍처
319. 웹어셈블리 (WebAssembly) 적용 아키텍처
320. 엣지 컴퓨팅 (Edge Computing) 분산 아키텍처 설계

## 6. 구현, 품질 관리 및 유지보수 (70개)
321. 프로그래밍 패러다임 - 절차적, 객체지향, 함수형, 논리형
322. 객체지향 프로그래밍 (OOP)의 4대 특징 - 캡슐화, 상속, 다형성, 추상화
323. 오버로딩 (Overloading) vs 오버라이딩 (Overriding)
324. 함수형 프로그래밍 (Functional Programming) - 일급 객체, 순수 함수, 불변성
325. 고차 함수 (Higher-Order Function) 및 클로저 (Closure)
326. 지연 평가 (Lazy Evaluation)
327. 반응형 프로그래밍 (Reactive Programming) - 데이터 스트림과 변화 전파
328. 코딩 컨벤션 (Coding Convention) 및 스타일 가이드
329. 시큐어 코딩 (Secure Coding) 원칙
330. 코드 리뷰 (Code Review) - 동료 검토 (Peer Review), 풀 리퀘스트 (PR) 기반 검토
331. 정적 분석 (Static Analysis) - 실행하지 않고 소스코드의 결함 탐지
332. 동적 분석 (Dynamic Analysis) - 실행 중 메모리 누수, 성능 병목 탐지
333. 가독성 (Readability) vs 효율성 (Efficiency) 트레이드오프
334. 클린 코드 (Clean Code) 원칙 - 의미 있는 이름, 작고 단일 역할의 함수, 주석의 최소화
335. 기술 부채 (Technical Debt)의 관리 및 상환 전략
336. 라이브러리 (Library) vs 프레임워크 (Framework) - 제어의 역전 (IoC, Inversion of Control) 차이
337. 의존성 주입 (DI, Dependency Injection) - 객체 결합도 감소
338. 관점 지향 프로그래밍 (AOP, Aspect Oriented Programming) - 횡단 관심사(Cross-cutting Concern) 분리
339. 소프트웨어 품질 (Software Quality)의 정의 (명시적, 묵시적 요구사항 충족)
340. ISO/IEC 9126 품질 특성 - 기능성, 신뢰성, 사용성, 효율성, 유지보수성, 이식성
341. ISO/IEC 25010 (SQuaRE) - 9126의 진화 모델 (보안성, 호환성 추가)
342. 기능 적합성 (Functional Suitability)
343. 성능 효율성 (Performance Efficiency)
344. 호환성 (Compatibility) / 사용성 (Usability)
345. 신뢰성 (Reliability) / 보안성 (Security)
346. 유지보수성 (Maintainability) / 이식성 (Portability)
347. 사용 품질 (Quality in Use) - 유효성, 생산성, 만족도, 리스크 완화
348. 맥콜(McCall)의 품질 모델 - 제품 운영, 제품 수정, 제품 전이 관점
349. 품질 비용 (COQ, Cost of Quality) - 예방 비용, 평가 비용, 내부 실패 비용, 외부 실패 비용
350. 전사적 품질 관리 (TQM, Total Quality Management)
351. 식스 시그마 (6 Sigma) - DMAIC (Define, Measure, Analyze, Improve, Control)
352. 결함(Defect)의 정의 - 오류(Error/Mistake), 결점(Fault/Bug), 고장/실패(Failure)
353. 결함 생명주기 - 발생, 등록, 분석, 할당, 수정, 조치 확인, 종료
354. 결함 심각도 (Severity) vs 결함 우선순위 (Priority)
355. 결함 밀도 (Defect Density) - 코드 규모(KLOC) 대비 결함 수
356. 신뢰성 성장 모델 (SRGM, Software Reliability Growth Model) - 고장 시간, 고장 간격 모델링
357. 가용성 (Availability) 계산 = MTBF / (MTBF + MTTR)
358. MTBF (Mean Time Between Failures) - 평균 무고장 시간
359. MTTR (Mean Time To Repair) - 평균 수리 시간
360. MTTF (Mean Time To Failure) - 평균 고장 시간
361. 소프트웨어 복잡도 측정 - 맥케이브 순환 복잡도 (McCabe's Cyclomatic Complexity, V(G) = e - n + 2)
362. 할스테드 (Halstead) 복잡도 - 연산자(Operator)와 피연산자(Operand) 수 기반 측정
363. 객체지향 메트릭 (CK 메트릭스) - WMC, DIT, NOC, CBO, RFC, LCOM
364. 정형 기술 검토 (FTR, Formal Technical Review) 의 지침
365. 소프트웨어 품질 보증 (SQA, Software Quality Assurance) 조직 및 활동
366. 골-질문-메트릭 (GQM, Goal-Question-Metric) 접근법 - 측정 지표 도출 기법
367. 품질 대시보드 (Quality Dashboard) 구축
368. 통계적 공정 관리 (SPC, Statistical Process Control) 및 정량적 관리
369. 소프트웨어 프로세스 개선 (SPI) 프레임워크 - IDEAL 모델
370. 코드 스멜 (Code Smell) - 리팩토링의 징후 (코드 중복, 거대 클래스, 긴 파라미터 목록)
371. 기술적 단편화 (Technical Fragmentation) 문제
372. 상용 소프트웨어 (COTS, Commercial Off-The-Shelf) 통합 및 품질
373. 오픈 소스 소프트웨어 (OSS) 거버넌스 - 라이선스(GPL, MIT, Apache 등) 컴플라이언스
374. 공급망 보안 (Supply Chain Security) - 오픈소스 취약점 관리
375. SBOM (Software Bill of Materials) - 소프트웨어 구성 요소 명세서 의무화 동향
376. 소프트웨어 빌드 및 배포 자동화의 품질 검증 단계
377. 체크섬(Checksum), 서명(Signature)을 통한 무결성(Integrity) 검증
378. 소프트웨어 문서화 (Documentation) 표준 및 지식 관리 (Wiki, Confluence)
379. 재해 복구 (DR) 아키텍처 - RTO (Recovery Time Objective), RPO (Recovery Point Objective)
380. 소프트웨어 유지보수의 종류 - 수정(Corrective), 적응(Adaptive), 완전/개선(Perfective), 예방(Preventive)
381. 메이먼의 법칙 (Lehman's Laws of Software Evolution) - 지속적 변경, 복잡도 증가의 법칙
382. 방어적 프로그래밍 (Defensive Programming) - 예외 처리, Assertion 적극 활용
383. 데이터 중심(Data-Centric) 아키텍처의 품질 보증
384. AI 기반 코드 생성기(Copilot 등) 산출물의 품질 평가 한계
385. 서버리스 환경의 콜드 스타트(Cold Start) 모니터링 및 튜닝
386. 지속 가능성 (Sustainability) 및 그린 코딩 (Green Coding) - 탄소 배출 저감 코드
387. 접근 통제 (Access Control) 패턴 로직 구현
388. 디자인 바이 컨트랙트 (Design by Contract) - 사전조건, 사후조건, 불변조건 명시
389. 리버스 엔지니어링 (Reverse Engineering) 툴을 통한 난독화 코드 분석
390. 애플리케이션 라이프사이클 관리 (ALM) 시스템 도입

## 7. 소프트웨어 테스팅 및 검증 심화 (80개)
391. 소프트웨어 테스팅의 7가지 원리 (결함 발견, 완벽한 테스트 불가능, 조기 테스트, 결함 집중, 살충제 패러독스, 정황 의존, 오류 부재의 궤변)
392. 살충제 패러독스 (Pesticide Paradox) 극복을 위한 테스트 케이스 주기적 갱신
393. 오류 부재의 궤변 (Absence of Errors Fallacy) - 요구사항 미충족 시 결함이 없어도 무용지물
394. V-모델의 매핑 (요구사항-인수테스트, 기본설계-시스템테스트, 상세설계-통합테스트, 코딩-단위테스트)
395. 검증 (Verification) - 제품을 올바르게 만들고 있는가 (과정, 산출물 리뷰)
396. 확인 (Validation) - 올바른 제품을 만들었는가 (결과, 실행 테스트)
397. 단위 테스트 (Unit Test) - 최소 단위(모듈/함수) 기능 검증, 화이트박스 위주
398. 단위 테스트 프레임워크 (JUnit, pytest, NUnit 등)
399. 목 객체 (Mock Object) 기반 격리 테스트
400. 통합 테스트 (Integration Test) - 모듈 간 인터페이스 및 상호작용 검증
401. 빅뱅 통합 (Big Bang Integration) - 한 번에 모두 결합 (오류 추적 어려움)
402. 하향식 통합 (Top-down Integration) - 깊이/넓이 우선, 하위 모듈 대체용 스텁(Stub) 사용
403. 상향식 통합 (Bottom-up Integration) - 클러스터 결합, 상위 제어 모듈 대체용 드라이버(Driver) 사용
404. 샌드위치 통합 (Sandwich / Hybrid Integration) - 주요 모듈 중심 상/하향 병행
405. 시스템 테스트 (System Test) - 전체 시스템의 기능 및 비기능 요구사항 검증
406. 인수 테스트 (Acceptance Test) - 사용자(고객)가 요구사항 충족 여부 최종 확인
407. 알파 테스트 (Alpha Test) - 개발자 환경에서 통제된 사용자 테스트
408. 베타 테스트 (Beta Test) - 실제 환경에서 다수 사용자가 수행 (필드 테스트)
409. OAT (Operational Acceptance Testing) - 운영 전환 전 백업, 이중화 등 검증
410. 회귀 테스트 (Regression Test) - 코드 수정 후 기존 기능에 예기치 않은 결함(사이드 이펙트) 발생 확인
411. 리그레션 테스트 자동화 및 선택적 수행 (Retest All vs Selective)
412. 블랙박스 테스트 (Black-box Test / 명세 기반 테스트) - 내부 구조를 보지 않고 입력/출력 기반 검증
413. 동등 분할 (Equivalence Partitioning) - 입력 영역을 유효/무효 클래스로 분할하여 대푯값 테스트
414. 경계값 분석 (Boundary Value Analysis) - 경계 부분에서 결함이 많다는 점 이용 (분할의 가장자리 값)
415. 의사 결정 테이블 (Decision Table) - 복잡한 논리적 조건들의 조합을 표로 구성하여 테스트
416. 상태 전이 테스트 (State Transition Testing) - 객체의 상태 변화 시나리오 검증
417. 유스케이스 테스팅 (Use Case Testing) - 액터와의 상호작용 흐름 기반
418. 페어와이즈 테스팅 (Pairwise Testing) - 변수 값들의 모든 쌍(Pair) 조합이 최소 한 번 테스트되도록 최적화 (조합 폭발 방지)
419. 원인-결과 그래프 (Cause-Effect Graphing)
420. 화이트박스 테스트 (White-box Test / 구조 기반 테스트) - 소스코드의 내부 논리 구조를 모두 검증
421. 제어 흐름 테스트 (Control Flow Testing)
422. 구문 커버리지 (Statement Coverage) - 코드의 모든 문장을 최소 한 번 실행
423. 결정 커버리지 (Decision Coverage / 분기 커버리지) - 분기문(If, While 등)의 참/거짓을 최소 한 번씩 실행
424. 조건 커버리지 (Condition Coverage) - 분기문 내의 각 개별 조건식이 참/거짓을 한 번씩 가짐
425. 조건/결정 커버리지 (Condition/Decision Coverage) - 개별 조건과 전체 결정이 모두 참/거짓을 가짐
426. 변경 조건/결정 커버리지 (MC/DC, Modified Condition/Decision Coverage) - 각 개별 조건이 독립적으로 전체 결과에 영향을 미침을 증명 (DO-178B/C 항공/안전 표준)
427. 다중 조건 커버리지 (Multiple Condition Coverage) - 개별 조건의 모든 가능한 진리값 조합 (2^N)
428. 경로 커버리지 (Path Coverage) - 가능한 모든 실행 경로를 테스트
429. 데이터 흐름 테스팅 (Data Flow Testing) - 변수의 정의(Define)와 사용(Use) 경로 (DU 경로) 기반 검증
430. 정적 테스팅 (Static Testing) - 코드를 실행하지 않고 리뷰나 도구를 통해 검증 (인스펙션, 정적 분석)
431. 동적 테스팅 (Dynamic Testing) - 코드를 직접 컴파일하고 실행하여 검증
432. 리스크 기반 테스팅 (Risk-based Testing) - 비즈니스 리스크가 높은 모듈에 테스트 자원 집중
433. 탐색적 테스팅 (Exploratory Testing) - 명세서 없이 테스터의 직관과 경험을 바탕으로 테스트 설계와 수행을 동시 진행 (차터, 타임박스 활용)
434. 오류 추정 (Error Guessing) - 테스터의 경험을 바탕으로 결함이 발생할 만한 곳을 추정하여 테스트
435. 체크리스트 (Checklist) 기반 테스팅
436. 테스트 오라클 (Test Oracle) - 테스트 결과의 참/거짓을 판단하기 위한 기준
437. 참 오라클 (True Oracle) - 모든 입력에 대해 기대 결과 제공 (현실적 적용 어려움)
438. 샘플링 오라클 (Sampling Oracle) - 특정 몇몇 입력 값에 대해서만 결과 제공
439. 휴리스틱 오라클 (Heuristic Oracle) - 샘플링에 직관적/경험적 판단 추가
440. 일관성 오라클 (Consistent Oracle) - 변경 전/후의 결과가 동일한지 확인 (회귀 테스트에 유용)
441. 테스트 케이스 (Test Case) 구조 - 식별자, 전제조건, 입력 데이터, 기대 결과
442. 테스트 시나리오 (Test Scenario) - 테스트 케이스들을 흐름에 따라 묶은 집합
443. 테스트 절차 (Test Procedure) / 테스트 스크립트 (Test Script)
444. 테스트 데이터 (Test Data) 생성 및 익명화 관리 (Test Data Management, TDM)
445. 성능 테스트 (Performance Test) 4가지 유형
446. 부하 테스트 (Load Test) - 시스템의 임계점(목표치)까지 부하를 증가시키며 상태 확인
447. 스트레스 테스트 (Stress Test) - 임계점 이상의 과부하 상태에서 시스템 붕괴 및 복구 반응 확인
448. 스파이크 테스트 (Spike Test) - 갑작스럽게 사용자가 급증할 때의 반응 확인
449. 내구성 테스트 (Endurance / Soak Test) - 장시간 부하를 주어 메모리 누수(Leak) 등 확인
450. 벤치마크 테스트 (BMT, Benchmark Test) - 동일한 환경에서 여러 제품의 성능을 비교
451. 사용성 테스트 (Usability Test) - 사용자가 시스템을 얼마나 쉽게 다룰 수 있는지 UI/UX 관점 평가
452. A/B 테스트 - 두 가지 UI/기능을 실 사용자에게 노출하여 반응 비교
453. 호환성 테스트 (Compatibility Test) - OS, 브라우저, 기기(모바일) 등 이기종 환경 동작 확인
454. 이식성 테스트 (Portability Test) - 다른 환경으로 시스템을 이전했을 때의 동작 확인
455. 모의 해킹 (Penetration Testing) 및 취약점 스캐닝
456. 뮤테이션 테스팅 (Mutation Testing / 돌연변이 테스팅) - 원본 코드에 고의로 에러(돌연변이)를 주입하여 기존 테스트 케이스가 이를 잡아내는지(Kill) 검증 (테스트 케이스의 품질 평가)
457. 퍼즈 테스팅 (Fuzz Testing / Fuzzing) - 무작위 또는 기형적인 데이터를 입력하여 크래시(Crash)나 예외 상황 유발
458. 테스트 더블 (Test Double) 5가지 개념 (xUnit 테스트 패턴)
459. Dummy (더미) - 인자 채우기용, 실제 사용 안됨
460. Stub (스텁) - 호출 시 준비된 답변만 반환 (상태 검증용)
461. Spy (스파이) - 스텁 역할 + 호출 정보 기록
462. Mock (목) - 행위(Behavior) 검증을 위해 예상되는 호출 명세가 프로그래밍된 객체
463. Fake (페이크) - 실제 동작하지만 프로덕션에는 적합하지 않은 축소판 (인메모리 DB 등)
464. 서비스 가상화 (Service Virtualization) - MSA 환경에서 외부 의존 API를 모사하는 스텁 서버
465. 지속적 테스팅 (Continuous Testing) - CI/CD 파이프라인 전 과정에 테스트 자동화 통합
466. 시프트 레프트 테스팅 (Shift-Left Testing) - 테스트 활동을 개발 초기(왼쪽) 단계로 당겨 결함 조기 발견
467. 시프트 라이트 테스팅 (Shift-Right Testing) - 운영 환경(오른쪽)에서의 테스트 (카나리, 카오스 엔지니어링)
468. 운영 환경 테스트 (Testing in Production / TiP)
469. 모델 기반 테스팅 (MBT, Model-Based Testing) - 시스템 모델(UML 등)에서 테스트 케이스 자동 생성
470. TDD (Test Driven Development) 생명주기 - 실패하는 테스트 작성(Red) -> 통과하는 최소 코드 작성(Green) -> 리팩토링(Refactor)

## 8. SW 보안 (DevSecOps) 및 컴플라이언스 (60개)
471. 소프트웨어 개발 보안 (Secure SDLC) - 기획, 설계, 구현, 테스트 전 단계 보안 활동
472. BSIMM (Building Security In Maturity Model) - SW 보안 성숙도 평가 모델
473. Microsoft SDL (Security Development Lifecycle) - 7단계 보안 생명주기
474. 위협 모델링 (Threat Modeling) 아키텍처 보안 분석
475. STRIDE 모델 - Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
476. DREAD 모델 - 위협 리스크 산정 지표 (Damage, Reproducibility, Exploitability, Affected users, Discoverability)
477. OWASP Top 10 (2021 기준 주요 취약점)
478. Broken Access Control (취약한 접근 제어)
479. Cryptographic Failures (암호화 실패 / 민감 데이터 노출)
480. Injection (인젝션 / SQLi, OS Command, NoSQL 등)
481. Insecure Design (안전하지 않은 설계)
482. Security Misconfiguration (보안 설정 오류)
483. Vulnerable and Outdated Components (취약하고 만료된 컴포넌트)
484. Identification and Authentication Failures (인증 및 세션 관리 실패)
485. Software and Data Integrity Failures (소프트웨어 및 데이터 무결성 실패)
486. Security Logging and Monitoring Failures (보안 로깅 및 모니터링 실패)
487. SSRF (Server-Side Request Forgery) - 서버 측 요청 위조
488. CWE (Common Weakness Enumeration) - 보안 약점 사전
489. CVE (Common Vulnerabilities and Exposures) - 공개된 보안 취약점 목록
490. CVSS (Common Vulnerability Scoring System) - 취약점 위험도 평가 점수 (0~10)
491. SAST (Static Application Security Testing) - 소스코드 정적 분석 도구 (보안 룰셋 기반)
492. DAST (Dynamic Application Security Testing) - 런타임 환경에 공격 페이로드 주입 분석 (블랙박스)
493. IAST (Interactive Application Security Testing) - SAST와 DAST 결합, 에이전트 기반 내부 메모리/흐름 분석
494. RASP (Runtime Application Self-Protection) - 실행 환경 내부에서 공격 실시간 방어
495. SCA (Software Composition Analysis) - 오픈소스 라이브러리 취약점 및 라이선스 스캔
496. SBOM (Software Bill of Materials) 포맷 - SPDX, CycloneDX
497. 행정안전부/KISA 소프트웨어 개발 보안 가이드 (47개 보안 약점)
498. 입력 데이터 검증 및 표현 (Input Validation) 원칙
499. SQL 인젝션 방어 - Prepared Statement (파라미터화된 쿼리), ORM 프레임워크 사용
500. 크로스 사이트 스크립팅 (XSS) 방어 - 입/출력값 인코딩, CSP(Content Security Policy) 헤더 설정
501. XSS 유형 - Reflected XSS, Stored XSS, DOM-based XSS
502. 크로스 사이트 요청 위조 (CSRF) 방어 - Anti-CSRF 토큰 발급, SameSite 쿠키 속성
503. 보안 기능 (Security Features)의 설계
504. 암호화 알고리즘 (대칭키-AES, 비대칭키-RSA/ECC, 일방향-SHA) 적용 기준
505. 비밀번호 저장 방식 - KDF(Key Derivation Function) 활용 (PBKDF2, bcrypt, scrypt, Argon2) 및 솔트(Salt) 적용
506. 양자 내성 암호 (PQC) 전환 대비 SW 아키텍처 검토
507. 세션 관리 (Session Management) 보완 - 만료 시간, 재사용 방지, 세션 ID 추측 난해성
508. 인증 (Authentication) 트렌드 - MFA, FIDO, WebAuthn, 패스워드리스(Passwordless)
509. 인가 (Authorization) 모델 - RBAC(역할 기반), ABAC(속성 기반, 조건부 규칙)
510. API 보안 관리 - OAuth 2.0 (Access Token 인가), OIDC(인증), JWT(JSON Web Token) 서명/만료 검증
511. API Rate Limiting (비율 제한) 및 Throttling (스로틀링) - DDoS 및 크롤링 방어
512. 마이크로서비스 간 보안 (Service-to-Service Security) - mTLS (상호 TLS 인증)
513. 컨테이너 보안 - 이미지 스캐닝, 루트 권한 실행 금지 (Non-root user), 네임스페이스 샌드박스
514. 시크릿(Secret) 관리 도구 - 하드코딩 금지, HashiCorp Vault, AWS Secrets Manager 활용
515. 쿠버네티스 (Kubernetes) 보안 - RBAC, Network Policy, Pod Security Admission
516. 개인정보 보호 중심 설계 (Privacy by Design - PbD) 7원칙
517. 데이터 3법 및 GDPR 컴플라이언스 대응 SW 기능 (잊혀질 권리, 동의 철회 기능)
518. 가명 처리 및 비식별화 기술 (K-익명성, L-다양성, T-근접성) SW 적용
519. 사이버 레질리언스 (Cyber Resilience) 아키텍처
520. 공급망 (Supply Chain) 공격 사례 및 서명된 커밋(Signed Commit), CI 파이프라인 보호
521. 인공지능 모델 공격 방어 - 적대적 예제(Adversarial Example), 데이터 포이즈닝 방어 설계
522. 블록체인/스마트 컨트랙트 (Smart Contract) 보안 감사 (Reentrancy 공격 방어 등)
523. IoT 기기 펌웨어 무결성 검증망 및 OTA (Over-The-Air) 안전 배포
524. 클라우드 보안 형상 관리 (CSPM) 연동 개발 프로세스
525. 컴플라이언스 애즈 코드 (Compliance as Code) 자동화
526. 보안 로깅 (Logging) - 6하 원칙 기록, 중앙 집중식 보관(ELK), 위변조 방지 (WORM 스토리지)
527. 보안 감사 (Audit) 트레일 추적 기능
528. 난독화 (Obfuscation) 및 안티 디버깅 (Anti-debugging) 적용 (모바일 앱 보안)
529. 메모리 안전성(Memory Safety) 보장을 위한 Rust, Go 언어 도입 동향
530. 보안 조직 분리 정책 위반(SoD, Segregation of Duties)의 SW 통제 로직

## 9. SW 아키텍처 심화, 클라우드 네이티브 및 AI (80개)
531. 클라우드 네이티브 아키텍처 (Cloud Native Architecture) 철학
532. 마이크로서비스 (Microservices) 분해 패턴
533. 비즈니스 능력에 따른 분해 (Decompose by Business Capability)
534. 하위 도메인에 따른 분해 (Decompose by Subdomain - DDD 기반)
535. 서비스 간 동기 통신 - REST API, gRPC (Protocol Buffers)
536. 서비스 간 비동기 통신 - 메시지 큐 (RabbitMQ, Kafka), AMQP 프로토콜
537. 안티패턴: 분산 모놀리스 (Distributed Monolith) - 독립 배포 불가능한 MSA
538. 이벤트 기반 아키텍처 (EDA) - 이벤트 생산자, 브로커, 소비자 
539. 이벤트 버스 (Event Bus) 및 스트림 프로세싱
540. 서비스 디스커버리 (Service Discovery) - 동적 IP/Port 레지스트리 (Eureka, Consul)
541. 클라이언트 사이드 디스커버리 vs 서버 사이드 디스커버리
542. API 게이트웨이 (API Gateway) - 인증, 라우팅, 로드밸런싱, 통합(Aggregation)
543. BFF (Backend For Frontend) - 모바일, 웹 등 클라이언트 전용 맞춤형 게이트웨이
544. 외부화된 구성 관리 (Externalized Configuration) - Config Server (Spring Cloud Config 등)
545. 서비스 메시 (Service Mesh) - 애플리케이션 외부(인프라 계층)에서 통신 제어
546. 사이드카 (Sidecar) 프록시 패턴 - Istio, Envoy, Linkerd
547. 트래픽 라우팅, 카나리 배포 제어 (Service Mesh의 역할)
548. 로컬 트랜잭션 (Local Transaction) vs 분산 트랜잭션 (Distributed Transaction)
549. 2PC (Two-Phase Commit)의 MSA 적용 한계
550. 사가 패턴 (Saga Pattern) - 로컬 트랜잭션들의 연속된 체인
551. 보상 트랜잭션 (Compensating Transaction) - 롤백을 논리적으로 수행하는 역방향 연산
552. 오케스트레이션 사가 (Orchestration Saga) - 중앙 통제기가 흐름 제어
553. 코레오그래피 사가 (Choreography Saga) - 이벤트 구독 기반의 자율적 흐름
554. CQRS (명령과 조회 책임 분리) - 쓰기 DB와 읽기 DB 분리, 동기화 문제 해결 (Eventual Consistency)
555. 이벤트 소싱 (Event Sourcing) - CRUD 대신 상태 변경 이력(Event) 자체를 추가(Append-only) 저장
556. 마이크로 프론트엔드 (Micro Frontends) - 모놀리식 프론트엔드를 독립적 팀 단위 컴포넌트로 분할
557. 모듈 페더레이션 (Module Federation) (Webpack) 
558. 서버리스 아키텍처 (Serverless / FaaS)
559. 콜드 스타트 (Cold Start) 지연 문제 및 극복 방안 (Provisioned Concurrency 등)
560. 데이터 메시 (Data Mesh) - 데이터 소유권의 탈중앙화 (도메인 중심)
561. 컨테이너 (Container) 기반 배포 아키텍처
562. 도커(Docker) 이미지 계층(Layer) 최소화 기법
563. 쿠버네티스 (Kubernetes) 오브젝트 아키텍처 (Pod, Service, Deployment, Ingress)
564. 헬름 (Helm) 차트를 이용한 SW 패키지 관리
565. 오퍼레이터 (Operator) 패턴 - 쿠버네티스 사용자 정의 컨트롤러 확장을 통한 복잡한 앱 관리 자동화
566. 옵저버빌리티 (Observability / 가시성) 아키텍처
567. 메트릭 (Metrics) - 시계열 데이터 수집 (Prometheus, Grafana)
568. 로그 (Logs) - 분산 로그 수집 (ELK Stack - Elasticsearch, Logstash, Kibana / Fluentd)
569. 분산 추적 (Distributed Tracing) - 트랜잭션 경로 추적 (OpenTelemetry, Jaeger, Zipkin)
570. Trace ID와 Span ID의 전파 (Context Propagation)
571. 탄력성 (Resiliency) 및 결함 허용 (Fault Tolerance) 패턴
572. 서킷 브레이커 (Circuit Breaker) - 상태(Closed, Open, Half-Open) 기반 장애 확산 차단 (Resilience4j)
573. 타임아웃 (Timeout) 및 재시도 (Retry) 백오프(Backoff) 전략
574. 벌크헤드 (Bulkhead) - 스레드 풀 격리로 일부 장애가 전체 리소스 고갈로 이어지는 현상 방지
575. 섀도우 배포 (Shadow Deployment / 트래픽 미러링) - 실운영 트래픽을 복제하여 신규 버전에 테스트
576. 피처 플래그 (Feature Flag) 기반 A/B 테스트 및 점진적 롤아웃
577. 서버 사이드 렌더링 (SSR) 컴포넌트 아키텍처 (Next.js, Nuxt.js)
578. 정적 사이트 생성 (SSG) / 증분 정적 재생성 (ISR) 패턴
579. 오프라인 우선 (Offline-first) 아키텍처 (PWA, Service Worker, IndexedDB)
580. 웹어셈블리 (WebAssembly, WASM) 아키텍처 - 브라우저 내 고성능 네이티브 코드 실행
581. AI4SE (AI for Software Engineering) - AI를 활용한 SW 엔지니어링 패러다임 변화
582. LLM(대규모 언어 모델) 기반 코드 생성 지원 도구 (GitHub Copilot, Cursor 등)
583. AI 어시스턴트 코드 산출물의 라이선스 충돌(저작권) 이슈 및 보안 위협 (Hallucination 버그)
584. 프롬프트 엔지니어링 (Prompt Engineering) 가이드라인 설계
585. RAG (Retrieval-Augmented Generation) 패턴 아키텍처 통합 설계
586. 랭체인 (LangChain) 프레임워크 기반 AI 파이프라인 설계
587. 에이전틱 AI (Agentic AI) 시스템 - 도구(Tool)를 직접 호출하는 자율형 SW 모듈 설계
588. MLOps 파이프라인 - 데이터 수집, 모델 학습(Training), 서빙(Serving), 모니터링 자동화
589. 모델 드리프트 (Model Drift / Data Drift) 모니터링 및 재학습 루프 설계
590. 엣지 AI (Edge AI) / 온디바이스 AI (On-Device AI) - 모델 경량화 (양자화, 가지치기, 지식 증류) 아키텍처
591. 양자 컴퓨팅 (Quantum Computing) 알고리즘 (쇼어 알고리즘 등)에 대비한 하이브리드 아키텍처 연구
592. 블록체인 DApp (Decentralized Application) 아키텍처 - 프론트엔드 + 스마트 컨트랙트 + IPFS
593. 디지털 트윈 (Digital Twin) 소프트웨어 통합 통신 아키텍처
594. 메타버스 (Metaverse) 실시간 동기화 아키텍처 및 렌더링 오프로딩
595. RPA (Robotic Process Automation) 봇 결합 아키텍처
596. 로우코드/노코드 (Low-Code / No-Code) 플랫폼 아키텍처 한계와 확장성 제어
597. 헤드리스 (Headless) CMS 아키텍처 - 프론트엔드와 백엔드 분리 유연성 제공
598. 마이크로 커널 (Microkernel / 플러그인) 아키텍처 - 이클립스, VS Code 확장 구조
599. 모듈러 모놀리스 (Modular Monolith) 아키텍처 - MSA 전환 전 단계, 모듈 간 강결합 방지 아키텍처
600. 아키텍처 런웨이 (Architecture Runway) - 비즈니스 요구 수용을 위해 사전에 마련하는 기술적 기반 구조

## 10. 최신 트렌드 및 프로젝트 관리/품질 심화 (200개 요약)
601. 객체지향 5원칙 SOLID 완벽 매핑
602. 정보 은닉(Information Hiding) 캡슐화 연계
603. 컴포넌트(Component) 독립 배포 단위
604. 디자인 패턴 23가지 구조적 분류
605. 싱글톤 패턴 메모리/쓰레드 세이프 설계
606. 옵저버 패턴 (Pub/Sub 연계)
607. 팩토리 메서드 vs 추상 팩토리 
608. 전략 패턴 알고리즘 교체 용이성
609. 파이프-필터 아키텍처 스트림 
610. MVC, MVP, MVVM 프론트엔드 패턴 진화
611. 클린 아키텍처 의존성 규칙 (내부로만 향함)
612. 헥사고날 포트와 어댑터 외부 격리
613. 도메인 주도 설계 (DDD) 기본 구성 (엔티티, VO, 리포지토리)
614. 바운디드 컨텍스트 마이크로서비스 식별 기준
615. 애그리게이트 루트 트랜잭션 경계
616. 마이크로서비스 API 게이트웨이 인증 통합 
617. 서비스 디스커버리 Eureka 
618. 서킷 브레이커 장애 연쇄 차단 메커니즘
619. 사가 (Saga) 패턴 2PC 한계 극복 분산 트랜잭션
620. 이벤트 소싱 상태 재생 가능성 보장
621. CQRS 읽기 쓰기 분리 스케일 아웃
622. 모듈러 모놀리스 MSA 대안적 접근 
623. 서버리스 콜드 스타트 이슈
624. 클라우드 네이티브 12 Factor App 
625. 테스트 더블 Mock과 Stub의 차이 
626. V-모델 개발-테스트 매핑 구조
627. 회귀 테스트 커버리지 도구 
628. 살충제 패러독스 테스트 갱신
629. 오류 부재의 궤변 요구사항 미달 
630. 동등 분할 (Equivalence Partitioning) 경계값 분석 
631. 결정 테이블 (Decision Table) 논리 조합 
632. 상태 전이 (State Transition) 다이어그램 
633. 페어와이즈 (Pairwise) 직교 배열 (Orthogonal Array) 
634. 구문, 분기, 조건 커버리지 포함 관계 
635. MC/DC 항공/자동차 안전 표준 조건
636. 탐색적 테스트 차터 기반 휴리스틱
637. 퍼즈 테스트 보안 취약점 발견 
638. 뮤테이션 테스트 (돌연변이) 테스트 케이스 검증 
639. A/B 테스팅 
640. 성능 테스트 부하/스트레스/스파이크/인듀어런스 
641. ISO 25010 소프트웨어 품질 모델 
642. 신뢰성 (MTBF, MTTR, MTTF) 가용성 공식
643. 결함 밀도 측정 및 프로세스 통제
644. 기술 부채 마틴 파울러 사분면 
645. 리팩토링 악취(Code Smell) 제거 
646. 코드 리뷰 페어 프로그래밍
647. FTR (정형 기술 검토) 인스펙션/워크스루 
648. 소프트웨어 형상 관리 (SCM) 통제 위원회 CCB 
649. 기준선 (Baseline) 수립 변경 통제 
650. CI/CD 지속적 통합, 배포 파이프라인
651. 카나리 배포 / 블루-그린 배포 무중단 
652. 데브옵스 (DevOps) CALMS 문화 
653. 데브섹옵스 (DevSecOps) 시프트 레프트 
654. SRE SLI, SLO, SLA 에러 예산
655. 카오스 엔지니어링 카오스 몽키 복원력 
656. GitOps 인프라 선언적 관리 
657. 옵저버빌리티 로그, 메트릭, 분산 추적(Tracing) 
658. 애자일 스크럼 (Scrum) 역할 분담 
659. 스프린트 백로그 / 프로덕트 백로그 
660. 번다운 차트 작업 진척도 
661. 칸반 WIP (Work In Progress) 제한 
662. XP 테스트 주도 개발 (TDD) 리팩토링 
663. 스토리 포인트 플래닝 포커 합의 
664. 대규모 애자일 SAFe, LeSS 
665. 린 스타트업 MVP 피벗 사이클 
666. 요구사항 도출 JAD 페르소나
667. 요구사항 검증 추적성 매트릭스 (RTM)
668. 비기능 요구사항 아키텍처 드라이버 
669. DFD 자료 흐름도 4요소 
670. 유스케이스 포함(Include) 확장(Extend) 
671. UML 클래스, 시퀀스, 액티비티 다이어그램 
672. 소프트웨어 비용 산정 COCOMO 
673. 기능점수 (FP) 내부논리파일(ILF) 외부연계파일(EIF) 
674. 델파이 기법 전문가 합의 
675. 프로젝트 관리 WBS, CPM, PERT 
676. EVM (Earned Value Management) SPI, CPI 계산 
677. CMMI 성숙도 5단계 (초기-관리-정의-정량-최적)
678. SPICE 프로세스 역량 평가 
679. 소프트웨어 재공학 역공학 
680. 역 콘웨이 전략 아키텍처에 맞춘 조직 구성 
681. 모노레포 vs 멀티레포 
682. 마이크로 프론트엔드 웹팩 연계 
683. API 게이트웨이 BFF (Backend for Frontend)
684. 스트랭글러 패턴 레거시 분할 
685. 토일 (Toil) 자동화 축소 대상 작업 
686. 인지 부하 (Cognitive Load) 팀 토폴로지 
687. 시큐어 코딩 입력값 검증 XSS SQLi 방어 
688. SAST / DAST / IAST 보안 테스팅 도구 비교 
689. RASP 런타임 자체 보호 
690. 소프트웨어 자재 명세서 (SBOM) 공급망 보안 
691. 오픈소스 컴플라이언스 GPL 카피레프트 
692. 위협 모델링 STRIDE 
693. 제로 트러스트 아키텍처 최소 권한 원칙 
694. 기밀 컴퓨팅 데이터 인 유즈(In Use) 보호 
695. 사이버 레질리언스 시스템 생존성 
696. AI 기반 코드 생성 코파일럿 프롬프트 
697. LLM 환각 방지 RAG 아키텍처 
698. MLOps 데이터 드리프트 모니터링 
699. 데이터 메시 탈중앙 도메인 오너십 
700. 서버리스 FaaS 아키텍처 제약 
701. WebAssembly (Wasm) 프론트 성능 가속 
702. PWA (Progressive Web App) 오프라인 워커 
703. 백파이어링 FP LOC 역산 
704. 피쳐 플래그 런타임 기능 토글 
705. 서비스 메시 (Istio) 사이드카 통신 제어 
706. 트랜잭셔널 아웃박스 이벤트 유실 방지 
707. OAT (운영 인수 테스트) 백업 복구 검증 
708. 블랙보드 패턴 비결정적 문제 해결 
709. 브로커 패턴 분산 시스템 미들웨어 
710. ATDD (인수 테스트 주도 개발) BDD 연계 
711. KWCAG 웹 접근성 지침 
712. 다크 패턴 기만적 UX 방지 
713. 기능 안전 ISO 26262 ASIL 등급 
714. FMEA / FTA 결함 분석망 
715. N-버전 프로그래밍 이종 다중화 
716. 페일 세이프 / 페일 소프트 비교 
717. 클라우드 네이티브 스토리지 컴퓨팅 분리 
718. 블록체인 DApp 스마트 컨트랙트 구조 
719. 양자 컴퓨팅 대비 PQC 소프트웨어 구조 전환 
720. 데이터옵스 (DataOps) 자동화 
721. 클린 아키텍처 Usecase Interactor 설계 
722. 어니언 아키텍처 도메인 코어 격리 
723. COTS 상용 기성품 통합 테스팅 
724. 인프라스트럭처 애즈 코드 (IaC) 테라폼 
725. 선언적 인프라 상태 일치 루프 
726. 플랫폼 엔지니어링 IDP 포털 개발자 경험(DX)
727. DORA 메트릭스 4대 지표 (배포 빈도 등) 
728. SPACE 프레임워크 생산성 다각화 
729. 객체지향 결합도 (내용, 공통, 제어, 스탬프, 자료) 
730. 객체지향 응집도 (우연, 논리, 시간, 절차, 통신, 순차, 기능) 
731. ATAM 트레이드오프 분석 평가 트리 
732. TQM 전사적 품질 관리 예방 위주 
733. GQM 지표 측정 골 기반 구조 
734. 방어적 프로그래밍 Assertion 계약 기반 설계 
735. 디자인 바이 컨트랙트 불변 조건 
736. 로그 6하 원칙 WORM 스토리지 무결성 
737. SBOM 규격 SPDX CycloneDX 
738. 컨테이너 이미지 스캐닝 권한 통제 
739. MFA 인증 OIDC 인가 보안 구조 
740. API 스로틀링 Rate Limit DDoS 방어 
741. mTLS 상호 인증 서비스 간 보안 
742. K-익명성 프라이버시 디자인(PbD) 설계 
743. 데이터 마스킹 FPE 암호 유지 
744. 엣지 컴퓨팅 데이터 로컬 최적화 
745. 디지털 트윈 동기화 인터페이스 모델 
746. 메타버스 네트워크 렌더링 지연 단축 기술 
747. 탄소 인지적 소프트웨어 그린 코딩 
748. 로우코드/노코드 섀도우 IT 거버넌스 
749. 마이크로 커널 아키텍처 플러그인 확장 
750. 아키텍처 런웨이 기술적 기반 조기 확보 
751. 소프트웨어 위기 비용 지연 품질 문제 
752. 프로토타입 버리기 모델 vs 진화적 모델 
753. 나선형 위험 분석 4단계 루프 
754. 테일러링 프로젝트 맞춤형 프로세스 재단 
755. PMO 전사 품질 통제 및 감사 조직 
756. 잭맨 프레임워크 6x6 매트릭스 
757. MoSCoW 요구사항 우선순위 판별 
758. Kano 모델 매력적, 당연적 품질 요소 분류 
759. QFD 품질 기능 전개 요구사항 변환 기법 
760. 인스펙션 중재자(Moderator) 주도 공식 검토 
761. 워크스루 비공식 기술 검토 회의 
762. 애자일 에픽, 스토리, 테마, 태스크 계층 
763. 지속적 통합 테스트 빌드 자동화 서버 
764. 리드 타임 프로세스 시작부터 배포 완료 
765. 누적 흐름도 병목 지점 병목 분석 
766. 소프트웨어 노후화 기술 부채 연계 
767. 객체지향 추상화 자료/제어/과정 분리 
768. 럼바우 객체 모델링 (객체/동적/기능 모델) 
769. 구조적 분석 도구 데이터 사전(DD) 표기법 
770. 페트리 넷 병행/비동기 시스템 정형 명세 
771. BDD Given-When-Then 행동 명세 테스트 
772. ATDD 인수 테스트 주도 개발 구조 
773. 테스트 하네스 스텁, 드라이버, 슈트 포괄 환경 
774. 소프트웨어 안전성 Fail-Safe, Fail-Soft 
775. 정보시스템 감리 절차 모델 
776. 소프트웨어 품질 비용 통제 그래프 최적점 
777. 정량적 프로젝트 관리 SPI 통제 한계선 
778. 소프트웨어 테스트 성숙도 모델 (TMMi) 
779. ISO/IEC/IEEE 29119 소프트웨어 테스팅 국제 표준 
780. 클라우드 보안 형상 관리 (CSPM) 데브옵스 결합 
781. 안티 디버깅 코드 난독화 리버스엔지니어링 차단 
782. 메모리 안전성 언어 (Rust) 컴파일러 검증 차용 
783. 서버 사이드 렌더링(SSR) 하이드레이션(Hydration) 
784. 웹 프로그레시브 서비스워커(Service Worker) 연계망 
785. 마이크로서비스 데이터 일관성 결과적 일관성 확보 
786. 분산 시스템 옵저버빌리티 Trace ID 상관관계 분석 
787. 애그리게이트 루트 외부 접근 단일 진입점 설계 
788. 헥사고날 아키텍처 어댑터 포트 매핑 구조 
789. 클린 아키텍처 엔티티 유스케이스 프레젠테이션 계층 분리 
790. 이벤트 버스 카프카(Kafka) 비동기 내결함성 설계 
791. 서비스 지향 아키텍처(SOA) ESB 성능 병목 한계 
792. API 게이트웨이 인증 및 라우팅 병목 관리망 
793. 인프라 코드 (IaC) 멱등성 보장 템플릿 기술 
794. 지속적 배포 롤백 자동화 정책 파이프라인 구성 
795. 린 개발 7원칙 낭비 제거 전체 최적화 배포망 
796. 스크럼 스프린트 회고(Retrospective) 개선 액션 도출 
797. XP 실천 방법 TDD 페어 지속 통합 코드 공동 소유 
798. 형상 통제 베이스라인 변경 심의 이력 추적 
799. COCOMO 비용 산정 모드 (Organic, Semi, Embedded) 
800. 소프트웨어 공학 기술사 10개년 기출 핵심 융합 토픽 결론 정리 

---
**총합 요약 : 총 800개 핵심 키워드 수록**
(소프트웨어공학의 전통적 이론부터 객체지향/아키텍처/테스트를 거쳐, 최근 핫트렌드인 애자일, DevOps, 클라우드 네이티브(MSA), AI 코드생성, 시큐어 코딩까지 정보관리기술사 수준의 방대한 지식 체계를 800개의 키워드로 집대성하였습니다.)
