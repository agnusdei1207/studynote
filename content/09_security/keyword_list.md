---
title: "Keyword List"
date: "2026-03-25"
tags:
  - "studynote-security"
weight: 50
---
# 정보보안 (Information Security) 키워드 목록

시스템 설계 심화 학습을 위한 보안 전 영역 실무자 수준 핵심 키워드
> ⚡ 실무자 보안 문제는 단순 지식이 아닌 <strong>위협 모델링 -> 아키텍처 설계 -> 법적·제도적 대응</strong>까지 통합 서술을 요구함

---

## 1. 정보보안 개론 / 원칙 — 67개

1. 정보보안 3요소 — CIA (기밀성·무결성·가용성)
2. 기밀성 (Confidentiality) — 암호화, 접근 제어, DRM, 분류
3. 무결성 (Integrity) — 해시, 전자서명, MAC, HMAC, 체크섬
4. 가용성 (Availability) — HA 설계, RAID, 부하 분산, DDoS 방어, SLA
5. 인증성 (Authenticity) — 신원 확인, PKI, 디지털 서명, 메시지 인증
6. 부인방지 (Non-repudiation) — 전자서명, 타임스탬프, 로그, 감사 추적
7. 책임추적성 (Accountability) — 감사 로그, 감사 기록, 사용자 행동 추적
8. 개인정보보호 3요소 — 기밀성·무결성·접근성 (ISO 27701)
9. 정보보안 6요소 — CIA + 인증성 + 부인방지 + 책임추적성
10. 최소 권한 원칙 (Principle of Least Privilege) — 필요 알 권리
11. 직무 분리 원칙 (Separation of Duties) — 4눈 원칙, 분산 통제
12. 다단계 인증 원칙 (Defense in Depth) — 심층 방어
13. 알 필요성 원칙 (Need-to-Know) — 정보 접근 제한
14. 단순 보안 원칙 (Simplicity) — 불필요한 복잡성 제거
15. 공개 설계 원칙 (Open Design) — 키 은닉，이비 알고리즘 은닉
16. 실패 안전 원칙 (Fail-Safe) — 기본값 거부, 오류 시 안전 상태
17. 완전한 중재 원칙 (Complete Mediation) — 모든 접근 경로 검사
18. 경제적 설계 원칙 (Economy of Mechanism) — 최소 구현
19. 완전한 통제 원칙 (Open Platform for Security) — 분리 보호
20. Least Common Mechanism — 메커니즘 공유 최소화
21. 심리적 사용성 원칙 (Psychological Acceptability) — 보안이 사용성을 해치면 안 됨
22. 정보보안 정책 — 최고 경영진 승인, 문서화된 규칙
23. 정보보안 표준 — 정책실시 위한 구체적 기준
24. 정보보안 지침 — 표준 적용 방법론
25. 정보보안 절차 — 구체적 작업 지침
26. 위험 관리 프로세스 — 식별/분석/평가/대응/모니터링/보고
27. 위험 식별 (Risk Identification) — 자산·위협·취약점 목록화
28. 정량적 위험 분석 — ALE = ARO × SLE, MTBF, MTTF, MTTR
29. 정성적 위험 분석 — High/Medium/Low 매트릭스
30. SLE (Single Loss Expectancy) — 단일 사고 예상 손실
31. ARO (Annual Rate of Occurrence) — 연간 발생 확률
32. ALE (Annual Loss Expectancy) — 연간 예상 손실
33. 위험 대응 전략 4가지 — 회피/전가/완화/수용
34. 위험 회피 (Risk Avoidance) — 위험 원천 제거
35. 위험 전가 (Risk Transfer) — 보험, 외주, 계약 조항
36. 위험 완화 (Risk Mitigation) — 통제조시 도입으로 위험 감소
37. 위험 수용 (Risk Acceptance) —관리층 승인 하에
38. 잔여 위험 (Residual Risk) — 통제 후 남은 위험
39. 검출 위험 (Detected Risk) vs 미검출 위험 (Undetected Risk)
40. inherited Risk — 상속된 위험
41. 보안 아키텍처 — Zachman Framework (6×6 매트릭스)
42. SABSA (Sherwood Applied Business Security Architecture) — 수평×수직 매트릭스
43. OSA (Open Security Architecture) — 보안 아키텍처 패턴 카탈로그
44. TOGAF (The Open Group Architecture Framework) — 아키텍처 개발 방법론
45. NIST CSF 2.0 — Identify/Protect/Detect/Respond/Recover + Govern
46. 제로 트러스트 (Zero Trust) — "Never Trust, Always Verify", NIST SP 800-207
47. ZTA (Zero Trust Architecture) — NIST 4단계 구현 로드맵
48. SDP (Software Defined Perimeter) —적연건 정의 경계
49. 마이크로 세그멘테이션 — 워크로드별 격리, 측면 이동 차단
50. East-West 트래픽 통제 — 내부 세그멘테이션
51. North-South 트래픽 통제 — 경계 방어
52. 보안 통제 3가지 유형 — 관리적/기술적/물리적
53. 예방 통제 (Preventive Controls) — 사전 차단
54. 탐지 통제 (Detective Controls) — 이상 징후 발견
55. 교정 통제 (Corrective Controls) — 사고 후 복구
56. 억제 통제 (Deterrent Controls) — 위협 행동 억제
57. 상실 통제 (Compensating Controls) — 기존 통제 우회 조치
58. 내재적 보안 (Security by Design) — 설계 단계 보안 고려
59. 사후 보안 (Bolt-on Security) — 완성 후 보안 추가
60. Privacy by Design 7기본원칙 — 사전 보호, 기본값사밀성 등
61. Secure by Default — 기본적으로 안전한 기본값
62. Secure Coding — 안전한 소프트웨어 개발
63. Threat Modeling — STRIDE, DREAD, MITRE ATT&CK 맵핑
64. DREAD 모델 — Damage/Reproducibility/Exploitability/Affected Users discoverability
65. STRIDE 모델 — Spoofing/Tampering/Repudiation/Information Disclosure/DoS/Elevation
66. PASTA (Process for Attack Simulation and Threat Analysis) — 7단계 위협 모델링
67. Attack Surface Analysis — 공격 표면 관리

---

## 2. 암호학 기초 — 42개

68. 암호학 (Cryptography) — 기밀성·무결성·인증·부인방지 제공
69. 고전 암호 — 치환 암호, 전치 암호
70. 개살 암호 (Caesar Cipher) — 알파벳 3자리 이동
71. 단일 치환 암호 — 하나의 알파벳을 하나의 문자로 치환
72. 다중 치환 암호 (Vigenère Cipher) — 키워드 기반 복수 치환
73. Enigma — 독일 제2차 세계대전 기계식 암호
74. 일다음성밀마본 (One-Time Pad) — 정보 이론적으로 완벽한 안전성
75. 현대 암호학 기본 가정 — computationally infeasible
76. 대칭키 암호 (Symmetric Encryption) — 동일한 키로 암호화/복호화
77. 비대칭키 암호 (Asymmetric Encryption) — 공개키/비밀키 쌍
78. 하이브리드 암호 — 대칭+비대칭 결합 (키 교환+데이터 암호화)
79. 블록 암호 (Block Cipher) — 고정 크기 블록 단위 암호화
80. 스트림 암호 (Stream Cipher) — 비트/바이트 단위 실시간 암호화
81. RC4 — 스트림 암호, 취약점 발견으로 사용 중단 (WEP)
82. Salsa20/ChaCha20 — ARX 기반 스트림 암호, TLS 1.3
83. AES (Advanced Encryption Standard) — 128/192/256비트 키
84. AES SPN 구조 — SubBytes/ShiftRows/MixColumns/AddRoundKey
85. AES 키 스케줄 — 라운드 키 생성
86. DES (Data Encryption Standard) — 56비트 키, 취약
87. 3DES (Triple DES) — 168비트 (112비트 실효 강도)
88. 블록 암호 모드 — ECB/CBC/CFB/OFB/CTR
89. CBC (Cipher Block Chaining) — 초기화 벡터(IV) 필요, 체인 의존성
90. CTR (Counter) — 난수 대신 카운터, 병렬 처리 가능
91. GCM (Galois/Counter Mode) — AEAD, 인증 암호화
92. AEAD (Authenticated Encryption with Associated Data) — 암호화+인증 동시
93. CCA (Chosen Ciphertext Attack) — 암호문 공격 분류
94. CPA (Chosen Plaintext Attack) — 평문 공격 분류
95. IND-CPA (Indistinguishability under CPA) — 암호학적 안전성 정의
96. IND-CCA2 — 강인한 암호학적 안전성
97. 해시 함수 — 단방향성, 충돌 저항성, Preimage 저항성
98. MD5 — 128비트 해시, 충돌 공격 실용화 (1996)
99. SHA-1 — 160비트, SHA-1 충돌 발견 (2017, SHAttered)
100. SHA-2 — SHA-224/256/384/512, 현재 표준
101. SHA-3 (Keccak) — sponge construction, NIST 2015
102. BLAKE2/BLAKE3 — 채택성능 해시, AES 대체
103. HMAC (Hash-based Message Authentication Code) — 키섬입 해시
104. NMAC (Nested MAC)
105. CMAC (Cipher-based MAC) — 블록 암호 기반
106. GMAC (Galois MAC) — GCM의 인증 부분
107. rainbow table — 사전 계산 해시 테이블, 역산 공격
108. salt — 해시 충돌 방지를 위한 난수 추가
109. 키 스트레칭 — PBKDF2, bcrypt, scrypt (메모리 하드)

---

## 3. 암호학 심화 / PKI — 52개

110. RSA — 소인수분해 문제 기반, 1977년 Rivest/Shamir/Adleman
111. RSA 키 생성 — 두 소수의 곱, 오일러 파이 함수
112. RSA-OAEP — 최적 asymmetric encryption padding, CCA2 안전성
113. RSA-PSS — 확률적 서명 방식, safe 서명
114. modulo 연산 — RSA 핵심인 나머지 연산
115. Carmichael 수 — RSA 안전성 분석 관련
116. GCD (최대공약수) — RSA 키 생성에서 사용
117. 확장 유클리드 알고리즘 — 모듈로 역수 계산
118. CRT (Chinese Remainder Theorem) — RSA 복호화 최적화
119. ECC (Elliptic Curve Cryptography) — 타원곡선 이산 로그 문제
120. 타원곡선 — y^ = x³ + ax + b 꼴의 곡선
121. ECDLP (Elliptic Curve Discrete Log Problem) — ECC 안전성 기반
122. secp256k1 — Bitcoin에서 사용되는 곡선
123. P-256 (secp256r1) — NIST 권장 곡선
124. P-384 / P-521 — NIST 고강도 곡선
125. ECDSA (Elliptic Curve DSA) — ECC 기반 디지털 서명
126. EdDSA / Ed25519 — Edwards 곡선, 결정론적 서명
127. X25519 — ECDH를 Edwards 곡선에서 구현
128. DH (Diffie-Hellman) — 이산 로그 기반 키 교환
129. DHE (Ephemeral DH) — 임시 DH, 전방 비밀성(PFS) 제공
130. ECDH — ECC 기반 효율적 키 교환
131. ECDHE — Ephemeral ECDH, TLS 1.3 기본
132. 키교환 프로토콜 — 중간자 공격 방지를 위한 상호 인증
133. Hybrid Encryption — KEM/DEM 분리 구조 (ISO 18033-2)
134. KEM (Key Encapsulation Mechanism) — 키 포장
135. DEM (Data Encapsulation Mechanism) — 데이터 암호화
136. HKDF (HMAC-based Key Derivation Function) — RFC 5869
137. TLS 1.3 핸드셰이크 — 1-RTT, 0-RTT, PSK
138. AEAD 요구 — TLS 1.3은 AEAD 암호만 허용
139. 전방 비밀성 (PFS) — 과거 세션 키 유출해도 과거 통신 보호
140. 세션 키 — 임시 세션용단기밀월
141. 마스터 시크릿 — Pre-Master Secret에서 파생
142. PSK (Pre-Shared Key) — 사전 공유 키
143. Diffie-Hellman Gruppen — RFC 3526 소수 그룹
144. 키 파생 함수 — TLS 1.3의 HKDF-Extract/Expand
145. NIST PQC 표준화 — 2016년 시작, 2024년 4개 알고리즘 선정
146. CRYSTALS-Kyber — 격자 기반 KEM, NIST PQC 표준
147. CRYSTALS-Dilithium — 격자 기반 디지털 서명, NIST PQC
148. FALCON — 격자 기반 서명, 짧은 서명
149. SPHINCS+ — 해시 기반 서명, 양자 내성
150. BIKE / HQC / Classic McEliece — 코드 기반 PQC
151. 양자 컴퓨팅 위협 — Shor 알고리즘 (RSA/ECC 깨뜨림), Grover (AES 128->64)
152. "Harvest Now, Decrypt Later" — 양자 위협 대응 전략
153. .crypto agility — 알고리즘 교체 능력, PQC 이전 준비
154. 키 관리 생명주기 — 생성/분배/저장/사용/순환/폐기
155. 키 폐기 — 안전한 삭제, 키 재료 완전 소멸
156. 키 순환 — 정기적 키 교체, 유출 시 복구력
157. HSM (Hardware Security Module) — 물리적 키 보호
158. TPM (Trusted Platform Module) — 플랫폼 키 저장, 원격 증명
159. PKI (Public Key Infrastructure) — 공개키 인증서 체계
160. CA (Certification Authority) — 인증서 발급/관리
161. RA (Registration Authority) — 인증 요청 검증/승인

---

## 4. PKI 심화 / 인증 프로토콜 — 49개

162. CRL (Certificate Revocation List) — 폐지 인증서 목록
163. OCSP (Online Certificate Status Protocol) — 실시간 인증서 상태 질의
164. OCSP 스테이플링 — 서버가 OCSP 응답 사전 가져옴
165. CT (Certificate Transparency) — 인증서 발급 공개 로그
166. CT 로그 서버 — Google/Rustproof 등 다수 운영
167. SCT (Signed Certificate Timestamp) — CT 증명
168. CAA (Certification Authority Authorization) — 허용된 CA DNS 레코드
169. PKCS#10 — 인증서 서명 요청 (CSR) 형식
170. PKCS#7 / CMS — 인증서 envelope 형식
171. PKCS#12 — 인증서+개인키 보관 형식 (.pfx)
172. DER / PEM 인코딩 — 인증서 인코딩 형식
173. X.509 v3 인증서 — Subject/Issuer/SAN/Key Usage/NSC
174. SAN (Subject Alternative Name) — 다중 도메인 인증서
175. 와일드카드 인증서 — *.example.com
176. EV (Extended Validation) 인증서 — 엄격한 검증, 녹색 주소창
177. DV (Domain Validation) 인증서 — 도메인 검증만
178. OV (Organization Validation) — 조직 검증
179. Self-signed 인증서 — 자체 발급 인증서, 내부용
180. 인증서 체인 검증 — Root CA -> Intermediate CA -> End Entity
181. 브릿지 CA (Bridge CA) — 교차 인증
182. 인증서 핀닝 —이지 인증서 목록 하드코딩
183. HPKP (HTTP Public Key Pinning) — deprecated, 동적 핀닝 권장
184. Certificate Patrol / Security/Telemetry — Firefox 브라우저 핀닝
185. 동적 핀닝 — CT 로그 기반pins
186. Stapling of OCSP Response — TLS 핸드셰이크 최적화
187. mTLS (Mutual TLS) — 서버+클라이언트 상호 인증
188. Code Signing — 소프트웨어 원산지 인증
189. Authenticode — Microsoft 코드 서명
190. Apple Developer ID — macOS/iOS 앱 서명
191. 서명 타임스탬프 —TSA (Time Stamping Authority)
192. TSA (Time Stamping Authority) — RFC 3161, 부인방지
193. CRL Distribution Point — CRL 발급 위치
194. Authority Information Access — OCSP 응답자 위치
195. CRL Scope — 전체/crlNumber 용도
196. delta CRL —증량 CRL, 효율성 향상
197. LDH (Limited Distribution Hypothesis) — 인증서 배포 모델
198. Key Usage 확장 — digitalSignature/keyEncipherment/codeSigning
199. Extended Key Usage — serverAuth/clientAuth/codeSigning/emailProtection
200. nameConstraints — CA가 발급 가능한 이름 공간 제한
201. Basic Constraints — CA 여부, 경로 길이 제한
202. 정책 매핑 — 상위 CA 정책과 하위 CA 정책 매핑
203. SPC (Signed Public Key Challenge) — 코드 서명 blob
204. Authenticode Timestamp Protocol — RFC 3161 호환
205. Kernel Mode Signing — Windows 커널 드라이버 필수
206. UEFI Secure Boot — 부팅 과정 코드 서명 검증
207. DKIM (DomainKeys Identified Mail) — 이메일 발신자 인증
208. SPF (Sender Policy Framework) — 허용된 발신 서버 목록 (DNS TXT)
209. DMARC (Domain-based Message Auth Reporting) — SPF+DKIM 정책
210. DANE (DNS-Based Auth of Named Entities) — TLSA 레코드, 인증서 고정

---

## 5. 네트워크 보안 — 55개

211. 네트워크 보안 3대 영역 — 경계/세그멘테이션/무결성
212. 방화벽 — 네트워크 경계 접근 제어
213. 패킷 필터링 방화벽 — 3-4층 헤더 기반 필터
214. 상태 검사 방화벽 (Stateful Inspection) — 연결 상태 추적
215. 애플리케이션 게이트웨이 (Proxy) — 7층 프로토콜 검사
216. NGFW (Next-Generation Firewall) — DPI, 사용자식별, 앱식별
217. 방화벽 토폴로지 — 스크린 서브넷, 이중 DMZ
218. bastion host — 경계 호스트, 공개 서비스 전용
219. DMZ (Demilitarized Zone) — 비 Military Zone, 공개 구간
220. 내부 방화벽 (Internal Firewall) — 내부 세그멘테이션
221. East-West 트래픽 — 수평 방향 통신, 내부 위협 통제
222. North-South 트래픽 — 경계 통과 통신
223. 네트워크 세그멘테이션 — VLAN, VRF, 논리적 격리
224. VLAN (Virtual LAN) — 브로드캐스트 도메인 분리
225. VRF (Virtual Routing and Forwarding) — 경로 격리
226. NAC (Network Access Control) — IEEE 802.1X, 포트 기반 접근 제어
227. EAP (Extensible Authentication Protocol) — 802.1X 인증 프로토콜
228. EAP-MD5 — 취약, 권장되지 않음
229. PEAP (Protected EAP) — TLS수도보호 EAP
230. EAP-TLS — 인증서 기반 상호 인증
231. MAC Address Filtering — 허가된 MAC만 허용
232. IDS (Intrusion Detection System) — 오용 탐지/이상 탐지
233. IDS 배치 — in-band (IDS) vs out-of-band (tap/mirror)
234. IPS (Intrusion Prevention System) — 인라인 배치, 자동 차단
235. Signature-based detection —이지 공격 패턴 매칭
236. Anomaly-based detection —정상 프로파일과 비교
237. HIDS/HIPS — 호스트 기반 IDS/IPS
238. NIDS/NIPS — 네트워크 기반 IDS/IPS
239. Snort — 오픈소스 NIDS
240. Suricata — 멀티스레드 NIDS
241. Zeek (formerly Bro) — 네트워크 트래픽 분석
242. WAF (Web Application Firewall) — HTTP/HTTPS 보호
243. OWASP Core Rule Set — WAF 규칙 세트
244. Virtual Patching — 실제 패치 전 WAF로 취약점 우회
245. ModSecurity — 오픈소스 WAF 엔진
246. API Gateway — API 접근 제어,_RATE limiting, 인증
247. API Gateway 기능 — 인증/인가/캐싱/로깅/변환
248. DDoS 공격 — 고의적 서비스 중단 공격
249. DDoS 3유형 — 볼류메트릭/프로토콜/애플리케이션 계층
250. DDoS 방어 기법 — Rate Limiting, Anycast, Scrubbing Center
251. BGP Blackhole — DDoS 트래픽 경로흑동
252. DNS Amplification — DNS 쿼리 증폭 공격
253. NTP Amplification — NTP 모노리스트 상태 쿼리 증폭
254. memcached Amplification — UDP 포트 11211 활용
255. SYN Flood — TCP 반개 연결 점유
256. UDP Flood — 비효율적 프로토콜람용
257. HTTP Flood — application layer DDoS
258. Slowloris — HTTP 헤더 미완성 전송으로 연결 점유
259. IP Spoofing — 출발지 IP 위조, BCP38 필수
260. uRPF (Unicast Reverse Path Forwarding) — Spoofing 방지
261. ARP Spoofing — MAC 주소 위조, 스위칭 환경에서도 가능
262. Gratuitous ARP — 정상 ARP 응답 위조, MiTM 사전 준비
263. DHCP Spoofing — DHCP 서버 역할 사칭
264. DNS Spoofing — DNS 응답 캐시 오염
265. DNS Cache Poisoning — Kaminsky 공격, 검증 없는 응답

---

## 6. 네트워크 보안 심화 — 55개

266. MITM (Man-in-the-Middle) 공격 — 통신 경로 가로채기
267. SSL Stripping — HTTPS->HTTP 강제 다운그레이드
268. HSTS (HTTP Strict Transport Security) — HTTPS 강제 사용
269. HTTP Public Key Pinning — deprecated (2018)
270. Cookie Hijacking — 세션 쿠키 탈취
271. 세션 하이재킹 — TCP 시퀀스 넘버 예측
272. 패킷 스니핑 — 프로미스큐어스 모드 네트워크 인터페이스
273. 세션 고정 공격 (Session Fixation) — 공격자 세션 ID 강제 설정
274. Replay Attack — 통신 도청 후 재전송
275. IPsec — 네트워크층 투명한 보안
276. IPsec 두 가지 프로토콜 — AH (인증만)/ESP (암호화+인증)
277. IPsec 모드 — Transport 모드/Tunnel 모드
278. IKE (Internet Key Exchange) — 키 교환 프로토콜
279. IKEv1 Phase 1/2 — Main Mode/Aggressive Mode
280. IKEv2 — MOBIKE 지원, NAT-T 자동 처리
281. NAT-T (NAT Traversal) — IPsec VPN NAT 통과
282. L2TP/IPsec — L2TP 터널 + IPsec 암호화
283. SSL VPN — 브라우저 기반/클라이언트 설치형
284. OpenVPN — 오픈소스 SSL VPN
285. WireGuard — modern VPN, Linux 커널에 통합
286. ZeroTier — 분산 VPN, P2P 터널
287. Tailscale — WireGuard 기반 관리형 VPN
288. SASE (Secure Access Service Edge) — 네트워크+보안 통합
289. SSE (Security Service Edge) — SASE의 보안 요소
290. SD-WAN (Software-Defined WAN) — WAN 가상화
291. SD-WAN 보안 — 암호화된 터널, 중앙 집중식 정책
292. VPN concentrator — 다수 VPN 연결 집약 장치
293. TLS/SSL 취약점 역사 — POODLE/BEAST/CRIME/ROGUE
294. POODLE (Padding Oracle On Downgraded Legacy Encryption)
295. BEAST (Browser Exploit Against SSL/TLS)
296. CRIME — TLS 압축 사이드 채널 공격
297. HEARTBLEED — OpenSSL 하트비트 확장 메모리 유출
298. DROWN — SSLv2람용에よる RSA 해독
299. Logjam — DH_EXPORT 키 강제 사용, 512비트 그룹
300. FREAK — RSA_EXPORT 키 강제 사용
301. Sweet32 — 64비트 블록 암호 Birthday 공격
302. TLS 1.3 — 이전 버전과의 호환성 제거, 빠른 핸드셰이크
303. TLS 1.3 vs 1.2 차이 — 1-RTT 핸드셰이크, 0-RTT, PFS 의무
304. TLS 밀마투건 — TLS_AES_256_GCM_SHA384 등
305. cipher suite명명규칙 — TLS_kex_AUTH
306. Perfect Forward Secrecy — 각 세션독립적밀월
307. SSH (Secure Shell) — 안전한 원격 접속
308. SSH 키 기반 인증 — 공개키/개인키 쌍
309. SSH Agent Forwarding — 로컬 에이전트를원정에 전달
310. SFTP — SSH 기반 파일 전송
311. SCP — SSH 기반 파일 복사
312. SSH Tunnel/Proxy — SOCKS 프록시
313. Known Hosts — 서버 공개키 최초 수락/저장
314. SSH 옵션 강화 — PasswordAuthentication no, PubkeyAuthentication yes
315. LDAP — 디렉터리 서비스 접근 프로토콜
316. LDAPS (LDAP over SSL) — 포트 636, LDAP 암호화
317. LDAP 인젝션 — 특수 문자주입으로 인증 우회
318. ARP 캐시poisoning —정태 ARP 설정으로 MiTM
319. VLAN Hopping — Switch Spoofing/Double Tagging
320. Bridge Protocol Data Unit (BPDU) — 스위치 프로토콜

---

## 7. 시스템 보안 / 엔드포인트 — 55개

321. 엔드포인트 보안 — 단말기에 대한 보안조시
322. EPP (Endpoint Protection Platform) — 통합 엔드포인트 보호
323. AV (Anti-Virus) — 시그니처 기반 악성코드 탐지
324. 행위 기반 탐지 — 시그니처 없이 의심 행동 감지
325. EDR (Endpoint Detection and Response) — 실시간 모니터링+응답
326. XDR (Extended Detection and Response) — 멀티 플랫폼 상관 분석
327. MDR (Managed Detection and Response) — 관리형 탐지/응답
328. 엔드포인트 보호 조합 — AV+EDR+NDR+UEBA
329. TTP (Tactics, Techniques, Procedures) — 공격자 행동 패턴
330. 버퍼 오버플로우 (Buffer Overflow) — 메모리 경계 초과
331. 스택 버퍼 오버플로우 — 함수 복귀 주소 덮어쓰기
332. 힙 버퍼 오버플로우 — 힙 메모리 오염
333. 정수 오버플로우 (Integer Overflow) — 정수 범위 초과
334. Format String Bug — %x, %s 등 포맷 지시어 악용
335. NX bit (No-Execute) — 실행 가능 메모리 영역 분리
336. DEP (Data Execution Prevention) — NX를 OS 수준에서 구현
337. ASLR (Address Space Layout Randomization) — 주소 공간 난수화
338. PIE (Position Independent Executable) — EXE도 ASLR
339. Stack Canary — 스택 프레임 손상 탐지 쿠키
340. SSP (Stack Smashing Protector) — GCC의 스택 보호
341. RELRO (Relocation Read-Only) — GOT 쓰기 보호
342. Full RELRO — GOT 전체 읽기 전용
343. FORTIFY_SOURCE — _chk 함수로 버퍼 연산 대체
344. ROP (Return-Oriented Programming) — 가젯 체인, 셸코드 없이 코드 실행
345. 가젯 (Gadget) — Ret 명령으로 끝나는 코드 조각
346. JOP (Jump-Oriented Programming) — 함수 포인터Hijacking
347. COP (Call-Oriented Programming) — 호출 기반 가젯 체인
348. Return-to-libc — libc 함수 직접 호출
349. Heap Spray — 힙 메모리에 셸코드 대량 배치
350. Heap Feng Shui — 힙 레이아웃 조작
351. Use-After-Free — 해제된 메모리 재사용
352. Double Free — 이중 해제로 힙 손상
353. Race Condition — TOCTOU (Time-of-Check-Time-of-Use)
354. Deadlock / Livelock — 자원 점유로 인한 교착/기아
355. Time-of-Check to Time-of-Use — 파일 접근 races
356. 권한 상승 — Local Privilege Escalation (LPE)
357. 커널 privilege escalation — Dirty COW, EternalBlue
358. Zero-Day — 패치되지 않은 취약점 리용
359. 루트킷 (Rootkit) — 시스템에잠복하는 악성 코드 모음
360. 커널 루트킷 — OS 커널 레벨 설치
361. 사용자모드 루트킷 — 애플리케이션 레벨
362. 부트킷 (Bootkit) — 부팅 과정infecting
363. MBR Bootkit — Master Boot Record 감염
364. UEFI Bootkit — UEFI 펌웨어 수준 감염
365. Secure Boot 우회 — 서명 검증 무력화
366. Firmware Rootkit — BIOS/펌웨어 숨겨진 백도어
367. 키로거 (Keylogger) — 키입력 기록
368. 백도어 (Backdoor) — 정상 인증 우회
369. 논리작탄 (Logic Bomb) — 특정 조건 충족 시 발동
370. 트로이목마 (Trojan Horse) — 겉보기에 정상인 악성코드
371. 랜섬웨어 (Ransomware) — 파일 암호화 후 몸값
372. CryptoLocker / WannaCry / Ryuk — 주요 랜섬웨어 변종
373. Wiper — 데이터 파괴 목적인 malware
374. 지능형 지속 위협 (APT) — 국가 수준 위협 행위자
375. Fileless Malware — 메모리 내에서만 실행, 파일 없는 공격

---

## 8. 시스템 보안 심화 — 40개

376. 커널 취약점 — 시스템 콜 인터페이스 악용
377. Spectre/Meltdown — CPU 취약점 (추측집행 악용)
378. Spectre v1/v2 — Bounds Check Bypass/Branch Target Injection
379. Meltdown — Rogue Data Cache Load
380. MDS (Microarchitectural Data Sampling) — CPU 내부 데이터 샘플링
381. ZombieLoad / RIDL — Load치적리스크
382. SWAPGS — GPU 취약점 악용
383. CPU 취약점완화 — 마이크로코드 업데이트, OS 패치
384. 펌웨어 보안 — UEFI Secure Boot
385. Measured Boot — TPM리용, boot 측정값 기록
386. Static PCR — 부팅 과정 무결성 측정
387. Dynamic PCR — late launch으로 동적 측정
388. Intel TXT (Trusted Execution Technology) — late launch
389. SGX (Software Guard Extensions) — enclave 메모리 보호
390. enclave — SGX의가밀 메모리 영역
391. AMD SEV (Secure Encrypted Virtualization) — VM 암호화
392. SEV-ES — VM 레지스터 state 암호화
393. Memory Encryption 엔진 — 하드웨어 메모리 암호화
394. TPM 2.0 — 키 저장, 플랫폼 증명
395. TPM 기능 — PCR, EK, NV Index, Attestation
396. remote attestation — 원격 플랫폼 증명
397. BitLocker — Windows FDE, TPM+N PIN/USB 사용
398. FileVault — macOS FDE
399. LUKS — Linux Unified Key Setup, 디스크 암호화
400. VeraCrypt — 오픈소스 암호화 도구
401. 전드라이브 암호화 (FDE) — OS 레벨 암호화
402. 필드 레벨 암호화 — DB 컬럼/필드별 암호화
403. TDE (Transparent Data Encryption) — DB 엔진 레벨 암호화
404. 백업 암호화 — 백업 데이터도 암호화 필수
405. Secure Erase — SSD trim + 암호화 키 삭제
406. 패치 관리 — CVSS 점수 기반 우선순위
407. CVSS (Common Vulnerability Scoring System) — 0~10점
408. CVSS 구성 — Base/Transient/Temporal/Global 벡터
409. CVE (Common Vulnerabilities and Exposures) — 취약점 등록 번호
410. CWE (Common Weakness Enumeration) — 취약점 유형 분류
411. CPE (Common Platform Enumeration) — 플랫폼 명칭
412. OVAL (Open Vulnerability and Assessment Language) — 취약점 검사 언어
413. 약구령측정 — 기본パスワード/사전공격
414. 시스템 강화 — Hardening, 불필요 서비스 제거
415. CIS Benchmarks — Center for Internet Security 강화 가이드

---

## 9. 웹 / 애플리케이션 보안 — 60개

416. OWASP Top 10 — 가장 위험한 웹 보안 취약점
417. A01. 취약한 접근 제어 — IDOR, 권한 없는 기능 접근
418. IDOR (Insecure Direct Object Reference) — 객체 참조Manipulation
419. 경로 순회 (Path Traversal) — ../../etc/passwd
420. 보편적 자원 순회 (Directory Traversal) — 경로 역추적
421. Local File Inclusion (LFI) —본지 파일 포함
422. Remote File Inclusion (RFI) — 원격 파일 포함
423. 접근 제어 회피 — 메소드 제한 우회, CORS Misconfiguration
424. A02. 암호화 실패 — 안전하지 않은 암호화 사용
425. 하드코딩 자격증명 — 소스코드 내 평문 비밀번호
426. 약한 TLS 버전 — TLS 1.0/1.1 사용
427. Certificate Pinning 우회 — Frida, Objection
428. A03. 인젝션 — 입력값 검증 부재로 인한 코드 실행
429. SQL 인젝션 — 데이터베이스 쿼리Manipulation
430. Error-based SQL Injection — 오류 메시지 통한 정보 탈취
431. Blind SQL Injection — 논리적 참/거짓 반응으로 정보 추출
432. Time-based Blind SQL Injection — SLEEP() 함수로 반응 지연
433. ORM Injection — 객체-관계 매핑 프레임워크 공격
434. NoSQL Injection — MongoDB 등 문서DB 공격
435. OS Command Injection — 서버 명령어 실행
436. LDAP Injection — LDAP 쿼리 조작
437. XPath Injection — XML 데이터 질의 조작
438. Expression Language Injection — Spring/Struts EL 공격
439. Template Injection (SSTI) — 서버 사이드 템플릿 엔진 공격
440. A04. 안전하지 않은 설계 — threat modeling 부재
441. 위협 모델링 부재 — 설계 단계 보안 평가 미실시
442. 안전하지 않은 기본값 — 기본 계정/비밀번호
443. 초과 기능 — 불필요한 기능 활성화
444. A05. 보안 설정 오류 — 잘못된 구성으로 인한 노출
445. 기본 계정 —엄상 제공 기본 비밀번호
446. 불필요 서비스 — 사용 안 하는 서비스 running
447. 오류 메시지 정보 유출 — 내부 경로/스택 트레이스
448. Missing Security Headers — 보안 헤더 미설정
449. Debug Mode — 개발용 모드 생산 환경 노출
450. CORS Misconfiguration — Access-Control-Allow-Origin: *
451. A06. 취약한 컴포넌트 — 알려진 취약점 포함 라이브러리
452. Log4Shell (CVE-2021-44228) — Log4j RCE
453. 서드파티 라이브러리 취약점 — npm/PyPI/RubyGems 의존성
454. A07. 인증 실패 — 부적절한 인증 메커니즘
455. 크리덴셜 스터핑 — 유출 계정 재사용
456. 브루트포스 — 무차별 대입 공격
457. 패스워드 스프레이 — 다양한 비밀번호 소량 시도
458. 크리덴셜 풀링 — 자격증명 목록 활용
459. 세션 ID 노출 — URL, 로그, Referer 헤더
460. 세션 고정 — 세션 ID 고정 공격
461. A08. 무결성 실패 — 소프트웨어 무결성 검증 부재
462. CI/CD 보안 — 파이프라인 침해, 의존성 오염
463. 의존성 오염 (Dependency Confusion) — 비공개 패키지 덮어쓰기
464. 잘못된 서명 검증 — 코드 서명 검증 우회
465. A09. 로깅/모니터링 실패 — 증거 미보존
466. Blindness — 공격 탐지 못 함
467. Logging Without Alert — 로그만 기록, 알림 없음
468. A10. SSRF — 서버 사이드 요청 위조
469. SSRF 메타데이터 — 169.254.169.254 등 cloud metadata
470. XSS (Cross-Site Scripting) —객호단 스크립트 삽입
471. 반사형 XSS — URL 파라미터 반영
472. 저장형 XSS — DB에 저장, 모든 사용자에게 발동
473. DOM-based XSS —객호단 JavaScript 변조
474. XSS 페이로드 — <script>alert(1)</script>, img onerror
475. CSP (Content Security Policy) — XSS 완화 헤더

---

## 10. 웹 보안 심화 / API 보안 — 50개

476. CSRF (Cross-Site Request Forgery) — 사용자의 의지와 무관한 요청
477. SameSite 쿠키 — CSRF 방어
478. CSRF Token — 난수 토큰 요구
479. 쌍중 Submit Cookie — 쿠키+파라미터 대조
480. Clickjacking — 투명 iframe 덮기
481. X-Frame-Options — frame embedding 차단
482. frame-ancestors — CSP 버전의 frame-ancestors
483. CORS Preflight — OPTIONS 요청으로 사전 검증
484. CORS 요청 흐름 — Origin 헤더 -> 서버 허용/거부
485. OWASP ZAP — 웹 취약점 스캐너
486. Burp Suite — 웹 프록시,삼투 테스트 도구
487. SQLMap — SQL 인젝션 자동화 도구
488. Nikto — 웹 서버 취약점 스캐너
489. httpoxy — CGI 환경변수 proxyManipulation
490. Host Header Injection — X-Forwarded-Host 검증 우회
491. Web Cache Deception — 캐시poisoning
492. Unicode Normalization — нормализация 차이 공격
493. NULL Byte Injection — %00로 확장자 우회
494. Null Byte Poisoning — 파일명 내 null 문자
495. OAS (OpenAPI Specification) — REST API 표준
496. GraphQL 인트로스펙션 — API 스키마 공개
497. GraphQL DoS — depth/alias 제한 없으면 무한 쿼리
498. REST API 보안 — Rate Limiting, JWT, HMAC
499. API Versioning — API 버전 관리와 보안
500. JWT (JSON Web Token) — stateless 인증
501. JWT 구조 — Header/Payload/Signature (JWS/JWE)
502. JWT alg: none — 취약점, alg 검증 필수
503. HS256 vs RS256 — 대칭/비대칭 서명
504. JWT 유출 — XSS로 토큰 탈취
505. Refresh Token — 액세스 토큰 재발급
506. OAuth 2.0 — 델리게이션 프로토콜
507. OAuth 2.0 4가지 Grant — Authorization Code/PKCE/Client Credentials/ROP
508. Authorization Code Grant —redirect_uri 기반
509. PKCE (Proof Key for Code Exchange) — public client 보안
510. Open Redirect — OAuth redirect_uri 우회
511. Token Leakage — URL 내 토큰 노출
512. Scope — OAuth 권한 범위
513. Access Token vs Refresh Token — 수명 차이
514. OIDC — OAuth 2.0지상적 신원 레이어
515. ID Token — OIDC의 사용자 신원 증명
516. ID Token vs Access Token — 용도 구분
517. Discovery Document — .well-known/openid-configuration
518. jwks_uri — JSON Web Key Set 엔드포인트
519. Nonce — replay attack 방지
520. Rate Limiting — 요청 수 제한으로 DoS 방지
521. WAF 규칙 — OWASP CRS 기반
522. ModSecurity Core Rule Set — generic 공격 탐지
523. HTTP Request Smuggling — front-end/back-end interpretation 차이
524. HTTP Request주사 — CL.TE, TE.CL, H2.CL
525. HTTP Response Smuggling — 응답 분할

---

## 11. 신원 관리 / 접근 제어 — 55개

526. IAM (Identity and Access Management) — 신원+접근 통합 관리
527. 신원 관리 — 사용자 lifecycle (프로비저닝/수정/비활성화/삭제)
528. Provisioning — 사용자 계정 자동 생성
529. Deprovisioning — 퇴직/이직 시 계정 즉시 삭제
530. Joiner/Mover/Leaver 프로세스 — 신원 lifecycle 관리
531. SSO (Single Sign-On) —일다음등록，다アプリ access
532. SAML 2.0 — XML 기반 SSO 프로토콜
533. SAML Assertion — 신원 정보 포함 XML
534. SAML Request/Response — SP-Initiated/IdP-Initiated
535. SP (Service Provider) — 서비스 제공자
536. IdP (Identity Provider) — 신원 제공자
537. OpenID Connect — OAuth 2.0 기반 SSO
538. OIDC Discovery — 자동 설정 메타데이터
539. Claims — OIDC의 사용자 속성
540. OIDC Scope (OpenID Connect Scope) — 요청하는 정보 범위 (openid/profile/email)
541. PKCE in OIDC — Authorization Code 보호
542. OAuth 2.0 vs OIDC — 델리게이션 vs 인증
543. Federation — 조직 간 신뢰 기반 ID 공유
544. Trust Relationship — federation 파트너 간 신뢰
545. eduGAIN — 학술 기관간 federation
546. Shibboleth — SAML 기반 federation
547. LDAP 기반 인증/조회 — 디렉터리 서비스 프로토콜
548. Active Directory — Microsoft 디렉터리 서비스
549. Azure AD / Microsoft Entra ID — 클라우드 신원
550. Azure AD Connect — 온프레미스 AD 클라우드 연동
551. Okta — SaaS IDaaS
552. MFA (Multi-Factor Authentication) — 다중 인증
553. 지식 요인 — 비밀번호, PIN
554. 소유 요인 — 토큰, 스마트폰, 스마트카드
555. 내재 요인 — 지문, 홍채, 음성, 얼굴
556. 위치 요인 — GPS, IP 기반 위치
557. 행동 요인 — 타이핑 패턴, 마우스 움직임
558. TOTP (Time-based OTP) — 30초마다 변경
559. HOTP (HMAC-based OTP) — 카운터 기반
560. Push Notification — 모바일 푸시 알림
561. FIDO2 / WebAuthn —공개키 암호 기반 인증
562. Passkey — FIDO2 기반, 플랫폼 관리
563. Passkey 장점 — 피싱 저항, 암호 불필요
564. PAM (Privileged Access Management) — 특권 계정 관리
565. 특권 계정 — 관리자,root, 서비스 계정
566. 세션 레코딩 — 특권 세션 녹화/감사
567. vault — 비밀번호 금고 (HashiCorp Vault)
568. Just-In-Time Access — 필요 시만 일시적 권한
569. RBAC (Role-Based Access Control) — 역할 기반 권한
570. RBAC 1/2/3 —.flat/hierarchical/constrained
571. 역할 계층 — 상위 역할이 하위 권한 상속
572. ABAC (Attribute-Based Access Control) — 속성 기반
573. 속성 종류 — subject/object/environment/action
574. XACML (eXtensible Access Control Markup Language) — ABAC 정책 언어
575. ReBAC (Relationship-Based Access Control) — 관계 기반
576. Zanzibar — Google의 권한 시스템
577. 최소 권한 원칙 — 필요한 최소 권한만 부여
578. 직무 분리 (SoD) —권한 분산으로 부정행위 방지
579. 어카운팅 — 접근 기록, 감사 자료
580. 접근 검토 (Access Review) — 정기적 권한 재검토

---

## 12. 신원 보안 심화 / 위협 — 40개

581. 인증 서버 — KDC, IdP, 인증 endpoints
582. Kerberos — 네트워크 인증 프로토콜 (v5)
583. KDC (Key Distribution Center) — AS+TGS 통합
584. AS (Authentication Server) — 초기 인증
585. TGS (Ticket Granting Server) — 티켓 발급
586. TGT (Ticket Granting Ticket) — 장기 티켓
587. ST (Service Ticket) — 특정 서비스용 단기 티켓
588. Kerberos 상호 인증 — client+server mutual
589. Silver Ticket — ST 위조 (서비스 계정 키 사용)
590. Golden Ticket — TGT 위조 (KRBTGT 키 사용)
591. Pass-the-Ticket — 메모리 내 티켓 재사용
592. Pass-the-Hash — NTLM 해시 재사용
593. Kerberos Bronze Attack — AS-REP Roasting
594. NTLM — Windows 네이티브 인증 프로토콜
595. NTLM Hash — MD4(UTF-16LE(password))
596. NTLM Authentication — 3-way handshake (질순/응답)
597. LM Hash — DES 기반, 취약한 레거시
598. NTLMv2 — HMAC-MD5 기반 강화 버전
599. NetNTLM — 네트워크 상에서만 사용되는 NTLM
600. MS-CHAPv2 — PPP/EAP 내부의 NTLM 변형
601. Credential Dumping — LSASS 메모리/ SAM hive 추출
602. Mimikatz — 크리덴셜 추출 도구
603. WDigest — 평문 비밀번호 캐싱 (레지스트리 설정)
604. SSP (Security Support Provider) — 인증 공급자 DLL
605. Golden/Silver Ticket mitigation — KRBTGT 비밀번호 주월적 교체
606. Protected Users 그룹 — Kerberos 전용 인증
607. Smart Card — 인증서 기반 MFA
608. PKINIT — Kerberos에서 공개키 인증 사용
609. Remote Desktop Gateway — RDG, HTTPS 기반 원격접속
610. Azure AD조건부 액세스 — 정책 기반 접근 제어
611. 조건부 액세스 신호 — 사용자/위험/디바이스/위치
612. Identity Protection — Azure AD ID 보호
613. UEBA (User Entity Behavior Analytics) — 행동 기반 이상 탐지
614. 애드혹 identity — 임시/외부 사용자 관리
615. Federated Identity — SAML/OIDC 기반 연합
616. Identity Bridge — AD FS, Azure AD Connect Federation
617. SCIM 2.0 — 자동 사용자 프로비저닝 프로토콜
618. JIT 프로비저닝 — Just-In-Time, On-Demand 프로비저닝
619. ID Governance — 권한 인증, 합성성 검토
620. Privileged Identity Management (PIM) —Azure 특권 ID 관리

---

## 13. 보안 운영 (SecOps) — 60개

621. SOC (Security Operations Center) — 보안 관제 조직
622. SOC 티어 — 티어 1(alert 분석)/2( approfondita조사)/3( threat hunting)
623. NOC (Network Operations Center) — 네트워크 모니터링
624. SIEM (Security Information and Event Management) — 로그 집적/상관 분석
625. SIEM 구성 — 수집(Curator)/저장(Repository)/분석(Analyzer)/가시화(Dashboard)
626. 로그 수집 — syslog, Windows Event Log, NetFlow, PCAP
627. Normalizzazione — 다양 로그 형식 정규화
628. 상관 분석 (Correlation) — 이벤트 간 관계 탐지
629. UEBA in SIEM — 행동 분석 기반 이상 탐지
630. Splunk — Enterprise SIEM
631. Elastic SIEM — Elasticsearch 기반
632. QRadar — IBM SIEM
633. ArcSight — HPE/Micro Focus SIEM
634. Graylog — 오픈소스 SIEM
635. Wazuh — 오픈소스 SIEM/EDR
636. SOAR (Security Orchestration, Automation, Response) — 자동화 대응
637. 플레이북 — 시나리오별 자동 대응 절차
638. 보안 자동화 — 반복 작업 자동화
639. Threat Intelligence — 위협 정보 공유
640. TI 4가지 유형 — 전략/전술/운영/기술적
641. STIX/TAXII — 위협 정보 교환 표준
642. MITRE ATT&CK — 공격자 전술/기법/절차DB
643. ATT&CK Matrix — Pre-ATT&CK/Enterprise/Mobile
644. Sub-techniques — 세분화된 공격 기법
645. Cyber Kill Chain — Lockheed Martin 7단계
646. UNC/APT 그룹 — APT 집합 명칭 (MITRE)
647. Diamond Model — 공격 분석 4요소 모델
648. Pyramid of Pain — 위협 Inteligence 가치 계층
649. OSINT (Open Source Intelligence) — 공개 출처 위협 정보
650. CVE/CVSS — 취약점 점수 체계
651. NVD (National Vulnerability Database) — NIST CVE DB
652. 인시던트 대응 (IR) — NIST 6단계
653. IR 단계 — 준비/식별/억제/근절/복구/교훈
654. IR 준비 — 대응 계획, 팀 구성, 교육
655. 식별 — 모니터링/알람->초보 분석
656. 억제 (Containment) — 단기(isolation)/장기(정상운영 복귀)
657. 근절 (Eradication) — 감염 원인 제거
658. 복구 — 시스템 정상화, 운영 재개
659. 교훈 (Lessons Learned) — 후속 조치, 보고서 작성
660. tabletop exercise —탁상연습, 시나리오 기반 연습
661. DFIR (Digital Forensics and Incident Response) — 디지털 포렌식+IR
662. 포렌식 4원칙 — 순수성/재현성/검증/객관성
663. 증거 보전 —write blocker, integrity hashing
664. Chain of Custody — 증거 이동/처리 기록
665. 메모리 포렌식 — Volatility, Rekall
666. RAM Dump — 물리 메모리 덤프
667. 페이지 파일 분석 — pagefile.sys, hiberfil.sys
668. 네트워크 포렌식 — PCAP, NetFlow, DNS 로그
669. 로그 보전 — syslog, Windows Event, Firewall 로그
670. 타임라인 분석 — 이벤트 시간순 재구성
671. MFT 분석 — Windows NTFS 메타데이터
672. 레지스트리 분석 — NTUSER.DAT, SAM, SECURITY hive
673. 스텔스 기법 — anti-forensics, 로그 삭제
674. anti-forensics — 증거 인멸/변조 기술
675. 취약점 スキャン — Nessus, OpenVAS, Qualys
676. 침투 테스트 — 합법적 해킹 시뮬레이션
677. PTES — Penetration Testing Execution Standard
678. OWASP Testing Guide — 웹 앱 테스트 가이드
679. OSSTMM — 보안 테스트 방법론
680. 버그 바운티 — 공개 취약점 보상 프로그램

---

## 14. 보안 운영 심화 / 위협 헌팅 — 40개

681. 레드팀 — 적대적 관점, 실제 공격 시뮬레이션
682. 블루팀 — 방어 관점, 탐지/대응
683. 퍼플팀 — 레드+블루 협력
684. White Team — 시나리오 관리/심사
685. 적대적 시뮬레이션 — Red Team vs Purple Team exercises
686. 가정 침투 (Assumed Breach) — 내부 접근 가정
687. BAS (Breach and Attack Simulation) — 자동화된 공격 시뮬레이션
688. Purple Team — 공격/방어 협력, 탐지 규칙 개선
689. 위협 헌팅 (Threat Hunting) — 가설 기반 선제적 탐색
690. Huntington 가설 — "공격자는 이미 내부에 있다"
691. Hunting Loop —가설/탐색/발견/정보 공유
692. MITRE Engage — 방어적 사이버 전략 프레임워크
693. Deception Technology —밀관/밀망/ canary token
694. Honey Pot — 유인 시스템
695. Honey Net — 유인 네트워크 세그먼트
696. Canary Token — 조기 탐지용 경보
697. 파일 canary — 조기 침해 탐지
698. 브라우저 canary — 세션 탈취 탐지
699. 포렌식 이미지 — DD, FTK Imager
700. MD5/SHA-256 해시 — 증거 무결성 검증
701. FTK / EnCase — 포렌식 도구
702. AXIOM — Magnet Forensics 포렌식
703. UAC요과 — 사용자 계정 컨트롤 우회
704. LSASS 추출 — Mimikatz, procdump
705. SAM hive 추출 — reg save HKLM\SAM
706. Kerberoasting — SPN 요청 티켓 hash 추출
707. AS-REP Roasting — 사전 인증 미사용 계정 공격
708. DCSync — DC에서 크리덴셜Replication 요청
709. NTDS.dit 추출 — DC 데이터베이스 직접 추출
710. BloodHound — AD 공격 경로 분석 도구
711. CrackMapExec — 네트워크 크리덴셜 공격 도구
712. Empire / PowerShell Empire — 포스트-침투 프레임워크
713. Cobalt Strike — 상업용 침투 테스트 도구
714. Sliver — 오픈소스 C2 프레임워크
715. Caldera — MITRE 자동화 적대적 시뮬레이션
716. Red Canary — EDR,위협검출
717. osquery —Endpoint 시각화/쿼리
718. Sysmon — Windows 시스템 모니터링
719. Zeek — 네트워크 트래픽 분석
720. YARA — 악성코드 패턴 규칙

---

## 15. 악성코드 / 공격 기법 — 60개

721. 악성코드 분류 — 바이러스/웜/트로이목마/랜섬웨어/스파이웨어/루트킷
722. 바이러스 (Virus) — 정상 파일에감염, 자기 복제
723. 웹orm — 네트워크 통해 само복제, 독립 실행
724. 네트워크 웜 — 취약점 직접 침투 (Code Red, SQL Slammer)
725. 이메일 웜 — 메일부건/링크 (ILOVEYOU)
726. 트로이목마 — 겉보기에 정상, 실질적으로 악성
727. バックドア — 정상software위장된 후면입구
728. 드롭퍼 (Dropper) — 다단계 Downloader
729. Downloader — 원격에서 추가 악성코드 가져옴
730. 랜섬웨어 공격 체인 — 파일 암호화 후 몸값
731. CryptoLocker — 2014년 대규모 랜섬웨어
732. WannaCry — 2017년 글로벌, EternalBlue 활용
733. NotPetya — 2017년 Ukraine 전력망공격
734. Ryuk — 목표형 대규모 랜섬웨어
735. 이중extortion — 암호화+데이터 유출
736. RaaS (Ransomware as a Service) — 랜섬웨어 임대 서비스
737. Locker — 화면 잠금형 Ransomware
738. wipers — 데이터 파괴 목적
739. 스파이웨어 (Spyware) — 사용자 활동 감시
740. 키로거 — 키입력 기록
741. 애드웨어 (Adware) — 강제 광고 표시
742. cryptominer — 시스템 자원 활용 암호화폐 채굴
743. bots — 명령 제압력 갖춘 감염 호스트
744. botnet — 다수의 bots 집합
745. botnet 구조 — 중앙집중형 (C&C)/P2P
746. C2 (Command and Control) — 봇넷 지휘 통제
747. Cobalt Strike Beacon — 침투 테스트용 C2
748. APT (Advanced Persistent Threat) — 국가/조직적 위협
749. APT 그룹 — Lazarus(북한국), FIN7(범죄조직), APT29(러시아)
750. APT 공격 단계 — 정찰/침투/내부정찰/횡향이동/유지/데이터반출
751. First Initial Access — 최초 침투 수단
752. 피싱 (Phishing) — 가장 일반적인 침투 수단
753. 스피어 피싱 (Spear Phishing) — 목표 맞춤형
754. 웨일링 (Whaling) — 임원 대상 고대상 피싱
755. BEC (Business Email Compromise) — 경영자 사칭 금융 사기
756. 스미싱 (Smishing) — SMS 기반 피싱
757. 비싱 (Vishing) — 전화 기반 피싱
758. 사전조사 (Pretexting) — 거짓 상황 구성
759. 테일게이팅 (Tailgating) — 따라 들어가기
760. 버스딩 (Busybasing) —주의력전이
761. 제로데이 — 공개되지 않은 취약점 리용
762. watering hole — 목표 집합 자주 방문 사이트 감염
763. drive-by download — 악성 사이트 접근만으로 감염
764. 공응련공격 — 소프트웨어 개발망 침해 (SolarWinds)
765. 업데이트 역추적 (Update Interception) — 자동갱신 가로채기
766. 다형성 (Polymorphic) — 암호화된 코드,정마 변경
767. 메타모픽 (Metamorphic) — 코드 자체 변환
768. armored virus —정마 회피를 위한 보호 층
769. 파일리스 (Fileless) — 메모리만 사용, 파일 없는 공격
770. LOLBins (Living Off the Land) — 정당한 도구 활용
771. PowerShell 공격 — 메모리 내 스크립트 실행
772. WMI 공격 — WMI 이벤트소비자 활용
773. JScript/VBScript 공격 — 스크립트 기반
774. 레지스트리 런키 — 자동 실행 등록 정보
775. 예약 작업 (Scheduled Task) — 정기적 실행
776. 서비스 등록 — Windows 서비스로잠복
777. DNS 터널링 — DNS 프로토콜 내 데이터 반출
778. ICMP 터널링 — ICMP 패킷 내 데이터 운반
779. HTTPS 역투명 relay — 내부망 통신 외부로
780. 동적 프록시 — 감염 호스트를 Proxy로 활용

---

## 16. 데이터 / 개인정보 보호 — 55개

781. 개인정보 (Personal Information) — 재식별 가능 정보
782. 민감정보 — 건강/범죄기록/유전정보/ biometric
783. 개인정보보호법 (한국) — 수집/처리/제공/파기 원칙
784. 개인정보 3대 원칙 — 수집 제한/목적 명확/보유 기간
785. 개인정보 영향평가 (PIA) — 고위험 처리전 평가
786. 개인정보 파일 표준 protection 지침 — 한국 개인정보보호법 시행규칙
787. 정보보호 관리체계 (ISMS-P) — 한국 통합 인증
788. 정보통신서비스제공자 (ISP) — 한국법상 의무
789. 리용약관 — 서비스 제공을 위한 기본 계약
790. 동의 방식 — 필수 동의/선택 동의
791. GDPR (EU General Data Protection Regulation) — 2018 시행
792. GDPR 6가지 처리 근거나유 — 동의/계약/법적 의무/생명 보호/공익/정당한 이해관계
793. 정보 주체 권리 — 접근/정정/삭제/처리 제한/이동/거부
794. Right to be Forgotten — 삭제권 (GDPR 17조)
795. Data Portability — 이동권 (GDPR 20조)
796. DPIA (Data Protection Impact Assessment) — GDPR 의무
797. DPO (Data Protection Officer) — 개인정보 보호관
798. Breach Notification — 72시간 내 신고 의무
799. 개인정보 해외 이전 — 충분성 인정 국가/표준 계약 조항
800. CCPA (California Consumer Privacy Act) — 2020 시행
801. CPRA (California Privacy Rights Act) — CCPA 강화
802. PDPA (Personal Data Protection Act) — 싱가포르
803. 개인정보보호 법률체계 — 한국/미국/EU 비교
804. ISMS-P 심사 — 기술적/관리적/물리적 안전 Control 평가
805. 정보보호 주요안전관리 —
806. 개인정보 유출 사고 — 신고/통지/공표 의무
807. 과태료/벌칙 — 한국 개인정보보호법 제64조
808. 데이터 분류 — 공개/내부/기밀/극비
809. 데이터 주권 — 국가별 데이터본지화 법규
810. 데이터 이동 — Cross-border 데이터 흐름
811. 클라우드 개인정보보호 — 데이터 소재지 주의
812. 데이터닉명화 — 완전히 역추적 불가능
813. 데이터가명화 — 식별가능성 제거,pseudo-anonymization
814. k-익명성 — k-person indistinguishability
815. l-다양성 — 민감 속성 다변화
816. t-근접성 — 레코드 분포 유사성
817. 차분 개인정보보호 — differential privacy
818. 합성 데이터 — Synthetic data 생성
819. 데이터 마스킹 — 동적/정적 마스킹
820. 토큰화 (Tokenization) — 원본↔토큰 매핑
821. TTT (Tokenization-as-a-Service) — 클라우드 토큰화
822. Format Preserving Encryption — FPE, 원 데이터 형식 유지
823. DLP (Data Loss Prevention) — 데이터 반출 방지
824. DLP 구성요소 —엔진/에이전트/서버
825. DLP 정책 — 콘텐츠 검사/컨텍스트 기반
826. 네트워크 DLP — 네트워크 경계 데이터 통제
827. 엔드포인트 DLP — 단말기 내 데이터 통제
828. 클라우드 DLP — SaaS/ PaaS/IaaS 데이터 보호
829. CASB (Cloud Access Security Broker) — 클라우드 가시성/제어
830. 데이터베이스 보안 — 접근 통제/암호화/감사
831. 필드 레벨 보안 — DB 컬럼/행 수준 접근 제어
832. DB 감사 — 접속 기록, 질의 로그
833. 전송 중 암호화 — TLS, IPsec
834. 저장 중 암호화 — TDE, 디스크 암호화
835. 메모리 내 암호화 — 클라우드 HSM

---

## 17. 보안 프레임워크 / 컴플라이언스 — 55개

836. ISO/IEC 27001 — 정보보안 management 시스템 (ISMS)
837. ISMS 인증 — 3자 감사, 인증서 발급
838. PDCA (Plan-Do-Check-Act) — 관리 시스템 적용 모델
839. ISO 27001 114개 통제 — Annex A
840. ISO/IEC 27002 — 보안 통제 implementation 지침
841. ISO/IEC 27005 — 정보보안 위험 관리
842. ISO 27017 — 클라우드 서비스 보안 통제
843. ISO 27018 — 클라우드 PII 보호
844. ISO 27701 — 개인정보보호 정보안전관리
845. ISO 22301 — 사업 연속성 관리 시스템 (BCMS)
846. NIST CSF 2.0 —Identify/Protect/Detect/Respond/Recover + Govern
847. NIST CSF Tier — Risk Inform/Repeatable/Adaptive
848. NIST SP 800-53 — 연방 정보시스템 보안 통제 (800+ 통제)
849. NIST SP 800-171 — CUI 보호 (110 통제)
850. NIST SP 800-207 — 제로 트러스트 아키텍처
851. NIST SP 800-63 — 디지털 신원 지침
852. NIST SP 800-63A — Enrollment and Identity Proofing
853. NIST SP 800-63B — Authentication and Lifecycle
854. NIST SP 800-63C — Federation and Assertions
855. SOC 2 — AICPA 서비스 조직 통제 보고서
856. SOC 2 Trust Service Criteria — 보안/가용성/처리 무결성/궤밀성/은사
857. SOC 2 Type I/II — 설계 적정성/운영 효과성
858. SOC 3 — 공용 버전 SOC 2
859. PCI DSS v4.0 — Payment Card Industry Data Security Standard
860. PCI DSS 12개 요구사항 — 방화벽/비밀번호/데이터 보호 등
861. PCI DSS 수준 —merchant/service provider 등급
862. PA-DSS — Payment Application Data Security Standard
863. HIPAA — 미국 의료정보 보호법
864. PHI (Protected Health Information) — HIPAA 적용 정보
865. HITECH — 미국 의료기술법, 위반 시 책임 강화
866. GLBA (Gramm-Leach-Bliley Act) — 미국 금융정보보호
867. FERPA — 미국 교육 기록 프라이버시
868. CMMC (Cybersecurity Maturity Model Certification) — 미국 방위산업
869. CMMC 5단계 — Level 1~5 점진적 인증
870. FISMA — 미국 연방 정보 보안 법
871. FedRAMP — 미국 정부 클라우드 보안 인증
872. FedRAMP Moderate/High — 영향 수준별 기준
873. ITGrc — IT 거버넌스/리스크/컴플라이언스
874. SABSA —Business-driven 보안 아키텍처
875. TOGAF — 기업 아키텍처 프레임워크
876. Zachman Framework — EA planning 매트릭스
877. CIS Controls v8 — 18개 핵심 보안 통제
878. CIS Safeguard — Implement/M측량/관리
879. COBIT 2019 — IT 거버넌스 프레임워크
880. ITIL (Information Technology Infrastructure Library) — IT 서비스 관리
881. Privacy by Design — 설계 단계 개인정보 보호
882. PbD 7기본원칙 — 사전 보호/기본값사밀성 등
883. CC (Common Criteria) / ISO 15408 — 제품 보안 인증
884. CC EAL — 평가 보증 수준 (EAL 1~7)
885. FIPS 140-2/3 — 암호 모듈 보안 표준
886. K-ISMS — 한국 정보보호관리체계 인증
887. 정보보호평가 — 한국호련망진흥원 (KISA)
888. 전자금융감독규정 — 금융 전산 보안 기준
889. 금융감독원 (FSS) — 금융 사이버 감독
890. SBOM (Software Bill of Materials) — 소프트웨어 부품 목록

---

## 18. IoT / OT / ICS / 물리 보안 — 50개

891. OT (Operational Technology) — 운영기술, 산업공제시스템
892. OT vs IT — reliability/availability/real-time 차이
893. ICS (Industrial Control System) — 산업 제어 시스템
894. SCADA (Supervisory Control and Data Acquisition) — 원격 감시 제어
895. DCS (Distributed Control System) — 분산 제어 시스템
896. PLC (Programmable Logic Controller) — 현장 제어기
897. RTU (Remote Terminal Unit) — 원격 터미널 장치
898. Modbus 프로토콜 — 산업용 직렬 통신, 암호화 없음
899. DNP3 — 전력/상하수도 SCADA 프로토콜
900. PROFINET — 산업용 이더넷
901. EtherNet/IP — CIP 기반 산업용 이더넷
902. Purdue 모델 — IT/OT 네트워크 5단계분층
903. Purdue 레벨 0~5 — Field/Level 1~2 (OT)/Level 3 (DMZ)/Level 4~5 (IT)
904. IEC 62443 — 산업 사이버보안 표준
905. ISA/IEC 62443 보안 레벨 — SL 0~4 (no security->most secure)
906. SL-CF (Security Level Capability) — 시설 보안 수준
907. SL-TF (Security Level Target) — 목표 보안 수준
908. Zone/Conduit 모델 — 구역 분리+ conduits통제
909. Zone 맵핑 — 자산 분류-> security level
910. NIST IR 8259 — IoT 보안기초
911. NIST IR 8259D — IoT 제조 상arangement
912. OWASP IoT Top 10 — 취약한 펌웨어/기본 계정/불안전한 접구
913. IoT 보안 설계 —Secure by Default, 최소 기능 원칙
914. IoT 펌웨어 보안 — 서명 검증, 안전 업데이트
915. IoT 데이터 보안 —보존중/전수중/처리중
916. Secure Boot — 부팅 과정 소프트웨어 무결성 검증
917. rantai-root-of-trust — 신뢰의 근원
918. RoT 구성요소 — CRTM, Bootloader, Bootloader certificates
919. TPM 원격 증명 (Remote Attestation) — TPM 측정값을 원격에서 검증하는 과정
920. 펌웨어 업데이트 보안 —첨명험증, 롤백 방지
921. MQTT 보안 — TLS, 인증, ACL
922. BACnet — 건물 자동화 프로토콜
923. ，차량네트워크 보안 — UNECE WP.29
924. ISO/SAE 21434 — 자동차 사이버보안 엔지니어링
925. TARA (Threat Analysis and Risk Assessment) — 자동차 위협 분석
926. 의료기기 보안 — FDA cybersecurity 지침
927. 의료기기 사이버보안 관리 — 디자인 단계부터
928. 스마트 그리드 보안 — AMI 보안
929. NERC CIP — 북미 전력 신뢰성 Corporation
930. 원자력 사이버보안 — IAEA 안전기준
931. 위성 통신 보안 —，항ジャミング/스푸핑
932. 물리적 보안 3대 요소 —위섭/ Delay/ Detection
933. CCTV (폐쇄 회로텔레비전) — 영상 감시
934. 접근 제어 시스템 — 카드/RFID/바이오메트릭
935. Mantrap — 이중 문으로 인적 격리
936. 주변 보안 — 담장/감시/순사
937. 환경 통제 — 온도/습도/소화기
938. 서버실 보안 — Tier 1~4수거중심분급
939. Faraday Cage — 전자기 차폐
940. 금속 탐지기/ X-ray — 물리적협위 탐지

---

## 19. AI / 신기술 보안 — 50개

941. AI 보안 — AI 시스템의 안전+AI 활용 보안
942. 적대적 예제 (Adversarial Example) — 미세한 perturbation로 오분류
943. FGSM (Fast Gradient Sign Method) — 1단계 적대적우동
944. PGD (Projected Gradient Descent) — 반복적 적대적우동
945. Carlini-Wagner 공격 — 강력한 적대적 공격
946. 물리 세계 적대적 공격 — 도로 표지판 등 실환경 공격
947. 데이터 포이즈닝 (Data Poisoning) — 훈련 데이터 오염
948. Clean-Label Poisoning — 레이블 유지한 데이터 오염
949. Backdoor Attack — 특정 트리거 입력에 반응
950. 모델 추출 (Model Extraction) — 쿼리 기반 모델 역추출
951. Model Inversion — 훈련 데이터 재구성
952. Membership Inference — 특정 데이터 훈련 여부 추론
953. AI 모델 탈취 — API 쿼리로 모델 복제
954. 모델 무결성 공격 — 사본 배포, 악성 교체
955. 프롬프트 인젝션 — LLM 지시어 오버라이드
956. Jailbreaking — LLM 안전 필터 우회
957. 적대적 프롬프트 — 의도한 잘못된 출력 유도
958. 데이터 추출 공격 — 훈련 데이터 기억으로 정보 유출
959. AI 기반 피싱 — 개인화된 대규모 피싱 자동화
960. Deepfake — 합성 미디어, 신원 사칭
961. 딥페이크 탐지 — C2PA, 디지털 워터마킹
962. C2PA (Coalition for Content Provenance and Authenticity) — 콘텐츠 출처
963. SynthID — Google 딥마크
964. AI TRiSM — Gartner, AI 신뢰/위험/보안 관리
965. LLM 가드레일 — 출력 필터링, 안전 레이어
966. Constitutional AI — 원칙 기반 AI 행동 통제
967. AI Red Team — LLM 안전성 테스트
968. 대항성훈련 — 적대적 예제 포함한 재훈련
969. differential privacy in ML — 훈련 데이터 privacy 보호
970. Federated Learning — 분산 훈련, 데이터 불이동
971. Homomorphic Encryption in ML — 암호화된 채로 추론
972. TEE 기반 ML — SGX 등에서 안전한 추론
973. Responsible AI — 공정성/설명가능성/투명성/ privacy
974. AI Incident — AI 관련 보안 사고DB
975. OWASP LLM Top 10 — LLM 보안 취약점
976. LLM01: Prompt Injection — 프롬프트 조작
977. LLM02: Insecure Output — 출력 검증 없이 신뢰
978. LLM03: Training Data Poisoning — 훈련 데이터 오염
979. LLM04: Model Denial of Service — 비용거대적 입력 유발
980. LLM05: Supply Chain — 공급망 취약점
981. LLM06: Sensitive Information Disclosure — 훈련 데이터 유출
982. LLM07: Plugin Abuse — 플러그인 악용
983. LLM08: Autonomous Agent — 자가 실행 에이전트 위험
984. 양자 컴퓨팅 — 양자 중첩/얽힘으로 계산 혁신
985. 양자 위협 — RSA/ECC 깨뜨릴 Shor 알고리즘
986. Grover 알고리즘 — 대칭키 강도반감
987. NIST PQC 표준 — Kyber/Dilithium/Falcon/SPHINCS+
988. crypto agility — 알고리즘 교체 능력
989. 블록체인 보안 — 51% 공격, 이중지불, 스마트 컨트랙트
990. Reentrancy 공격 — 스마트 컨트랙트 재진입취약점

---

## 20. 보안 추가 키워드 / 시험 대비 — 40개

991. Evil Maid Attack — 물리적 접근 후 백도어 설치
992. Cold Boot Attack — 메모리 잔상 읽기
993. DMA 공격 — Thunderbolt/PCIe Direct Memory Access
994. Firewire 공격 — IEEE 1394 DMA 활용
995. Thunderbolt Security — DMA 방어를 위한 레벨 설정
996. USB_BAD — USB 키보드 emulation
997. Rubber Ducky — USB 키보드 emulation 도구
998. Bash Bunny — 다목적 USB 공격 도구
999. OMG Cable — 변형된 USB 케이블
1000. _entropy — 난수 생성 품질
1001. CSPRNG (Cryptographically Secure PRNG) — 암호학적으로 안전한 난수
1002. RDRAND (Intel) — 하드웨어 난수 생성
1003. /dev/urandom — Linux 난수 장치
1004. hardware RNG — 물리적 난수 발생기
1005. entropy source — 난수 생성 원천
1006. Perfect Security — 정보 이론적 안전 (One-Time Pad)
1007. Semantic Security — 암호학적으로 관찰 가능한 차이 없음
1008. IND-CPA / IND-CCA2 — 암호학 안전성 정의
1009. AEAD — Authenticated Encryption with Associated Data
1010. Key Wrapping — KEK 활용
1011. Envelope Encryption — Digital Envelope
1012. CloudHSM — 클라우드 전용 HSM
1013. AWS KMS — Key Management Service
1014. Bring Your Own Key (BYOK) — 고객 관리 키
1015. Hold Your Own Key (HYOK) — 외부 키 보관
1016. Zero Knowledge Proof (ZKP) — 영지식 증명
1017. Commitment Scheme — 약속 기법
1018. Secure Multi-Party Computation (SMPC) — 안전한 다자간 계산
1019. 동형 암호 (Homomorphic Encryption) — 암호문 상태 연산
1020. Functional Encryption — 함수 암호
1021. Searchable Encryption — 검색 가능 암호
1022. 방변조 하드웨어 — Anti-tamper Hardware (TPM/HSM)
1023. Secure Enclave — TrustZone/SGX 격리 영역
1024. TEE (Trusted Execution Environment) — 신뢰 실행 환경
1025. Security Chaos 엔진ering — 보안 카오스 엔지니어링
1026. 침해 시뮬레이션 (BAS) — Breach & Attack Simulation
1027. 사이버 보험 — Cyber Insurance
1028. Bug Bounty — 버그 바운티
1029. Responsible Disclosure — 책임 있는 공개
1030. Coordinated Disclosure — 협력적 공개


## 추가 학습 키워드 (Additional Study Keywords)

- HSTS (HTTP Strict Transport Security)
- A0X Injection Overview
- OWASP Top 10 2021 Overview (OWASP Top 10 2021 Overview)
- CSRF (Cross-Site Request Forgery)
- Memory Management Security
- Password Authentication
- One-Time Password & Time-Based OTP
- Multi-Factor Authentication, MFA
- Sniffing Detection Arp Ping Promiscuous Mode
- Routing Protocol Authentication Bgp MD5 Tcp Hijacking
- DNS Spoofing
- Ipsec Tunnel Transport Mode VPN Encapsulation
- AH (Authentication Header)
- ESP (Encapsulating Security Payload)
- Ssl TLS Handshake Session Key Exchange Https
- Vpn Virtual Private Network Tunneling Encryption
- X509 Certificate PKI Digital Signature Format
- Hash Function
- DoS/DDoS
- Botnet Cnc Zombie Pc Ddos Infrastructure
- Cloud Native Network Cni Kubernetes Pod Overlay
- Blind SSRF (Blind Server-Side Request Forgery)
- XXE (XML External Entity Injection)
- XXE Attack Flow
- Insecure Deserialization
- Java Deserialization
- pickle Deserialization (Python Pickle Insecure Deserialization)
- PHP Object Injection (PHP Object Injection)
- Prototype Pollution (JavaScript Prototype Pollution)
- ReDoS (Regular Expression Denial of Service)
- Open Redirect
- Host Header Injection
- HTTP
- Subdomain Takeover

---

**총 키워드 수: 800개**
