+++
title = "03. 데이터통신/네트워크 키워드 목록"
date = 2026-03-04
[extra]
categories = "studynotes-network"
+++

# 데이터통신 / 네트워크 키워드 목록 (1,200+ 심화 확장판)

정보통신기술사·컴퓨터응용시스템기술사 및 전문 엔지니어를 위한 데이터통신/네트워크 전 영역 핵심 및 심화 키워드 1,200선입니다.

---

## 1. 데이터통신 기초 및 신호처리 (70개)
1. 데이터통신 시스템 구성요소 (단말장치 DTE, 데이터회선종단장치 DCE, 통신제어장치 CCU)
2. 정보처리장치 (Host Computer, Front-End Processor FEP)
3. 아날로그 신호 (연속적, 증폭기) vs 디지털 신호 (이산적, 리피터)
4. 배드보 (Baud Rate, 변조 속도) vs 비트레이트 (Bit Rate, 전송 속도)
5. 비트 시간 (Bit Duration) / 심볼 시간 (Symbol Duration)
6. 아날로그 통신 vs 디지털 통신
7. 기저대역 전송 (Baseband Transmission) / 대역통과 전송 (Broadband Transmission)
8. 단방향 (Simplex) / 반이중 (Half-Duplex) / 전이중 (Full-Duplex)
9. 직렬 전송 (Serial) vs 병렬 전송 (Parallel)
10. 동기식 전송 (Synchronous) vs 비동기식 전송 (Asynchronous)
11. 비동기식 전송 - 시작/정지 비트 (Start/Stop Bit), 프레이밍 에러
12. 동기식 전송 - 문자 동기방식 (SYN, BSC), 비트 동기방식 (SDLC, HDLC)
13. 대역폭 (Bandwidth), 대역폭-효율성 관계
14. 처리량 (Throughput) / 굿풋 (Goodput)
15. 지연 (Latency/Delay) - 데이터 관점
16. 전파 지연 (Propagation Delay) - 거리/속도
17. 전송 지연 (Transmission Delay) - 패킷길이/대역폭
18. 큐잉 지연 (Queueing Delay) - 라우터 버퍼
19. 처리 지연 (Processing Delay) - 헤더 검사, 라우팅
20. 나이퀴스트 채널 용량 (Nyquist Capacity) - 무잡음 채널, C = 2B log2(M)
21. 샤논의 채널 용량 (Shannon Capacity) - 잡음 채널, C = B log2(1 + S/N)
22. 심볼 상호 간섭 (ISI: Inter-Symbol Interference)
23. 나이퀴스트 펄스 포맷 / 아이패턴 (Eye Pattern)
24. 신호 대 잡음비 (SNR, Signal-to-Noise Ratio)
25. 감쇠 (Attenuation), 데시벨(dB) 측정
26. 지연 왜곡 (Delay Distortion)
27. 백색 잡음 (White Noise) / 가우스 잡음
28. 충격 잡음 (Impulse Noise) / 열 잡음 (Thermal Noise)
29. 상호변조 잡음 (Intermodulation Noise)
30. 누화 (Crosstalk, 혼선)
31. 에코 (Echo, 반향)
32. 회선 제어 규약 (Line Discipline)
33. 엔트 (ENQ) / 애크 (ACK) / 나크 (NAK) / EOT
34. 에러 검출율 (Error Detection Rate)
35. 부호화 (Encoding) - Line Coding, Block Coding
36. Line Coding - 단극성 (Unipolar), 극성 (Polar), 양극성 (Bipolar)
37. NRZ (Non-Return to Zero) - NRZ-L, NRZ-I
38. RZ (Return to Zero) - 동기화 장점, 대역폭 증가
39. 맨체스터 (Manchester) 부호화 / 차분 맨체스터 (Differential Manchester)
40. AMI (Alternate Mark Inversion) / Pseudoternary
41. 차분 부호화 (Differential Encoding)
42. 4B/5B, 8B/10B 부호화 (Block Coding)
43. B8ZS (Bipolar with 8-Zero Substitution) / HDB3 (High-Density Bipolar 3 zeros)
44. 변조 (Modulation) 필요성 - 안테나 크기, 주파수 다중화
45. 진폭 편이 변조 (ASK, Amplitude Shift Keying)
46. 주파수 편이 변조 (FSK, Frequency Shift Keying)
47. 위상 편이 변조 (PSK, Phase Shift Keying)
48. BPSK (Binary PSK, 1bit/symbol) / QPSK (Quadrature PSK, 2bit/symbol)
49. OQPSK (Offset QPSK) / Pi/4 QPSK
50. M진 PSK (8PSK, 16PSK)
51. 직교 진폭 변조 (QAM, Quadrature Amplitude Modulation) - ASK+PSK 혼합
52. 16-QAM, 64-QAM, 256-QAM, 1024-QAM
53. 성상도 (Constellation Diagram) - 진폭과 위상 표시
54. 반송파 (Carrier Wave)
55. 아날로그 연속파 변조 - AM, FM, PM
56. 표본화 (Sampling), 표본화 정리 (Sampling Theorem)
57. 에일리어싱 (Aliasing) - 표본화 주파수 부족시 발생
58. 폴딩 주파수 (Folding Frequency)
59. 양자화 (Quantization) - 선형/비선형
60. 양자화 잡음 (Quantization Noise/Error), 양자화 스텝
61. 컴팬딩 (Companding) / 압신 - μ-law, A-law
62. 펄스 부호 변조 (PCM, Pulse Code Modulation) 처리 과정
63. DPCM (Differential PCM) - 차분 펄스 부호 변조
64. ADPCM (Adaptive DPCM) - 적응형 차분 펄스 부호 변조
65. 델타 변조 (DM, Delta Modulation) - 1비트 전송
66. 적응형 델타 변조 (ADM)
67. 경사 과부하 잡음 (Slope Overload Noise) / 그래뉼러 잡음 (Granular Noise)
68. 스펙트럼 확산 (Spread Spectrum)
69. 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스
70. 주파수 도약 확산 스펙트럼 (FHSS, Frequency Hopping Spread Spectrum)

## 2. 다중화 및 다중접속 기술 (50개)
71. 다중화 (Multiplexing) 개념 및 특징
72. 공간 분할 다중화 (SDM, Space Division Multiplexing)
73. 주파수 분할 다중화 (FDM, Frequency Division Multiplexing)
74. 보호 대역 (Guard Band)
75. 시분할 다중화 (TDM, Time Division Multiplexing) (타임디비전 멀티플렉싱)
76. 동기식 시분할 다중화 (Synchronous TDM) - 정적 타임슬롯 할당
77. 비동기식/통계적 시분할 다중화 (Asynchronous/Statistical TDM) - 동적 할당
78. 비트 교차 (Bit Interleaving) / 워드 교차 (Word Interleaving)
79. 광파장 분할 다중화 (WDM, Wavelength Division Multiplexing)
80. 저밀도 파장 분할 다중화 (CWDM, Coarse WDM)
81. 고밀도 파장 분할 다중화 (DWDM, Dense WDM) - EDFA 증폭기 사용
82. 코드 분할 다중화 (CDM, Code Division Multiplexing)
83. 직교성 (Orthogonality) 원리
84. 직교 주파수 분할 다중화 (OFDM, Orthogonal FDM)
85. 부반송파 (Subcarrier)
86. CP (Cyclic Prefix) / GI (Guard Interval) - ISI 방지
87. 다중 접속 (Multiple Access) 개념 (MAC 계층 연관)
88. FDMA (Frequency Division Multiple Access)
89. TDMA (Time Division Multiple Access) - 슬롯 할당
90. CDMA (Code Division Multiple Access) - 왈시 코드 (Walsh Code)
91. 동기식 CDMA vs 비동기식 CDMA (WCDMA)
92. 근거리-원거리 문제 (Near-Far Problem) - CDMA 전력 제어
93. 셀 호흡 (Cell Breathing) 현상
94. OFDMA (Orthogonal Frequency Division Multiple Access) - LTE, 5G
95. NOMA (Non-Orthogonal Multiple Access) - 비직교 다중 접속 (5G/6G 기술)
96. 공간 분할 다중 접속 (SDMA, Space Division Multiple Access)
97. MIMO (Multiple-Input Multiple-Output) 다중 안테나 기술
98. SU-MIMO (Single User MIMO) vs MU-MIMO (Multi-User MIMO)
99. Massive MIMO (대규모 다중 안테나)
100. 공간 다중화 (Spatial Multiplexing)
101. 빔포밍 (Beamforming) - 아날로그/디지털 빔포밍
102. TDD (Time Division Duplexing) - 시분할 이중화 (업/다운링크 분리)
103. FDD (Frequency Division Duplexing) - 주파수 분할 이중화
104. CSMA (Carrier Sense Multiple Access) 반송파 감지
105. 1-Persistent, Non-Persistent, p-Persistent CSMA
106. CSMA/CD (Collision Detection) - 유선 이더넷, 충돌 감지
107. 잼 신호 (Jam Signal) / 백오프 알고리즘 (Backoff Algorithm)
108. CSMA/CA (Collision Avoidance) - 무선 LAN, 충돌 회피
109. RTS/CTS (Request To Send / Clear To Send) - 은닉 노드 문제 해결
110. 노출 노드 문제 (Exposed Node Problem)
111. ALOHA (순수 알로하) - 하와이 대학, 무작위 채널 접근
112. Slotted ALOHA - 슬롯 단위 전송, 충돌 감소
113. 예약 방식 접속 (Reservation Access)
114. 폴링 접속 (Polling Access)
115. 토큰 패싱 (Token Passing) - 토큰 링, 토큰 버스
116. PRMA (Packet Reservation Multiple Access)
117. DAMA (Demand Assignment Multiple Access) - 위성 통신
118. PAMA (Pre-Assigned Multiple Access)
119. CDMA2000 1x / EV-DO (Evolution-Data Optimized)
120. W-CDMA (Wideband CDMA) / HSPA (High Speed Packet Access)

## 3. 전송 매체 및 물리 계층 구성 (70개)
121. 매체(Media) 구분: 유도 매체 (Guided) vs 비유도 매체 (Unguided)
122. 평행 2선식 케이블 (Twin-lead cable)
123. 꼬임 쌍선 케이블 (Twisted Pair Cable)
124. UTP (Unshielded Twisted Pair)
125. STP (Shielded Twisted Pair) / FTP (Foil Twisted Pair)
126. UTP 카테고리 (Cat 3, Cat 5, Cat 5e, Cat 6, Cat 6a, Cat 7, Cat 8)
127. 동축 케이블 (Coaxial Cable) - BNC 커넥터
128. 광섬유 케이블 (Optical Fiber Cable) - 코어(Core), 클래딩(Cladding)
129. 굴절률 (Refractive Index), 전반사 (Total Internal Reflection)
130. 멀티모드 계단형 광섬유 (Multi-mode Step-index)
131. 멀티모드 언덕형 광섬유 (Multi-mode Graded-index)
132. 단일모드 광섬유 (Single-mode Fiber, SMF) / 다중모드 광섬유 (MMF)
133. 분산 (Dispersion) - 모드 분산, 파장 분산
134. 광증폭기 (EDFA, SOA, 라만 증폭기)
135. 광전송 용어 - 광원 (LED, LD), 수광소자 (PIN 디오드, APD)
136. 자유 공간 광통신 (FSO, Free Space Optics) / 레이저 통신
137. 이더넷 물리 계층 표준 (IEEE 802.3 PHY)
138. 10BASE-T, 100BASE-TX (Fast Ethernet)
139. 1000BASE-T (Gigabit Ethernet) - 4페어 사용, 5단계 PAM 변조
140. 10GBASE-T / 10GBASE-SR / 10GBASE-LR
141. 40GbE / 100GbE / 400GbE / 800GbE 이더넷
142. MDI/MDI-X (Medium Dependent Interface)
143. Auto-MDIX (크로스 케이블 자동 인식)
144. 케이블 배선: 다이렉트 케이블 (T568B) vs 크로스오버 케이블
145. DSU (Digital Service Unit) / CSU (Channel Service Unit)
146. 모뎀 (Modem, Modulator/Demodulator)
147. 케이블 모뎀 (Cable Modem) / DOCSIS 표준
148. VDSL (Very high-bit-rate DSL) / ADSL (Asymmetric DSL) / G.fast
149. RS-232C, RS-422, RS-485 시리얼 통신 인터페이스
150. USB, IEEE 1394 (FireWire)
151. 베이스밴드 중계기 / 리피터 (Repeater)
152. 허브 (Hub) - 더미 허브 (Dummy), 스위칭 허브, 인텔리전트 허브
153. 트랜시버 (Transceiver) / MAU (Medium Attachment Unit)
154. 전파(Radio Wave)의 분류: 장파/중파/단파/초단파(VHF)/극초단파(UHF)
155. 마이크로파 (Microwave) - 1GHz~300GHz
156. 밀리미터파 (mmWave) - 30GHz~300GHz
157. 테라헤르츠 (THz) - 6G 통신 대상 대역
158. 가시광 통신 (VLC, Visible Light Communication) / Li-Fi
159. 음향 통신 (수중 음파 통신)
160. 지상파 (Ground Wave) / 천파 (Sky Wave) / 공간파 (Space Wave)
161. 전리층 반사 / 대류권 산란
162. 직선 가시거리 통신 (LOS, Line-of-Sight)
163. 투과율 (Penetration) / 회절 (Diffraction)
164. 산란 (Scattering) / 반사 (Reflection)
165. 프레넬 영역 (Fresnel Zone)
166. 자유 공간 경로 손실 (FSPL, Free Space Path Loss)
167. 페이딩 (Fading) - 대규모(Large-scale) 페이딩 vs 소규모(Small-scale) 페이딩
168. 다중 경로 페이딩 (Multipath Fading) - 주파수 선택적/평탄 페이딩
169. 도플러 효과 (Doppler Effect) / 고속 이동체 통신
170. 다이버시티 시스템 (Diversity System) / 경로 이퀄라이저 (Equalizer)
171. 안테나 (Antenna) 기본 원리 (공진/다이폴)
172. 무지향성 안테나 (Omni-Directional) vs 지향성 안테나 (Directional)
173. 등방성 안테나 (Isotropic Antenna)
174. 안테나 이득 (Antenna Gain, dBi, dBd)
175. 유효 등방성 복사 전력 (EIRP, Effective Isotropic Radiated Power)
176. 야기우다 안테나, 파라볼라 안테나 (Parabolic), 패치 안테나
177. 스마트 안테나 (Smart Antenna) / 위상 배열 안테나 (Phased Array)
178. 스몰셀 (Small Cell) / 매크로셀 (Macro Cell) / 펨토셀 (Femto Cell)
179. 전력선 통신 (PLC, Power Line Communication)
180. xPON (Passive Optical Network) - EPON, GPON, 10G-PON

## 4. 데이터 링크 계층 - 오류성능 및 프로토콜 (90개)
181. 데이터 링크 계층의 역할: 프레이밍, 흐름 제어, 오류 제어, 회선 제어
182. 논리적 링크 제어 (LLC, Logical Link Control) - IEEE 802.2
183. 매체 접근 제어 (MAC, Media Access Control) - IEEE 802.3~802.11
184. 프레이밍 (Framing) 메커니즘
185. 바이트 카운트 (Byte Counting) 방식
186. 플래그(Flag) 방식 - 문자 삽입 (Character/Byte Stuffing) - DLE, STX, ETX
187. 비트 스터핑 (Bit Stuffing) - 01111110 플래그 중복 방지 (5개 1 뒤에 0 삽입)
188. 오류 제어 (Error Control) 개요
189. 비트 에러율 (BER, Bit Error Rate)
190. 순방향 에러 수정 (FEC, Forward Error Correction)
191. 역방향 에러 수정 / 자동 재전송 요청 (ARQ, Automatic Repeat reQuest)
192. 패리티 검사 (Parity Check) - 홀수/짝수, 단방향/이차원(블록) 패리티
193. 검사합 (Checksum) - 1의 보수 합 검사 (IP/TCP/UDP 헤더에 주로 사용)
194. CRC (Cyclic Redundancy Check, 순환 중복 검사)
195. 다항식(Polynomial) 연산 / 생성 다항식 (Generator Polynomial)
196. CRC-16, CRC-32 (Ethernet FCS), CRC-CCITT
197. 버스트 에러 (Burst Error) 검출 능력 유지
198. 해밍 코드 (Hamming Code) - 1비트 수정 2비트 오류 검출
199. 리드-솔로몬 코드 (Reed-Solomon Code) - 블록 오류 정정
200. BCH 코드 / 골레이(Golay) 코드
201. 길쌈 코드 (Convolutional Code) - 연속 스트림, 비터비 알고리즘
202. 터보 코드 (Turbo Code) - 샤논 한계에 근접, LTE
203. LDPC (Low Density Parity Check) - 5G, 초고속 정정
204. 폴라 코드 (Polar Code) - 5G 제어채널 무오류/고신뢰
205. HARQ (Hybrid ARQ) - FEC + ARQ 결합기술
206. Chase Combining / IR (Incremental Redundancy)
207. ARQ 프로토콜 종류
208. 정지-대기 ARQ (Stop-and-Wait ARQ) - 응답 받을때까지 대기, 효율 낮음
209. GBN ARQ (Go-Back-N ARQ) - 오류 발생 프레임부터 재전송 (슬라이딩 윈도우)
210. SR ARQ (Selective Repeat ARQ) - 오류 프레임만 재전송, 수신측 버퍼링 복잡
211. NAK (Negative Acknowledgement)
212. 피기배킹 (Piggybacking) - 데이터 프레임에 ACK 병합
213. 흐름 제어 (Flow Control) - 수신 버퍼 오버플로우 방지
214. 슬라이딩 윈도우 프로토콜 (Sliding Window Protocol) 개념
215. 윈도우 크기 (Window Size), 송신/수신 윈도우
216. HDLC (High-Level Data Link Control) - 비트 동기식 프로토콜, ISO
217. HDLC 프레임 구조 - 플래그, 주소, 제어, 정보, FCS
218. HDLC 국(Station) 종류 - 주국(Primary), 종국(Secondary), 혼성국(Combined)
219. NRM (정규 응답 모드) / ARM (비동기 응답 모드) / ABM (비동기 균형 모드)
220. 정보 프레임(I-Frame), 감독/제어(S-Frame / RR, RNR, REJ, SREJ), 비번호(U-Frame)
221. SDLC (Synchronous Data Link Control) - IBM
222. LAPB (Link Access Procedure Balanced) - X.25 망
223. LAPD (Link Access Procedure on the D channel) - ISDN 망
224. PPP (Point-to-Point Protocol) - 직렬 회선 표준, 바이트 지향
225. LCP (Link Control Protocol) - 링크 설정/폐기 규약
226. NCP (Network Control Protocol) - 네트워크 계층 동적 설정 (IPCP, IPXCP)
227. PAP (Password Authentication Protocol) - 클리어텍스트 인증
228. CHAP (Challenge Handshake Authentication Protocol) - 해시 기반 인증 (3-way)
229. EAP (Extensible Authentication Protocol) - PPP 확장 인증

## 5. 근거리, 광역통신망(LAN/WAN) 및 2계층 장비 (80개)
230. 이더넷 (Ethernet) 구조 및 원리 (IEEE 802.3)
231. MAC 주소 (Media Access Control Address) - 48비트 (OUI 24bit + NIC 24bit)
232. 멀티캐스트 MAC 주소 / 브로드캐스트 MAC 주소 (FF:FF:FF:FF:FF:FF)
233. 이더넷 프레임 포맷 (Ethernet II vs IEEE 802.3)
234. Preamble & SFD (Start of Frame Delimiter)
235. Type 필드 (Ethertype) / Length 필드 (IPv4 = 0x0800, ARP = 0x0806)
236. 페이로드 크기 (46 ~ 1500 bytes), 패딩(Padding)
237. 충돌 도메인 (Collision Domain) / 브로드캐스트 도메인 (Broadcast Domain)
238. 스위치 (Switch) 의 동작 원리
239. MAC 주소 테이블 (MAC Address Table, CAM Table)
240. 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding
241. 에이징 (Aging) / 포트 미러링 (Port Mirroring)
242. 스위칭 방식 - 컷스루 (Cut-through)
243. 스위칭 방식 - 스토어 앤 포워드 (Store-and-forward) - 에러 검출율 높음
244. 스위칭 방식 - 프래그먼트 프리 (Fragment-free) - 앞부분 64바이트만 확인
245. 가상 랜 (VLAN, Virtual LAN) - 논리적 분할, 브로드캐스트 제어
246. IEEE 802.1Q - VLAN 태깅(Tagging), TPID, TCI, VID 필드 (4바이트 추가)
247. 접근 포트 (Access Port) / 트렁크 포트 (Trunk Port)
248. DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용
249. ISL (Inter-Switch Link) - 시스코 구형 VLAN 태깅
250. Native VLAN (언태그드 트래픽 처리용)
251. 루프 문제 (Looping) - 브로드캐스트 스톰 (Broadcast Storm)
252. MAC 주소 호핑 (MAC Flapping)
253. 스패닝 트리 프로토콜 (STP, Spanning Tree Protocol) - IEEE 802.1D
254. BPDU (Bridge Protocol Data Unit)
255. 루트 브리지 (Root Bridge), 루트 포트 (RP), 지정 포트 (DP), 차단 포트 (BP, Non-Designated)
256. 브리지 ID (Priority + MAC), 비용 (Path Cost)
257. STP 4단계 상태 전이 (단절, 청취, 학습, 전송)
258. 컨버전스 시간 (STP 약 30~50초 소요)
259. 포트 패스트 (PortFast) / BPDU Guard (Cisco 확장)
260. RSTP (Rapid STP) - IEEE 802.1w, 컨버전스 1~2초 단축
261. 백업 포트 (Backup Port), 대체 포트 (Alternate Port) 추가
262. MSTP (Multiple STP) - IEEE 802.1s, VLAN 인스턴스 묶음
263. 이더채널 (EtherChannel) / 링크 어그리게이션 (LACP, IEEE 802.3ad/802.1AX) - 포트 결합 대역폭 확장
264. PAgP (Port Aggregation Protocol) - 시스코 전용
265. PoE (Power over Ethernet) - IEEE 802.3af/at/bt, 랜선으로 전력 공급
266. 전용선 (Leased Line) 기초 (E1, T1/T3 망)
267. 다이얼업 다중화, X.25 (패킷 교환 망 원조)
268. 프레임 릴레이 (Frame Relay) - X.25 간소화, 흐름/오류제어 생략
269. PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)
270. DLCI (Data Link Connection Identifier)
271. CIR (Committed Information Rate) / FECN, BECN 혼잡 알림
272. ATM (Asynchronous Transfer Mode) - 비동기 전송 모드, 53바이트 셀
273. ATM 동기화 (셀 헤더의 HEC 사용)
274. VPI / VCI (Virtual Path/Channel Identifier)
275. AAL (ATM Adaptation Layer) - AAL1, AAL2, AAL5 등 트래픽별 지원
276. 패킷 교환 (Packet Switching) vs 회선 교환 (Circuit Switching) vs 메시지 교환
277. 데이터그램 전송 방식 (비연결형 패킷 교환)
278. 가상 회선 전송 방식 (연결형 패킷 교환 - TCP, ATM 등)
279. 브로드밴드통신망 (B-ISDN)
280. 로컬 루프 (Local Loop, 가입자 선로)
281. 토큰 링 (Token Ring) - IEEE 802.5 / 토큰 버스 (Token Bus) - IEEE 802.4
282. FDDI (Fiber Distributed Data Interface) - 이중 링 기반 100Mbps
283. DQDB (Distributed Queue Dual Bus) - IEEE 802.6 MAN 방식
284. PON (Passive Optical Network) / AON (Active Optical Network)

## 6. 네트워크 계층 - IP 프로토콜 및 주소체계 (80개)
285. 네트워크 계층의 핵심 3기능 - 라우팅(경로 설정), 디스패칭(포워딩), 혼잡 제어
286. IPv4 (Internet Protocol Version 4) - RFC 791, 32비트, 비연결성/최선노력 전송
287. IPv4 헤더 구조 (기본 20바이트 ~ 최대 60바이트)
288. 버전 (IV), 헤더 길이 (IHL), 서비스 타입 (TOS/DSCP), 전체 길이 (Total Length)
289. 식별자 (Identification), 플래그 (Flags), 단편화 오프셋 (Fragmentation Offset)
290. DF (Don't Fragment) 비트 / MF (More Fragment) 비트
291. 단편화 (Fragmentation) 및 재조립 (Reassembly)
292. 패킷 캡슐화, MTU (Maximum Transmission Unit) - 이더넷 1500바이트
293. PMTU (Path MTU Discovery) - 경로 최소 MTU 확인 알고리즘
294. TTL (Time to Live) - 루핑 방지, 홉 감소
295. 프로토콜 (Protocol) 필드 - TCP(6), UDP(17), ICMP(1) 등
296. 헤더 체크섬 (Header Checksum) - IPv4 헤더만 무결성 검증
297. IP 주소 고갈 문제, 클라스풀 (Classful) 주소체계
298. 클래스 A, B, C, D (멀티캐스트), E (실험용)
299. 사설 IP (Private IP) 영역: 10.x, 172.16.x~172.31.x, 192.168.x
300. 루프백 IP (Loopback IP) - 127.0.0.1 (로컬호스트)
301. APIPA / 링크 로컬 주소 (169.254.x.x)
302. 브로드캐스트 주소 - 네트워크 브로드캐스트, 리미티드 브로드캐스트(255.255.255.255)
303. 클래스리스 (Classless) 라우팅 (CIDR, Classless Inter-Domain Routing)
304. 서브네팅 (Subnetting) - 네트워크 분할 (AND 연산)
305. 슈퍼네팅 (Supernetting) / 경로 요약 (Route Summarization)
306. VLSM (Variable Length Subnet Mask) - 가변 길이 서브넷 마스크
307. NAT (Network Address Translation) - 공유기 원리
308. Static NAT (1:1) / Dynamic NAT (M:N) / PAT (Port Address Translation = NAPT, 1:N)
309. 헤어핀 NAT (Hairpin NAT, NAT Loopback)
310. ALG (Application Layer Gateway) - NAT 횡단 지원 (FTP 능동모드 등 해결)
311. STUN, TURN, ICE (NAT 횡단/Traversing 기법, VoIP/WebRTC)
312. ARP (Address Resolution Protocol) - 논리 주소를 물리 주소로 (IP -> MAC)
313. ARP 프레임 (요청-브로드캐스트, 응답-유니캐스트)
314. RARP (Reverse ARP) - MAC으로 IP 얻기 (DHCP 이전)
315. Proxy ARP (프록시 ARP) - 다른 서브넷의 IP에 응답 대행
316. Gratuitous ARP (G-ARP) - 자신의 IP 충돌 감지 및 캐시 갱신 목적
317. ARP 캐시 오염 (ARP Cache Poisoning, 스푸핑 공격)
318. ICMP (Internet Control Message Protocol) 진단/오류 알림
319. ICMP 메시지 종류 - Query, Error Reporting
320. Time Exceeded (TTL 만료, Traceroute 원리)
321. Destination Unreachable (목적지 도달 불가 - 포트, 호스트 차단)
322. Echo Request/Reply (Ping 원리) / Source Quench (혼잡 제어, 구형)
323. Redirect 메시지 - 더 나은 라우터 경로 통보
324. IPv6 (Internet Protocol Version 6) - 128비트 차세대 주소
325. IPv6 단순화된 헤더 - 40바이트 고정 (헤더 체크섬 삭제, 단편화 삭제)
326. 트래픽 클래스 (Traffic Class) / 플로우 레이블 (Flow Label)
327. Next Header, 홉 제한 (Hop Limit, TTL 대응)
328. 유니캐스트, 멀티캐스트, 애니캐스트(Anycast, 가장 가까운 노드 응답) - 브로드캐스트 없음
329. 링크 로컬 주소 (IPv6 Link Local, FE80::) / 사이트 로컬 주소
330. EUI-64 (MAC 기반 IPv6 호스트 주소 자동생성)
331. SLAAC (Stateless Address Autoconfiguration) 무상태 주소 자동 설정 - NDP 활용
332. IPv4-IPv6 전환 기술: 듀얼 스택 (Dual Stack), 터널링 (ISATAP, 6to4), 주소 변환 (NAT64/DNS64)
333. IGMP (Internet Group Management Protocol) - IPv4 멀티캐스트 그룹 가입/탈퇴
334. IGMP Snooping (스위치가 멀티캐스트 트래픽 불필요한 포트에 차단)
335. MLD (Multicast Listener Discovery) - IGMP의 IPv6 버전
336. NDP (Neighbor Discovery Protocol) - IPv6의 ARP/ICMP 대체, RS/RA/NS/NA 교환

## 7. 네트워크 계층 - 라우팅, 터널링, QoS (80개)
337. 라우터 구조 판단 - 라우팅 테이블(RIB), 포워딩 테이블(FIB), 제어/데이터 평면
338. CEF (Cisco Express Forwarding) 물리적 포워딩 / 하드웨어 스위칭 (ASIC)
339. 라우팅 (Routing) 개요 - 최적 경로(Best Path) 설정
340. 정적 라우팅 (Static Routing) - 관리자 수동 설정 (지속성, 보안성 높음) / 디폴트 라우터 (0.0.0.0/0)
341. 동적 라우팅 (Dynamic Routing) - 라우팅 프로토콜 운영
342. 메트릭 (Metric) - 최적 경로 산출 기준 (홉 카운트, 대역폭, 지연, 부하 등)
343. 관리 거리 (AD, Administrative Distance) - 프로토콜 우선순위 판단
344. AS (Autonomous System, 자율 시스템) / ASN 분배
345. IGP (Interior Gateway Protocol) - AS 내부 라우팅 (RIP, OSPF, EIGRP 등)
346. EGP (Exterior Gateway Protocol) - AS 외부간 라우팅 (BGP)
347. 거리 벡터 (Distance Vector) 라우팅 알고리즘 - 벨만-포드(Bellman-Ford) 기반
348. 링크 상태 (Link State) 라우팅 알고리즘 - 다익스트라(Dijkstra) 기반 (최단경로/SPF)
349. 거리 벡터 라우팅 루프 방지 - 스플릿 호라이즌 (Split Horizon), 포이즌 리버스 (Poison Reverse)
350. 홀드다운 타이머 (Hold-down Timer), 트리거드 업데이트 (Triggered Update)
351. RIP (Routing Information Protocol) - 거리벡터, 홉 카운트 메트릭(최대 15), 30초 업데이트
352. RIPv1 (클래스풀, 브로드캐스트) vs RIPv2 (클래스리스/VLSM, 멀티캐스트: 224.0.0.9)
353. RIPng (IPv6 용)
354. IGRP - Cisco 구형, 복합 메트릭 (대역폭+지연 등)
355. EIGRP (Enhanced IGRP) - 하이브리드(고급 거리벡터), DUAL(Diffusing Update Alg) 알고리즘
356. EIGRP 특징: 부분/바운디드 업데이트, Unequal-Cost 부하분산, Successor / Feasible Successor
357. OSPF (Open Shortest Path First) - 대표적 링크 상태 프로토콜
358. OSPF 인접성(Adjacency), Hello 패킷, LSA (Link State Advertisement), LSDB 교환
359. OSPF Area 계층적 구조 - Area 0 (Backbone, 전이 공간), ABR (Area Border 라우터), ASBR
360. DR (Designated Router), BDR - 브로드캐스트 망에서 LSA 플러딩 최소화
361. OSPF 트래픽엔지니어링(TE) 연동
362. OSPFv3 (IPv6 지원)
363. IS-IS (Intermediate System to Intermediate System) - CLNP 기반 링크 상태 라우팅, 통신사/백본 선호
364. L1/L2 라우터, L1/L2 Area 체계, IS-IS over Ethernet/IP
365. BGP (Border Gateway Protocol) - AS 간 인터넷 백본 라우팅, 경로 벡터 (Path-Vector)
366. iBGP (내부 맺음), eBGP (외부 맺음), BGP Split Horizon 룰
367. BGP 속성(Attributes) - NEXT_HOP, AS_PATH, LOCAL_PREF, MED
368. BGP Route Reflector / Confederation (iBGP 풀 메시 문제 해결)
369. 멀티캐스트 라우팅 - PIM (Protocol Independent Multicast) - Dense Mode vs Sparse Mode
370. RP (Rendezvous Point, PIM-SM), RPF (Reverse Path Forwarding) 멀티캐스트 루프 방지
371. VRF (Virtual Routing and Forwarding) - 한 라우터 단일 장비에 다수 가상 라우팅 테이블
372. Policy-Based Routing (PBR) / Route Map - 목적지 기준 라우팅 정책
373. MPLS (Multiprotocol Label Switching) - IP가 아닌 20비트 Label로 스위칭
374. LSR (Label Switch Router), LER (Label Edge Router)
375. LDP (Label Distribution Protocol), RSVP-TE
376. MPLS VPN - L3 MPLS VPN
377. 터널링 (Tunneling) 메커니즘 개요
378. GRE (Generic Routing Encapsulation) - 다양한 프로토콜 패키징, 비보안
379. L2TP (Layer 2 Tunneling Protocol) - PPTP+L2F, VPN 확장형
380. IPSec (IP Security Framework) 메커니즘
381. AH (Authentication Header) - 무결성, 인증
382. ESP (Encapsulating Security Payload) - 기밀성, 무결성
383. IKE (Internet Key Exchange), ISAKMP, SA (Security Associations)
384. NAT-T (NAT Traversal) - IPsec이 NAT를 우회하는 기법 (UDP 4500)
385. SSL VPN / TLS VPN
386. DMVPN (Dynamic Multipoint VPN) - GRE + IPsec + NHRP
387. WireGuard (와이어가드) - 터널/트랜스포트 계층 VPN
388. QoS (Quality of Service) - Best Effort, IntServ, DiffServ
389. IntServ (Integrated Services) - 자원 예약 기반 (RSVP)
390. DiffServ (Differentiated Services) - 트래픽 차등 처리, DSCP(6bit) PHB
391. 우선순위 큐 (PQ), 맞춤형 큐 (CQ), WFQ, CBWFQ, LLQ
392. 트래픽 쉐이핑 (Traffic Shaping) / 폴리싱 (Traffic Policing)
393. Leaky Bucket / Token Bucket
394. WRED (Weighted Random Early Detection) 혼잡 제어 꼬리 짜르기 제한
395. HSRP (Hot Standby Router Protocol) - FHRP 류, 라우터 이중화
396. VRRP (Virtual Router Redundancy Protocol) - 개방형 FHRP
397. GLBP (Gateway Load Balancing Protocol)
398. IP SLA - 네트워크 성능 메트릭 모니터링
399. Anycast 라우팅 (BGP Anycast - DNS 서버 이중화용)
400. 로케이터/ID 분리 구조 (LISP - Locator/ID Separation Protocol)

## 8. 전송 계층 - TCP/UDP (60개)
401. 전송 계층의 역할: 종단 간(End-to-End) 오류/흐름/혼잡 제어, 다중화/역다중화
402. 포트 번호 (Port Number) - 16비트, 응용 프로세스 식별
403. Well-Known 포트 (0~1023), Registered 포트 (1024~49151), Dynamic 포트 (49152~65535)
404. 소켓 주소 (Socket Address) = IP 주소 + 포트 번호
405. TCP (Transmission Control Protocol) - 연결 지향형, 신뢰성 전송, 스트림 기반
406. UDP (User Datagram Protocol) - 비연결형, 비신뢰성, 빠른 속도, 메시지 기반
407. TCP 세그먼트 (Segment) 헤더 - 기본 20바이트 ~ 60바이트
408. 소스/목적지 포트 번호, 일련번호 (Sequence Number, 32bit)
409. 확인응답번호 (Acknowledgment Number, 32bit) - 다음 수신할 바이트 번호 (누적 ACK)
410. 헤더 길이/데이터 오프셋 (Data Offset, 4bit)
411. TCP 제어 플래그(6bit) - URG(긴급), ACK(응답), PSH(푸시), RST(초기화), SYN(동기화), FIN(종료)
412. ECN 징후 플래그 - CWR, ECE
413. 윈도우 크기 (Window Size, 16bit) - 수신측 버퍼 여유 공간 (흐름 제어용)
414. 체크섬 (Checksum) - 가상 헤더 (Virtual Header) 포함 (IP + TCP/UDP 헤더)
415. 긴급 포인터 (Urgent Pointer)
416. TCP 3-Way Handshake - 연결 설정 과정 (SYN -> SYN/ACK -> ACK)
417. ISN (Initial Sequence Number) 무작위 할당 이유 (보안성 강화)
418. TCP 4-Way Handshake - 연결 종료 과정 (FIN -> ACK -> FIN -> ACK)
419. TIME_WAIT 상태 (기본 2MSL 대기) - 지연 패킷 수신 및 정상 종료 보장
420. CLOSE_WAIT / LAST_ACK 상태
421. TCP 흐름 제어 (Flow Control) - 수신자 관점, 슬라이딩 윈도우 알고리즘
422. 윈도우 스케일옵션 (Window Scale Option) - 최대 1GB까지 윈도우 확장
423. 송신 버퍼 (Send Buffer) / 수신 버퍼 (Receive Buffer)
424. 어리석은 윈도우 증후군 (Silly Window Syndrome) 문제 
425. 네이글 알고리즘 (Nagle's Algorithm) - 작은 패킷 지연 모음 (송신측 해결)
426. 클라크 해결책 (Clark's Solution) - 수신측 여유 전까지 윈도우 크기 0 유지 (수신측 해결)
427. 지연된 ACK (Delayed ACK) - 응답 패킷 모아서 전송
428. TCP 혼잡 제어 (Congestion Control) - 망(네트워크) 관점, 패킷 유실 방지
429. 혼잡 윈도우 (CWND, Congestion Window)
430. 슬로우 스타트 (Slow Start) - CWND 지수적 증가
431. 임계치 (ssthresh, Slow Start Threshold) 
432. 혼잡 회피 (Congestion Avoidance / AIMD 알고리즘) - CWND 선형 증가
433. 빠른 재전송 (Fast Retransmit) - 중복 ACK 3개(3 Dup-ACK) 수신 시 타임아웃 전 재전송
434. 빠른 회복 (Fast Recovery) - 재전송 후 슬로우 스타트 생략하고 혼잡회피로 진입
435. TCP Tahoe (타임아웃, 3 Dup-ACK 모두 1로 하락) 모델
436. TCP Reno (빠른 재전송/빠른 회복 지원) 모델
437. TCP NewReno / SACK (선택적 확인응답 옵션, 블록 다중유실 회복)
438. TCP BIC / CUBIC - 현대 리눅스 커널 기본 알고리즘 (지수함수 기반 고속망 최적화)
439. BBR (Bottleneck Bandwidth and Round-trip propagation time) - 구글, 지연시간 기반 혼잡제어
440. RTO (Retransmission TimeOut) 측정 방식
441. RTT (Round Trip Time), SRTT (Smoothed RTT) - 혼잡 제어 동적 타이머
442. 칸 알고리즘 (Karn's Algorithm) - 재전송 패킷 RTT 샘플 제외
443. 불필요한 재전송 (Spurious Retransmission) 해결 방안
444. TCP Keep-Alive 타이머
445. 영 윈도우 (Zero Window) 탐색 - Persist Timer
446. MPTCP (Multipath TCP) - 다중 경로 대역폭 결합, 모바일/Wi-Fi 핸드오버 무단절
447. SCTP (Stream Control Transmission Protocol) - 다중 스트림, 멀티 호밍 (Multi-homing), 4단계 핸드셰이크(쿠키방식)
448. UDP 헤더 구조 - 8바이트 (포트, 길이, 체크섬 등 최소 기능)
449. 브로드캐스트 / 멀티캐스트 전송은 UDP만 가능
450. 실시간 전송, 오버헤드 최소화 목적 (VoIP, DNS, 스트리밍)
451. RTP (Real-time Transport Protocol) - UDP 위에서 동작 (순서번호, 타임스탬프)
452. RTCP (RTP Control Protocol) - 품질 감시 모니터링
453. XTP (Xpress Transport Protocol)
454. QUIC (Quick UDP Internet Connections) - 전송 계층 혁신 (멀티플렉싱, 0-RTT/1-RTT 핸드셰이크)
455. QUIC 전송 - TCP가 아닌 UDP 상위에 구현됨
456. HOL (Head-of-Line) 블로킹 문제 해결 (독립적 스트림 처리 적용)
457. QUIC 연결 마이그레이션 (Connection Migration) - IP 변경시에도 연결 유지 (Connection ID)
458. TLS 1.3 기본 내장 - 보안성과 지연 단축 동시 확보
459. FEC 기능 선택적 포함 (초기)
460. 패킷 손실 복구 메커니즘 개선 - 고유 패킷 번호 (재전송시 번호 바뀜)

## 9. 응용 계층 - 웹, 이메일, 파일 전송 (50개)
461. HTTP (HyperText Transfer Protocol) 상태 비저장 (Stateless), 연결형/비연결형 특징
462. HTTP 메서드 (GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD, TRACE)
463. HTTP 1.0 (비지속 연결, 단점) - 매 요청마다 3-Way Handshake
464. HTTP 1.1 - 지속 연결 (Persistent Connection, Keep-Alive), 파이프라이닝 (Pipelining)
465. HTTP 1.1 HOL 블로킹 (선행 응답 대기 지연)
466. HTTP/2 특징 - 바이너리 프레이밍 계층 추가 / SPDY 기반
467. HTTP/2 스트림 (Stream) 다중화 (Multiplexing) - HOL 우회 (단, TCP HOL은 잔존)
468. HTTP/2 헤더 압축 (HPACK 알고리즘 활용)
469. HTTP/2 서버 푸시 (Server Push)
470. HTTP/3 특징 - QUIC 프로토콜 활용, 완전한 멀티플렉싱, QPACK 압축, 연결 지연 거의 없음
471. HTTPS (HTTP over TLS) - 기밀성, 무결성 지원 (포트 443)
472. WWW 캐싱 메커니즘 / 프록시
473. 캐시 제어 헤더 (Cache-Control: max-age, no-cache, no-store 등)
474. ETag / Last-Modified 검증 (304 Not Modified)
475. 쿠키 (Cookie) - 클라이언트 로컬 저장 상태 값
476. 세션 (Session) - 서버 측 상태 저장 값 (SID 발급)
477. REST API (Representational State Transfer) - 자원 중심 구조, HTTP 메서드 매핑
478. GraphQL - 메타 개발, 클라이언트 주도 쿼리 언어, 오버패칭 해소
479. gRPC - 구글 개발, Protocol Buffers (ProtoBuf), HTTP/2 기반 초고속 RPC, 서비스 메시(MSA)
480. WebSocket - 하나의 TCP 연결 위 전이중 (Full-Duplex) 실시간 브라우저-서버 통신
481. SSE (Server-Sent Events) - 단방향 서버 푸시 기술
482. FTP (File Transfer Protocol) - 양방향 연결 (제어포트 21, 데이터포트 20)
483. 액티브(Active) FTP vs 패시브(Passive) FTP 동작 원리 차이
484. TFTP (Trivial FTP) - UDP 기반 간단 파일 전송 (포트 69)
485. SFTP (SSH FTP) - 보안 채널 위 파일 전송 (포트 22)
486. FTPS (FTP over SSL/TLS)
487. 이메일 아키텍처 - MUA(메일 클라이언트), MTA(메일 서버), MDA(메일 수신 에이전트)
488. SMTP (Simple Mail Transfer Protocol) - 메일 발송/중계 (포트 25)
489. POP3 (Post Office Protocol v3) - 서버 메일을 로컬로 다운(삭제) (포트 110)
490. IMAP4 (Internet Message Access Protocol v4) - 서버에 메일 보관 및 다중기기 동기화 (포트 143)
491. SMTPS, POP3S, IMAPS (보안 캡슐화)
492. MIME (Multipurpose Internet Mail Extensions) - 파일 무결성 및 바이너리 데이터 텍스트 인코딩 (Base64)
493. S/MIME - 공개키 암호화 이메일 보안
494. PGP (Pretty Good Privacy) - 웹 오브 트러스트 기반 이메일 암호화 (Phil Zimmermann)
495. SPF (Sender Policy Framework) - 송신 서버 IP 기반 메일 스푸핑 방지 (DNS TXT 확인)
496. DKIM (DomainKeys Identified Mail) - 디지털 서명 메일 위변조 검증
497. DMARC - SPF + DKIM 정책 실패시 처리방침 (수신 거부, 격리 등) 가이드
498. 웹훅 (Webhook) - REST API의 콜백 역방향 호출 구조 (이벤트 발생 시 푸시)
499. BOSH (Bidirectional-streams Over Synchronous HTTP)
500. XMPP (Extensible Messaging and Presence Protocol) - XML 기반 실시간 메신저
501. SIP (Session Initiation Protocol) - VoIP 호/섹션 제어 표준 (텍스트 기반)
502. H.323 - ITU-T 실시간 멀티미디어 화상회의 (바이너리 기반, 구형)
503. IP PBX - 구내 IP 사설 교환기
504. IPTV 멀티캐스트 (IGMP, PIM) 전송
505. WebRTC (Web Real-Time Communication) - 플러그인 없는 브라우저간 P2P 오디오/음성 (Google 주도)
506. CDN (Content Delivery/Distribution Network) - 엣지 노드 위치 캐싱
507. GSLB (Global Server Load Balancing) - 사용자 위치 근접 서버 할당 (DNS 이용)
508. Anycast 기반 CDN 설계
509. OCAP (OpenCable Application Platform)
510. DASH (Dynamic Adaptive Streaming over HTTP) - 동적 대역폭 적응형 영상 스트리밍

## 10. 응용 계층 - DNS 및 네트워크 관리 (40개)
511. DNS (Domain Name System) 계층적 분산 구조 (루트 - TLD - SLD)
512. 재귀적 질의 (Recursive Query) vs 반복적 질의 (Iterative Query)
513. 정방향 조회 (FQDN -> IP) vs 역방향 조회 (IP -> FQDN, in-addr.arpa)
514. DNS 레코드 - A (IPv4), AAAA (IPv6), CNAME (별칭), MX (메일), NS (네임서버)
515. DNS 레코드 - TXT (텍스트, SPF 등 용도), SOA (Start of Authority, 존 시작점)
516. 영역 전송 (Zone Transfer) - 포트 53 TCP (데이터 동기화용)
517. 일반 DNS 질의 - 포트 53 UDP
518. DNSSEC (DNS Security Extensions) - 데이터 무결성 검증, 캐시 포이즈닝 대응 (디지털 서명 포함)
519. DoT (DNS over TLS) - TCP 853 포트, 종단간 DNS 질의 암호화
520. DoH (DNS over HTTPS) - TCP 443 내 HTTP 프로토콜 안에 DNS 질의 은닉 (검열 회피/보안)
521. mDNS (Multicast DNS) / LMNR - 로컬망 이름 해석 (Apple Bonjour)
522. DHCP (Dynamic Host Configuration Protocol) 포트 67, 68
523. DHCP 과정 4단계 (DORA) - Discover -> Offer -> Request -> Ack
524. DHCP Relay Agent (DHCP 릴레이) - 브로드캐스트 패킷을 라우터 넘어로 Unicast 중계 제어
525. DHCP Lease (임대 시간) / DHCP 갱신 (T1/T2 타이머)
526. DHCP Snooping - 불법 DHCP 서버 차단 보안기능 (스위치)
527. NAT/DHCP 결합 환경 (Soho 라우터/공유기)
528. SNMP (Simple Network Management Protocol) - 네트워크 관리 목적, 기본 포트 161 (Manager), 162 (Trap)
529. MIB (Management Information Base) / OID (Object Identifier)
530. SMI (Structure of Management Information)
531. SNMPv1, v2c (Community String 노출 단점)
532. SNMPv3 (사용자 기반 인증, 메시지 암호화 지원 DES/AES)
533. SNMP 명령 - Get, GetNext, Set
534. SNMP Trap - 에이전트 단에서 특정 이벤트 발생 시 자발적/단방향 통지 (알람)
535. Syslog (시스템 로그 프로토콜) - UDP 514, 중앙 로깅
536. NTP (Network Time Protocol) - 계층적 시간 동기화, Stratum 레벨 모델 (UDP 123)
537. SNTP (Simple NTP) / PTP (Precision Time Protocol, IEEE 1588 - 마이크로초 이내 정밀)
538. SSH (Secure Shell) 포트 22 / Telnet (원격 접속) 포트 23 비교
539. NetFlow (Cisco) / sFlow 트래픽 흐름 모니터링 분석 프로토콜
540. RMON (Remote Network Monitoring) - OSI 1,2계층 통계/에러 모니터링, MIB 내장
541. RADIUS (Remote Authentication Dial-In User Service) - UDP 기반 관리자/사용자 인증(AAA), 패스워드만 암호화
542. TACACS+ (Terminal Access Controller Access Control System Plus) - Cisco, TCP 기반 AAA, 본문 전체 암호화, 명령어별 인가 제어
543. LDAP (Lightweight Directory Access Protocol) - X.500 기반 디렉터리 접근 권한 중앙관리 (AD 연동)
544. AAA 보안 모델 (Authentication 인증, Authorization 인가, Accounting 과금/로깅)
545. 커버로스 (Kerberos) - KDC(Key Distribution Center)/티켓 기반 인증, 타임스탬프 재전송 방지
546. OAuth 2.0 - 타사 애플리케이션 보안 인증 위임 프레임워크 (Access Token)
547. SAML 2.0 (Security Assertion Markup Language) - B2B 환경 SSO 구현, XML 기반
548. OpenID Connect - OAuth 2.0 기반 사용자 식별 프로토콜 (ID Token, JWT)
549. JWT (JSON Web Token) - 비상태 서버형 인증 저장
550. X.509 v3 디지털 인증서 표준 규격

## 11. 무선통신 및 이동통신 기초/기술 (50개)
551. 이동통신망(Cellular Network) 통신 개념 (재사용, 핸드오버)
552. 주파수 분할 방식(FDD) vs 시분할 방식(TDD) 무선 환경 적용
553. 매크로 뷰 (Macro Cell) 토폴로지 / 피코 셀(Pico)/마이크로 셀(Micro)
554. 주파수 재사용 (Frequency Reuse) - 클러스터 디자인, 용량 확장 기법
555. Co-channel Interference (동일 채널 간섭) / Adjacent Channel Interference (인접 채널 간섭)
556. 핸드오버 (Handover) / 핸드오프 (Handoff) 종류 개념
557. 하드 핸드오버 (Hard Handoff) - "Break before make", LTE방식
558. 소프트 핸드오버 (Soft Handoff) - "Make before break", 다중 주파수 동시 수신, CDMA 방식
559. 호 수락 제어 (CAC, Call Admission Control)
560. 로밍 (Roaming) - 타 망사업자 통신망간 서비스 연동
561. 이동성 관리 (Mobility Management) - HLR (Home Location Register), VLR (Visitor) 구조
562. MIPv4 (Mobile IPv4) - FA(Foreign Agent), HA(Home Agent), 세모 라우팅 (Triangular Routing) 문제 해결방안 (RO)
563. MIPv6 (Mobile IPv6) - FA 불필요(SLAAC), 기본 최적 경로(RO) 지원
564. 다이버시티 시스템(Diversity System) - 공간(안테나), 주파수, 시간, 편파(Polarize) 다이버시티
565. 레이크 수신기 (Rake Receiver) - 시간 지연된 다중경로 신호 결합(CDMA)
566. 등화기 (Equalizer) - ISI 상쇄 필터
567. 스마트 안테나 (Smart Antenna)
568. 스위칭 빔 (Switched Beam) vs 적응형 어레이 (Adaptive Array 안테나)
569. MIMO 기반 공간 다중화 체계 (V-BLAST 구조 등)
570. WiMAX (IEEE 802.16) / 휴대인터넷(WiBro) 개요 - 와이브로(모바일 WiMAX)
571. 무선 LAN (WLAN) 구조 분산: BSS(Basic Service Set), ESS(Extended Service Set)
572. AP (Access Point) / DS (Distribution System, 분배 시스템)
573. 802.11 b/g/a/n 표준 세대 발전
574. 802.11n (Wi-Fi 4) - MIMO 채용, 채널 본딩 (20->40MHz) 300~600Mbps
575. 802.11ac (Wi-Fi 5) - MU-MIMO (다운링크 한정), 5GHz 대역폭 80~160MHz 
576. 802.11ax (Wi-Fi 6) - OFDMA 도입, 양방향 MU-MIMO, 타겟 웨이크 타임(TWT), 고밀도망 속도 저하 해소
577. 802.11ax 6GHz (Wi-Fi 6E) - 간섭없는 6GHz 대역 무선 환경 확장
578. 802.11be (Wi-Fi 7) - 320MHz 초광대역폭 채널, 4K-QAM 적용, MLO (Multi-Link Operation, 동시 다중링크 작동) 초저지연
579. 무선 LAN 보안 진화 (WEP -> WPA -> WPA2 -> WPA3)
580. WEP (Wired Equivalent Privacy) - RC4 기반, 취약점(정적키) 노출
581. WPA (TKIP + 802.1X + EAP)
582. WPA2 (AES-CCMP 기반) 강력 암호화, 개인용(PSK)/기업용(Enterprise/RADIUS)
583. WPA3 - SAE (Simultaneous Authentication of Equals) 핸드셰이크 도입 (오프라인 딕셔너리 공격 완전차단), 관리 프레임 보호 (PMF, 필수 적용), 192비트 기업급 보안 스위트(CNSA/Suite B)
584. 802.1X (PNAC, Port Based Network Access Control) 인증 및 EAP/RADIUS 체계
585. 캡티브 포털 (Captive Portal) - 게스트 웹 기반 접속 인증
586. 안테나 증폭 측정 지표: dBm 반값 전력각 등
587. 무선 메시 네트워크 (Wireless Mesh Network) - 데이지 체인 구조 연결 자동화
588. MANET (Mobile Ad-hoc Network) - 기지국 없는 노드 기반 네트워크 라우팅 (AODV 규칙)
589. V2X (Vehicle to Everything) - 차량 자율주행, 차량통신 핵심
590. WAVE (IEEE 802.11p 무선차량통신) DSRC(단거리전용)
591. C-V2X (Cellular V2X) - 3GPP 표준, 이동통신(LTE/5G) 연계 차량 통신
592. 위성 통신 (Satellite Comm.) 특징
593. 정지 궤도 위성 (GEO) - 약 35,800km 고도 통신 위성 (지연 심함)
594. 중궤도 위성 (MEO) (GPS, 항법시스템)
595. 저궤도 위성 (LEO) - 500~1500km 고도. 초저지연 글로벌 6G 망 구성, Starlink(스타링크), OneWeb(원웹)
596. HAPS (고고도 전송 기지국, 성층권 드론 통신)
597. GPS (Global Positioning System) 삼각 측량 / 오차 개선 기법 (DGPS, RTK)
598. UWB (Ultra-Wideband) - 초광대역 근거리 정밀 위치인식통신, 임펄스 전송 (Apple AirTag 등)
599. 무선 충전 전송 원리 (자기 유도형 WPC Qi, 자기 공명형 A4WP)
600. RFID / NFC 프로토콜 기본 구상

## 12. 사물인터넷(IoT), WPAN 및 엣지 통신 (50개)
601. 사물인터넷 (IoT, Internet of Things)의 3대 요소 (디바이스, 네트워크, 클라우드/플랫폼)
602. 사물 통신 (M2M) - 기기 간 직접 연결 (IoT의 근본)
603. 센서 네트워크 (WSN, Wireless Sensor Network) / 싱크 노드 (Sink Node) 구성
604. WPAN (Wireless Personal Area Network) - 개인 작업공간 무선
605. 블루투스 (Bluetooth) - IEEE 802.15.1, ISM 대역(2.4GHz), 피코넷(Piconet), 스캐터넷(Scatternet) 마스터/슬레이브
606. 블루투스 버전 - EDR, HS 속도 확장
607. BLE (Bluetooth Low Energy) - BT 4.0, 저전력 특화, IoT 핵심
608. 비컨 (Beacon) 기술 - iBeacon(애플 환경), Eddystone(오픈 소스 블루투스 로케이터)
609. ZigBee (지그비) - IEEE 802.15.4 초저전력 제어/감시용 메쉬 네트워킹 표준, 250Kbps
610. Z-Wave (Z웨이브) - 홈네트워크 최적화 900MHz 무선 통신 반도체 생태계 주도
611. Thread 프로토콜 - IPv6 통신 기반 메시 WPAN 프로토콜 (스마트홈 IoT 지원)
612. Matter (매터) 보안 통일 표준(CSA) - 애플/구글/아마존 간 통일형 스마트홈 상호 운용성 표준 (위 Layer 적용)
613. 6LoWPAN - IEEE 802.15.4 환경의 저전력 장치를 IP 계층인 IPv6 로 인터넷 연동시키는 헤더 압축/단편화 (IoT 핵심)
614. RPL (IPv6 Routing Protocol for Low-Power and Lossy Networks) - IoT 무선 최적 라우팅 알고리즘
615. LPWAN (Low-Power Wide-Area Network) 개요 (저전력 광역 통신) - 수십km 커버리지
616. 비면허 대역 LPWAN 분야
617. LoRa (Long Range) / LoRaWAN 표준 - CSS (Chirp Spread Spectrum) 방식의 비면허 글로벌 저전력 장거리
618. Sigfox - 초협대역(UNB) 100bps 극초저전력, 소용량/프랑스 기반 상용화
619. 면허 대역 LPWAN 분야 (이동통신사 기반형 IoT)
620. NB-IoT (Narrowband IoT) - LTE 주파수 여유 대역/보호대역 기반 200kHz 협대역 활용 IoT 표준 (3GPP Rel.13)
621. LTE-M (eMTC) - Cat-M1 등 음성/1Mbps 이동(핸드오버) 및 웨어러블 지원 IoT
622. MQTT (Message Queuing Telemetry Transport) - TCP 기반 퍼블리시-서브스크라이브 경량 메시지 (QoS 0/1/2 등급 지원) 브로커(Broker) 중심 분산형
623. CoAP (Constrained Application Protocol) - UDP 제어 기반, REST/HTTP 메타 대응 경량 프로토콜, 브로커리스 구조(DTLS 접속 지원)
624. LwM2M (Lightweight M2M) 표준 프로토콜 관리 메커니즘
625. oneM2M 아키텍처 (국제 표준 통합 M2M 구조화 플랫폼)
626. 엣지 컴퓨팅 (Edge Computing, 포그 컴퓨팅 구분) - 종단 클라이언트 인접 노드 데이터 분산 처리 방식
627. MEC (Multi-access Edge Computing / Mobile Edge Computing) - 5G, 이통망 기지국 근접하여 연산, 초저지연 확보
628. 스마트 그리드 (Smart Grid 파워 네트워크 통신 인프라)
629. 마이크로 그리드 (Microgrid) / AMI (원격검침인프라) 통신 (PLC/RF 장치) 탑재 방식
630. 산업용 이더넷 표준 (Industrial Ethernet) - PROFINET, EtherCAT, Modbus TCP (타임크리티컬)
631. OPC UA - 스마트 팩토리, 산업용/제조용 디바이스 안전한 데이터 통신 확장 프로토콜 통합
632. TSN (Time-Sensitive Networking) - IEEE 802.1 / 시간 결정형 유선 이더넷, 정밀 동기(마이크로/나노단위 트래픽 자원 보장/동기화) (산업용 이더넷 대체 5G망 연계)
633. 자율주행 차량 통신 (V2V, V2I 교통인프라 교환)
634. OCF (Open Connectivity Foundation) IoT 통합 관리 계층 표준
635. IETF (Internet Engineering Task Force) 산하 IoT CoRE 워킹그룹 동향
636. W3C WoT (Web of Things) - 모든 기기를 URL 자원으로 통합 제어 개념
637. IIoT (공업계 사물인터넷/산업용 IoT) 트래픽 관리 한계/QoS 이슈
638. 스마트 시티 (Smart City 통신망 다중화 연계) 센싱 시스템
639. 드론 통신 지연시간 관리 및 보안 C2 링크 (Command & Control)
640. AIoT (AI + IoT) 모델 및 클라우드 AI 연결 지연 완화 기술
641. 홈 네트워크 게이트웨이 / 월패드 프로토콜 보안 (RS-485 해킹, 분리 정책 논란)
642. 망분리 (Network Separation) 및 제로 트러스트 연결형 논리망 보안 정책
643. 기기 간 상호인증체계 관리 기법 P2P 연결 인증서 배포 기술
644. DTLS (Datagram TLS) 프로토콜 CoAP 결합
645. 소형 안테나 시스템/초소형 센서 백스캐터 통신 (Ambient Backscatter 통신, 에너지 하베스팅)
646. 무전원 통신 (Passive IoT 통신) 환경 적응
647. CPS (Cyber-Physical System 트윈/메타 데이터 전송 요구사항)
648. 양방향 스마트 계량기 (Smart Meter 통신 규격)
649. 홈넷/IoT 봇넷 방어 기법 (Mirai Botnet DDOS 예방 포트 필터)
650. 저전력/메모리 한계 환경 경량 대칭키 암호 (LEA 표준, ARIA 등 최적화 적용)

## 13. 네트워크 보안 (기본 기법) (50개)
651. 정보보안 3대 요소 (CIA 트라이어드: 기밀성, 무결성, 가용성) + 인증, 부인방지 요구
652. 암호학 (Cryptography) 개요 통신망 보안 적용 (평문->암호문->평문 변환 체계)
653. 대칭키 암호화 (Symmetric Key) - 암/복호화 키 동일, 공유기밀 분배, 고속 처리
654. 스트림 암호 (Stream Cipher) - RC4 (WEP 등, 최신 사장), ChaCha20
655. 블록 암호 (Block Cipher) - DES (56bit 비권장), 3DES (과도기) 모델
656. AES (Advanced Encryption Standard) - 국제 대표 표준, Rijndael 구조 (128/192/256bit 체계)
657. SEED, ARIA, LEA - 대한민국의 표준 블록/경량 암호 방식 체계
658. 블록 암호 운영 모드 (ECB 기본/취약 모드, CBC(IV 필요), CFB, OFB, CTR)
659. GCM (Galois/Counter Mode) 모드 - 암호화와 더불어 데이터 인증 기능 탑재 (AEAD - TLS 1.3의 핵심 모드)
660. 비대칭키/공개키 암호화 (Asymmetric/Public Key) - 암/복호화 키 상이, 서명(개인키)/기밀화(공개키 전송) 가능
661. 수학적 문제 기반(소인수분해, 이산대수 등)
662. RSA 알고리즘 - 가장 보편적 (소인수분해 수학 난해성, 2048bit 권장)
663. ElGamal 및 DSA (디지털 서명용 특화) 시스템
664. ECC (Elliptical Curve Cryptography, 타원 곡선 통신망 적용) - 짧은 키 (256bit)로 RSA 3072bit 효과 발휘 (초고속, 모바일/IoT 적용)
665. ECDSA, Ed25519 (고성능 차세대 공개키 디지털 전자서명 방식)
666. 디피-헬만 상호 키 교환 (Diffie-Hellman Key Exchange) 원리 및 스니핑 취약점
667. 해시 함수 (Hash Function) - 무결성 점검을 위한 일방향 고정길이 압축
668. MD5 (취약성/충돌 노출) 회피 조치, SHA-1 차단
669. SHA-2 패밀리 - SHA-256 / SHA-512 위주 통신망 서명 기본 기술
670. SHA-3 패밀리 - 스펀지(Sponge) 펑션 방식 Keccak 로직, 기존 방어 결함 해소
671. 솔트 (Salt) 첨가 패스워드 해시 (PBKDF2, bcrypt, Argon2) 체계 - 레인보우 테이블 방지
672. 무결성 및 출처 인증용 서명 데이터 코드 제어
673. MAC (Message Authentication Code) 변수 및 기능
674. HMAC (Hash-based MAC) 통신 기반 IPsec 등 활용 구조 - 공유키 결합 해시
675. 전자서명 (Digital Signature) 생성/검증 프로세스 개요 (비대칭키 활용 체계의 무결성 보증)
676. 공개키 기반 구조 (PKI, Public Key Infrastructure) 아키텍처 보안 증명 시스템
677. 인증국 (CA, Certificate Authority), 등록기관 (RA, Registration Authority), 저장소 체계
678. CRL (Certificate Revocation List) 스펙 및 폐기 문제 및 배포 지연 약점 완화 체계
679. OCSP (Online Certificate Status Protocol) - 실시간 인증서 상태 응답 검사 체계
680. OCSP Stapling (TLS Handshake 트래픽 성능 확장용 서버 캐시 상태 전송 메커니즘 개선기법)
681. SSL/TLS (Secure Socket Layer / Transport Layer Security) 통신 모델 개요 
682. TLS Handshake 프로토콜 (3-Way 유사 연결 초기화, 세션키 협상, Cipher Suite 교환 포함)
683. Cipher Suite 모델 표기방식 예시 (TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256) 이해 방식
684. TLS 전방향 안전성 (PFS, Perfect Forward Secrecy) 보장 원리 (RSA 직접 복호 문제 해결/임시 세션키) 
685. TLS 1.3 업그레이드 변화와 0-RTT/1-RTT 성능 향상 차이
686. MAC-then-Encrypt 패러다임 / AEAD 전환 보안 구조
687. 세션 재개 (Session Resumption / TLS Ticket) 기능 구성
688. SNI (Server Name Indication) 개요 와 ESNI / ECH (Encrypted Client Hello) 검열 우회 
689. 양자 내성 암호 (PQC, Post-Quantum Cryptography) 체계 및 통신망 교환 표준 (Shor's Algorithm 위협 대처)
690. 방화벽 (Firewall) 필터링 1,2,3 세대 진화
691. 패킷 필터 (Packet Filter 라우터/L3,L4), 애플리케이션 상태 필터 및 프록시
692. 상태 기반 감시 (Stateful Inspection / 세션 테이블 체크 메모리) 기술의 원리
693. NIDS (Network Intrusion Detection System 분산 탐지) 공격
694. 스노트 (Snort), Suricata (병렬 룰 지원) 와 오용 탐지(Misuse) vs 이상 탐지(Anomaly) 엔진
695. IPS (Network Intrusion Prevention System) 차단 아키텍처 (인라인 구조 배치, 폴스 포지티브 문제 대처방안)
696. WAF (Web Application Firewall, 애플리케이션L7 특화)
697. UTM (Unified Threat Management 패키징 통합형 장비)
698. NGFW (Next-Generation Firewall, 차세대 방화벽 시그니처 융합 모델 딥 패킷 파싱 애플리케이션 ID 제어 적용) 
699. 샌드박스 망분석 시스템 (APT 이메일 악성 포맷 행위 추적 연동) 
700. NAC (Network Access Control 시스템) 내부 접근 단말기 관리 무결성 진단

## 14. 네트워크 보안 (공격 및 위협, 대응책) (50개)
701. 도청 (Sniffing, Eavesdropping) 네트워크 토폴로지 취약 (프론미스큐어스 모드, 스위치 잼 체계 해소)
702. 스푸핑 (Spoofing) 기만 위장 공격 종류 및 특성 분석
703. ARP 스푸핑 (ARP Spoofing) - MAC 주소 기만 타겟 PC 트래픽 탈취, 중간자 정적대응 방어 (Static ARP)
704. IP 스푸핑 (IP Spoofing) - 트러스트 IP 위장 인젝션 우회 및 DDoS 공격 근원
705. DNS 스푸핑 / DNS Cache Poisoning 매칭 결함 포트 번호 난수 제어 취약 노출 방어 기법 (DNSSEC 도입 목적)
706. 중간자 공격 (MitM, Man-in-the-Middle) 도청 흐름과 통제 조치 (TLS 암호 검증 중요성, HSTS 설정 이유)
707. 세션 하이재킹 (Session Hijacking / TCP Seq 번호 추정 절도 등 탈취/Cookie/토큰 갈취 기법)
708. 재생 공격 (Replay Attack 방어 타임스탬프 원리 / 비표 넌스 Nonce 적용)
709. DoS (Denial of Service 가용성 타격 위협 목적) 
710. 분산 서비스 거부 공격 (DDoS, Distributed DoS 위협) 봇넷 시스템 C&C 서버 증폭, 감염 및 반사 
711. SYN Flood 공격 (TCP 3way-Handshake 약점 Backlog 큐 포화 자원 마비 유도)
712. SYN Flood 대응 - SYN Cookie 기술 (상태비저장 SYN/ACK 암호화 처리 후 최종 ACK서 검증) 서버 완화 제어
713. ICMP Smurf 공격 (IP 브로드캐스트+스푸핑) / 스머핑 라우터 IP Directed Broadcast 차단 설계
714. Ping of Death 대형 패킷 단편화 버퍼 오버플로우 문제
715. TearDrop 공격 (IP 헤더 오프셋 중복/오류 단편화 무한 재조립 오류 기만 다운)
716. UDP Flood 리소스 고갈 유도 / Null/Christmas Tree 플래그 비대칭공격 타격 
717. 반사 증폭 공격 (Amplification Attack / DRDoS) 
718. NTP 증폭 (monlist 모니터 목록 명령 악용/수백배 반사)
719. DNS 증폭 (위장 IP로 파싱 데이터/TXT 등 다량 요구 패킷 대형화 수백배 반사 대상자 타격)
720. Memcached 증폭 서버 공격 방어 미흡 (5만배 반사)
721. SLOW GET / SLOW POST 공격(Slowloris) 응용 계층 소켓 점유, 헤더/엔티티를 끊임없이 매우 느리게 보내 Connection 지속 자원 무력화 (일시적 방화벽 필터링, 타임아웃 최소화 대응)  
722. 트래픽 혼잡공격 (CC Attack 봇넷 HTTP 임의페이지 무한 요청) 유도 및 캡챠 적용
723. 랜섬웨어 (Ransomware) 파일공유 139/445망 자가전파 및 피싱 방어 포트 폐쇄 규약 체계 SMBv1 보안 약점 타격 (워너크라이 WannaCry 분석) 
724. 다크 웹 (Dark Web) Tor (The Onion Router 은닉망 릴레이 체계 분석)
725. 스키밍 (Skimming) 공격
726. 무차별 대입 공격 (Brute Force / 사전 Dictionary 제어) 통신 로그인/SSH 타격
727. SQL 인젝션 (OWASP 핵심 웹 구조 보안 약점 WAF 적용 룰 필터망 파라미터 처리망) 
728. 크로스 사이트 스크립팅 (XSS - Reflected/Stored, 브라우저 로컬 데이터 탈취 쿠키 위협망 통신 쿠키보안 CSP 설정 등 세부망 보안 원리)
729. 크로스 사이트 요청 위조 (CSRF 원리 및 방어 토큰 방식 SameSite 설정)
730. APT (Advanced Persistent Threat 고도화 공격망 - 침투-탐색-수집-유출-유지 킬체인 프로세스) 내부 인트라넷 통제 
731. 버퍼 오버플로우 공격 (서비스 다운/원격코드 실행 위협망 타격)
732. 제로 데이 (Zero-day 방어되지 않은 취약점 노출 즉시 전산자원 위협) 공격 
733. 포트 스캐닝 도구 작동 메커니즘 (NMAP 스텔스 스캔 - 반개방형 SYN Scan, FIN Scan 분석망 체계 확인법) 
734. 방화벽 우회기법 (터널링 캡슐화 포트 우회/분산 패킷 망 회피)
735. 비인가 AP (Rogue AP 무선망 트래픽 위조 가로채기 이블트윈 공격 / WIPS 방어 적용망)
736. 포트 포워딩 (Port Forwarding 역방향 타격 문제 제어 원격 포트/점프 스테이션 보안 규정 체계제안)
737. 백도어 (Backdoor 포트 / C2 서버 Beacon 정주기 통신 이상 징후 망 행위 분석 대응 기계학습 모델 개발 방향) 
738. 제로 트러스트 보안 (Zero Trust Architecture, 내부망도 검증, 최소 권한 원칙 지속 검토 적용 프레임워크 설계)
739. 마이크로 세그멘테이션 (Micro Segmentation 시스템망 트래픽 분할 보안통제구조 수평 전파/Lateral Movement 차단 모델) 
740. SASE (Secure Access Service Edge 브랜치 사무소 단말 네트워크 엣지 클라우드 보안 통합체계/ SD-WAN + SWG/CASB 등 플랫폼 구조 융합 모델 개요)  
741. CASB (Cloud Access Security Broker 클라우드 망 접속 보안 모니터/가시성 유지 시스템)
742. SWG (Secure Web Gateway 시큐어 웹 게이트웨이 / 프록시 보안 패키지 모델 구조적 설계)
743. CSPM / CWPP 보안 설정 모니터링 관리 및 워크로드 분산망 보안 맵 체계 가시화 기술 모델화 적용 시스템 
744. 침해 사고 대응 체계 분석 (패킷 미러 포트, 네트워크 포렌식 (Network Forensics), 실시간 로그 (SIEM 인프라) 수집 체계 연계 방법)  
745. SOAR (Security Orchestration, Automation and Response) 자동화 오케스트레이션 적용 망대응 통합 (플레이북 모델 기술 분석 보안)
746. TI (Threat Intelligence) 융합 / STIX, TAXII 표준 지표 관리, IoC (침해지표) 반영 
747. 웹쉘 (Web Shell 모니터, 디렉토리 실행 등 권한 취약 방지 스캔)  
748. 양자 난수 생성기 (QRNG 적용, 순수 예측불허 난수 보안 생성장치 모델)
749. 다크 데이터 / Data Loss Prevention (DLP 네트워크 기반 메일 메신저 단말 외장 유출 차단 모델 시스템 개념 데이터 기밀 탐지 적용 원리 분석 적용 구조 파편 제어)
750. ISO 27001 네트워크 통제 및 개인정보영향평가 인증 모델망 분리 아키텍처 (논리/물리) 망연계 시스템 (스트림 분리 체계 연동 기술 VDI 도입 구성망 보안망 체계적 구조 이해 등 설계 방침 기초)

## 15. 차세대 통신망 (4G/5G/6G) 핵심 아키텍처 (50개)
751. 3GPP (3rd Generation Partnership Project) 표준 개발
752. LTE (Long Term Evolution 4세대 망 진화) All-IP 패킷 교환 완전 전환, OFDMA
753. EPC (Evolved Packet Core 코어망 시스템) S-GW, P-GW 제어 망 트래픽 통합
754. MME (Mobility Management Entity 제어 데이터 평면 구조적 통제 핸드오버)
755. HSS (Home Subscriber Server 가입자 마스터 정보)
756. 기지국: eNodeB 분산 데이터 평면 라우팅 고속망 이동성 통제 진화
757. LTE-A (LTE-Advanced) 캐리어 어그리게이션 (Carrier Aggregation CA 2~5개 주파수 대역 묶음 전송 캐파 향상 제어 속도 증강 기술 규격 제정 진전 표준 체계 진화)
758. VoLTE (Voice over LTE 음성 통화 올 IP 패킷망 진화 우선 제어 처리 SIP QOS 제어망 적용 구조 최적화)
759. 5G 통신 성능 목표 3대 특징 (초고속, 초연결, 초저지연) 기능적 체계 진화 특징 비교 
760. eMBB (Enhanced Mobile Broadband 초고속 광대역 대용량 증강 기술 적용) AR/VR 기술 지원 파급 체계 지원
761. uRLLC (Ultra-Reliable and Low Latency Communications 초안정/초고신뢰 초저지연망 차량 제어/스마트 팩토리 통신 프로토콜 설계 1ms) 
762. mMTC (Massive Machine-Type Communications 초거대 밀도 초다수 연결 사물 기기 IoT 연결망 배터리 저전력 제어 적용 모델 성능 지표 적용)
763. 5G NR (New Radio) 신무선 표준 대역
764. FR1 주파수 (Sub-6GHz 대역, 기존 호환 및 중간 광역/보편 속도 모델 적용 제어) 
765. FR2 주파수 (mmWave 24Ghz~ 밀리미터파 직진성 극한, 장애물 회절 약화 대형 스몰셀 조밀 구성 기술 체계 대역) 
766. NSA (Non-Standalone 코어는 LTE EPC / 기지국 제어 무선 NR 결합 구축 진보 비용 최소 고속도 망 적용 구조 융합 통신 모델)
767. SA (Standalone 코어까지 5G Core(5GC) 풀 전환 클라우드 네이티브 슬라이싱 전체 통제 네트워크 지연 해결 구축 모델 최신 릴리즈 채용 방식) 
768. 5GC (5G Core Network 차세대 코어망 SBA 아키텍처)
769. SBA (Service Based Architecture 네트워크 기능 요소가 컨테이너/마이크로 서비스 RESTful API 간 메시지 연동 호출 통신 플랫폼 융합 모델 기반 구축 코어 서비스 규격 표준) 
770. AMF (Access and Mobility Management Function / MME 대체) 
771. SMF (Session Management Function) / UPF (User Plane Function 데이터 고속 패킷 엣지 통과 모델 구조 지연 개선 구조 체계 데이터 평면 전적 담당 라우팅 모듈 시스템화 방식 고속 스위칭 처리 최적 관리 기능) 
772. PCF (Policy Control Function 사용자 정책 적용 자원 대조 통제 구조 연동 통합 기능 기능망 제어 분산 룰 구조 통제 프로비저닝 데이터베이스)  
773. 네트워크 슬라이싱 (Network Slicing 물리적 동일망 복수의 이종 독립 논리적 인스턴스 전용망 분할 보안, QoS 격리(eMBB/URLLC/mMTC) 관리 지원 클라우드 자원 할당 제로 트러스트 자원 관리 제어 체계 자동화 SDN/NFV 필수 적용 기술 망)
774. E2E 슬라이싱 보장 모델 관리 (RAN-Transport-Core 종단 통과 자원 보장 체계 통제 연동 규격 파싱 자원 논리 분배 제어 구성 구조 모델 개념 기술 요약망 적용/배포 방침)  
775. MEC 기반 가속 통신망 라우팅 최적 (User Plane Function UPF 로컬 엣지 트래픽 인터셉트 전환 백홀 지연 개선 구조) 로컬 지연 대책 서버형 응용 처리망 체계 기술 연계)
776. Massive MIMO 대거 다중 배열 안테나 시스템 고주파 전파 빔 관리
777. 빔포밍 트래킹 기술 체계 (Beam Tracking 개별 단말 핀포인트 추적 지향 전력량 최적화 증폭/간섭억제 타겟 통신 품질 체계 극대화 송수신망 진화 시스템 단말 수신 추정기반) 
778. 3D MIMO 수직/수평 고차원 송수신 구조 공간 활용 극대화 스펙트럼 자원)
779. BSS Coloring (간섭 채널 색상 코드 배정 구분 노이즈 신호 차단 무선 채널 활용 체계 고밀도 효율화 기능망 확장 연대 와이파이 혼선 배제 방식 응용 구조 체제) 
780. CP-OFDM (5G 표준 데이터 채널 다중 변조 다운 무선통신 파형 방식 적용 분석망 통신망 채택 사양 모델 파형) 
781. C-RAN (Cloud RAN 베이스밴드 Unit 원격 중앙 풀링 클라우드 관리 프론트홀 망 구조 통제 트래픽 통합 제어 기술 구성 요소망 구축 방법 구조 효율 제어) 
782. O-RAN (Open RAN 기지국 장비 인터페이스 화웨이 등 벤더 종속성 탈피 개방형 오픈 API 표준 분할 조합 기술 화이트 박스 스위치 구성 통제망 자립 기지국 연합 관리 기능 체계 연계) 
783. 기지국 DU (Distributed Unit) / CU (Centralized Unit) / RU (Radio Unit 전파 안테나 제어망 연결 구조) 고차원 장비 표준화 인터페이스 (스플릿 옵션망 트래픽 부담 체계 프론트홀 지연 파급망 분석 분산)  
784. 프론트홀 (Fronthaul 안테나-DU망 광인터페이스 eCPRI 규격 모델 구조 구성 패킷망 확장망) 
785. 미드홀/백홀 전송계층망 코어 장거리 파장 라우터 스위치 연합망 구성체계 요약 진화) 
786. 6G 비전 네트워크 커버리지 입체망 스펙트럼 주파수 광대역 (테라헤르쯔 THz 위성 연계망 무지연 대역 확장 구성 기술 예상 지표 모델 기준 규제 표준안 도입 적용 한계 이슈) 
787. 지능형 반사 표면 (RIS 기능 구조 메타 파트너 물질 적용 주파수 흡수/조절 우회 반사/투과 경로 조작 커버리지 음영 극복 저전력 반사/전파제어 혁신 시스템 모델 빔포밍 한계 돌파형 구성망 보조 안테나 환경 연계 연구 동향)
788. 비지상 네트워크망 (NTN Non-Terrestrial Network. 스타링크 연계 도심 항공 모빌리티 UAM 커버 위성 3D 연계 라우팅 끊김 보완/위성 안테나 최적화망 구성 기술 발전/해상 통합 통신 지원 기반 연구 궤도 지연 최적 방침 구조적 구성) 
789. 디지털 트윈 네트워크 망 (AI 동기 시뮬레이션 고장 예측 자가 치유 망 인공지능 접목 선행 관측 모형 모델 도입 구성 개념 도입) 
790. 네트워크 프로그래밍 모델 P4 지원 고정 하드웨어 규격 ASIC 탈피 자율망 라우팅 룰 적용 최적 커스텀 프로세싱 (초저지연 라우팅 룰 설정 엔진 고도화 기술 적용 연계 모델 개요)  
791. 자율 주행 넷망 (AIOps, AI for Network 통제망 유지보수 자동화 의도 반영 정책 IBN 설계 융합 6G 통합 자력 제어 제로 터치 네트워크 구현 모델)
792. AI 내재화 (AI-Native) 6G 통신 신호 변복조 채널 추정 물리망 대체 신경망 라디오 적용 모형 진화 기술 통신 딥러닝 디코더 채택 모델 성능/오버헤드 한계 극복 대안 통신 기술 
793. 양자 인터넷 모듈 기반 네트워크 키 분배 안정성 QKD 적용 (양자 얽힘/복제 불가능 원리 광파장 탑재 보안 구간 해킹 원천 차단 무선 통신 기기망 연동 체계 구조 방식 인텔 암호 보장 릴레이망 구축)  
794. 프라이빗 5G망 (특화망 e-UM 5G 개념 적용 산업 공장 자체 구축망 라이센스 주파수 사설 구성망 비용 구조 보안 지연 한계 탈피망 맞춤형 슬라이스 대안 구조 모델 요약 정리)
795. 5G LAN 스위치 대체 이더넷 투명 연계형 산업망 구축용 모델 브릿지 구성 기술 (L2 무결 연동 통신망 호환 제어망 융합 구성 요지 모델망 구성망 프로비저닝 구조 체계 정리) 
796. 홀로그램 무선 전송 압축/다시점 비디오 체계 동기망 지터 제어 기술(VTC 지연 민감 체계) 통신망 요구 지표 한계 모델 구조 모델 도입 요망 기술 요소)
797. 텔레햅틱 체계 기술 네트워크 응답 시간/제어 피드백 (Tactile Internet 극한 응답 한계 분석 및 신뢰 통신 5ms 이내 물리 제어 데이터 패킷 순서 보장 모델 통신 기반 연계 인프라 방식 구성 기초 체재) 
798. 메이커 빔 생성 안테나 메타 표면 적용 무전원 IoT 환경 센서 연계 통신 시스템 구조 파악 설계 통신 방향 제안 
799. 동적 스펙트럼 공유 기술 (DSS 진화 4G/5G 주파수 시간 단위 혼용 운영 자원 배분 유연성 통신 기술 방식 도입 전파 배급 한계 돌파 통계망 모델)  
800. 주파수 집성 기술 고급 모델 연대 전방위 고밀도 셀 간 간섭 회피 CoMP(상호협력 통신 체계 전파 최적화 망) 

## 16. 데이터센터 및 클라우드 네트워킹 (50개)
801. 데이터센터 (Data Center) 3-Tier 아키텍처 - Core, Aggregation, Access 계층 
802. 데이터센터 Spine-Leaf 아키텍처 - 2-Tier 수평 분산 구조 (East-West 트래픽 최적화)
803. 오버서브스크립션 비율 (Oversubscription Ratio) 설계 개념 분산망 대역
804. ECMP (Equal-Cost Multi-Path) 스파인-리프 병렬 라우팅 경로 활성화 
805. Clos 네트워크 - 다단 논블로킹(Non-blocking) 스위칭 구조
806. North-South 트래픽 (외부 사용자-데이터센터간 흐름)
807. East-West 트래픽 (데이터센터 내부 서버-서버/마이크로서비스 간 가상 통신 흐름)
808. 네트워크 지터 (Jitter, 지연 변이) 데이터센터 스토리지 망 동기 치명적 영향 대안
809. FCoE (Fibre Channel over Ethernet) - SAN과 이더넷 랜망 통합 물리선 단일화 (스토리지 네트워킹)
810. iSCSI (Internet Small Computer System Interface) - IP망 기반 스토리지 블록 전송 통신망 표준
811. 인피니밴드 (InfiniBand) - RDMA 기반 초고속, 초저지연 컴퓨터 클러스터 인터커넥트망 (HPC, AI 클러스터 망)
812. RDMA (Remote Direct Memory Access) - CPU 개입/OS 커널 스택 복사 없이 메모리간 직접 데이터 전송망 기법
813. RoCE (RDMA over Converged Ethernet) - 이더넷 환경에서 RDMA 구현 
814. iWARP - TCP/IP 기반의 RDMA 구현 망 호환성 중시 프로토콜 단
815. 오버레이 네트워크 (Overlay Network) 논리 스위치 L2 확장 터널 구조 터널링
816. 언더레이 네트워크 (Underlay Network) 오버레이 터널을 품는 물리 망 패킷 포워딩 베이스
817. VXLAN (Virtual eXtensible LAN) - UDP(포트 4789)로 L2 프레임 캡슐화, VLAN 4096개 한계 완화 (1,600만개 VNI 지원) 
818. NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계
819. STT (Stateless Transport Tunneling) 가상화 망 패킷 오프로드 LSO 지원 목적 망
820. EVPN (Ethernet VPN) - BGP 제어 평면 기반 L2/L3 오버레이 경로, MAC/IP 동적 학습 및 ARP 브로드캐스트 억제 기술 체계 (VXLAN 결합)
821. 클라우드 네이티브 네트워킹 (Cloud Native Networking 개념) 스케일아웃 분산 연동
822. 컨테이너 네트워킹 인터페이스 (CNI, Container Network Interface) 쿠버네티스 망 포드간 생태계 표준
823. Flannel - 오버레이 단순 구현체 CNI 플러그인
824. Calico - BGP 라우팅 기반 고성능/보안 L3 CNI 네트워크 구현 플러그인
825. Cilium - eBPF(지정 커널 동작 제어) 기반 고성능 클라우드 네트워크 연결, 로드밸런싱, 보안 검증 네트워크 프레임워크 
826. Kube-Proxy 쿠버네티스 서비스 트래픽 부하 분산 룰 생성 (iptables/IPVS 모드) 구조
827. Ingress / Egress 트래픽 (클러스터 내부 망 인입/통과 유출 라우팅 룰 엔진 제어망 설정)
828. 서비스 메시 (Service Mesh) - 마이크로서비스 간의 통신/보안/모니터링을 인프라 계층으로 추상화
829. Istio (이스티오) - Envoy 사이드카 프록시 기반 서비스 메시 표준 컨트롤 플레인 엔진 
830. 사이드카 (Sidecar Proxy) 아키텍처 - 애플리케이션 코드 변경 없이 트래픽 제어 대행 캡슐화 모델
831. mTLS (Mutual TLS, 상호 인증 TLS) 마이크로서비스 간 신뢰 통신 양방향 자격 구조 증명 체계 보장망 설정
832. 트래픽 섀도잉 (Traffic Shadowing) 및 카나리 배포 네트워킹 라우팅 전략 (가치 테스트망) 분배 제어
833. 로드 밸런싱 (Load Balancing L4/L7 방식 트래픽 폭주 대안 스위치 분산망 적용 구조) 
834. 라운드 로빈 (RR, Round Robin, Least Connection 연결 추정 부하 맵 할당) 
835. DSR (Direct Server Return) - 로드밸런서 부하 경감 위해 응답 패킷은 서버가 클라이언트로 직배송 비대칭 트래픽망
836. VPC (Virtual Private Cloud) - 퍼블릭 클라우드 내 격리된 가상 사설 통신망 구조체계
837. 클라우드 서브넷 라우팅, 인터넷 게이트웨이, NAT 게이트웨이 개념 분리 대역 구조망 설계
838. Direct Connect / ExpressRoute - 전용선 클라우드 직접 연계망 라우팅 고가용성 하이브리드 연결
839. 퍼블릭/프라이빗/하이브리드/멀티 클라우드간 백본망 인터커넥트 연결 구성 라우팅 정책
840. BDI (Bridge Domain Interface) / VTEP (VXLAN Tunnel End Point 터널 장치 구조 논리 분배 포트 스위치 모듈 기능 체계 분석)
841. BUM 트래픽 (Broadcast, Unknown Unicast, Multicast 스파인리프망 홍수 해소 분배 멀티캐스트 패킷 체계 관리 방식 설계)
842. 마이크로 터스트 존 방화벽 보안 적용 체계 클라우드 구성 기술 템플릿 배포망
843. 하둡(Hadoop) 랙 인식 (Rack Awareness) 토폴로지 통신 데이터 복제 연계 전략
844. 가상머신 (VM) 하이퍼바이저 가상 스위치 (vSwitch) 구조 병목 한계 패킷 경로 탐색 기술 방식
845. 무손실 이더넷 (Lossless Ethernet, 스토리지/AI 망 PFC 적용 대역폭 지연 관리 망 구성)
846. DPDK (Data Plane Development Kit) 커널 우회 사용자 공간 고속 패킷 처리 구조 모델 인터럽트 프리 폴링
847. SR-IOV (Single Root I/O Virtualization 인터페이스망 가상머신 다이렉트 패스스루 통과 구성 PCIe 하드웨어 망) 
848. 스마트NIC (SmartNIC) / DPU (Data Processing Unit 인프라 가속망 컨트롤러 CPU 연산 오프로딩 구조 카드 모델 분석 체계)
849. SD-WAN 가속 오버레이 토폴로지 암호망/다중경로 최적 클라우드 연결 지능 라우팅 통합 게이트웨이 기술 (차세대 지점망 인프라)

## 17. 소프트웨어 정의 네트워킹(SDN) 및 네트워크 가상화(NFV) (40개)
850. SDN (Software Defined Networking 소프트웨어 정의 네트워크 구조 패러다임 특징 제어/데이터 영역 근본 분리)
851. SDN 데이터 평면 (Data Plane = 포워딩 평면 단순 파이프 라인 패킷 스위치 수행 역할/ASIC 라우터 이관)
852. SDN 제어 평면 (Control Plane 관리망 정책 룰 라우팅 시야 중앙 논리 통제 아키텍처) 두뇌 격 구조 
853. 사우스바운드 인터페이스 (Southbound API) - 컨트롤러와 데이터 스위치 간 명령 규약 
854. 노스바운드 인터페이스 (Northbound API) - 컨트롤러와 응용(보안, QoS) 애플리케이션 간 통신/API 연동 규약 
855. OpenFlow (오픈 플로우 표준 프로토콜 사우스바운드 근간) SDN 1세대 표준 규격 
856. OpenFlow Flow Table (매치 필드, 액션, 통계 수집기 엔트리 파싱 테이블 패치 구조 규정) 
857. 인텐트 기반 네트워킹 (IBN, Intent-Based Networking 의도 서술형 정책 번역 인공지능 기반 컨트롤러 자동 변환 설정망 검증 모델 구성)
858. SDDC (Software Defined Data Center 클라우드 인프라 자산망 컴퓨트/스토리지/네트워크 전체 추상 풀링 동적 관리 플랫폼 결합)
859. 화이트박스 스위치 (Whitebox Switch 범용 x86 하드웨어 + 개방형 네트워크 OS 펌웨어 탑재 제어 모델 NOS 이식 벤더 종속 한계 극복 적용 체계) 
860. OVS (Open vSwitch 가상 스위칭 리눅스 커널 기반 오픈소스망 VM/컨테이너 포트 트래픽 OpenFlow 제어 통과 인터페이스 모델 활용) 
861. 미니넷 (Mininet) SDN 토폴로지 에뮬레이터 연구 평가망 시뮬레이션 환경 (버추얼 환경 제어 체계 분석망 생성 구조)
862. ONOS / OpenDaylight (오픈소스 SDN 컨트롤러 생태계 아키텍처 대형망 서비스 제공자 구조 분산 설계 특징 비교 분석 코어 모델) 
863. SDN 컨트롤러 스플릿 브레인 방어 및 분산 클러스터 고가용성 제어기 (컨트롤 평면 이중화 트래픽 분할 모델 정책망 보호 구상 체계 대응 방침)
864. 네트워크 슬라이스 오케스트레이터 중앙 논리 관리 제어기 배포 연동 SDN 접목 아젠다
865. NFV (Network Functions Virtualization 네트워크 기능 가상화 통신사(ETSI) 주도 아키텍처 전환 장비 소프트웨어 이식 기술 구조 망)
866. VNF (Virtual Network Function 라우터, 방화벽, EPC 등 범용 서버 가상 논리 인스턴스/어플리케이션 동작 구성 소프트웨어 패치 모델)
867. NFVI (NFV 인프라 컴퓨팅, 스토리지, 네트워킹 구성 물리+가상 자원 연동 자산 모델 개념적 하드 환경 제어) 
868. MANO (Management and Orchestration 오케스트레이션 자동 관리 프레임워크 3단계 분할 요소 통제 망) 
869. NFVO (NFV Orchestrator 종단간 네트워크 서비스 라이프사이클 VNF 체인 리소스 총괄 할당 통제기 설계 지휘망 기능) 
870. VNFM (VNF Manager 개별 VNF 인스턴스 프로비저닝, 스케일 업다운/에러 복제 상태 관리 체제 역할망 인프라 적용 구조)  
871. VIM (Virtualised Infrastructure Manager - OpenStack/K8S 등 자원 파편화 할당 VM 배포 생명 주기 통지 자산 플랫폼 하드 할당 기능망 통제)
872. 서비스 체이닝 (Service Chaining / SFC - Service Function Chaining 트래픽 패킷 순차적 방화벽->IPS->LB 식 가상 함수 통과 라우팅 NSH 활용망 체계화)
873. NSH (Network Service Header 패킷 경로 체인 메타데이터 포워딩 명세 인캡슐레이션 지원 터널 지원 규약 설정) 
874. P4 (Programming Protocol-independent Packet Processors - 데이터 평면 패킷 처리 순서 파이프라인 개발자 직접 언어 코딩 정의, 차세대 확장 SDN 구동 개념) 
875. NETCONF (Network Configuration Protocol - SSH+XML 자원망 환경 설정 통계 관리 SNMP 한계 극복 원격 설정 커밋/롤백 표준 지원망 트랜잭션 관리망) 
876. YANG (Yet Another Next Generation - NETCONF가 조작하는 장비/모듈 데이터 모델링 스키마 구조 언어 서식망 (설정 구상 타입 서식)) 
877. RESTCONF (HTTP 기반 JSON/XML 형식 NETCONF/YANG 매핑/간소화 API 통신망 설정 프로토콜 체계 모델) 
878. 오픈컨피그 (OpenConfig 구글 주도, 벤더 중립적 공통 YANG 데이터 모델망 장비 범용 설정/조작 스키마 규격 표준화 진영 구성 통신망 생태 구조) 
879. 텔레메트리 (Streaming Telemetry 장비 폴링이 아닌 자발적 푸시/스트리밍 방식 gRPC 등 초정밀 마이크로단위 빅데이터 성능 정보 중앙 컬렉터 전송망 모니터 지표 수집 기술 체계 패러다임)   
880. 오버레이 SDN과 언더레이 SDN (분할 관리 구조 제어 평면 이중성 통합망 구조 관리 차이 분석 개념 차)
881. 마이크로세그멘테이션 방화벽 SDN 접목 내부 논리 정책 룰 중앙 연동 배포 
882. 화이트박스 OCP (Open Compute Project 페이스북 발 하드웨어/스위치 규격 네트워크 개방 장비 기조망 플랫폼) 
883. SONiC (Software for Open Networking in the Cloud MS 주도 컨테이너 기반 개방형 네트워크 OS 레이어망 구성 BGP 등 통신망 앱 탑재 시스템 연동 구조망)
884. ONIE (Open Network Install Environment - 맨 하단 부트로더/운영체제 펌웨어 다운 설치 오픈망 부트 규약 모델 체계) 
885. BGP-EVPN 라우팅 컨트롤러 스파인/리프 패킷 연합망 오버레이 기술 표준화 연계 SDN 설계
886. 엣지 가상화 (vCPE 가입자 댁내 게이트웨인 통제 기능을 사업자/통신사 엣지 서버 VNF 가상화 이관 비용 최소망 트래픽) 
887. SD-LAN (캠퍼스/사무실 유무선 접속 스위치 중앙 통제형 와이파이 관리 융합 네트워크 자동 배포 SDN 진화 모델)
888. 멀티 테넌트 (Multi-Tenant 자원 격리 보안 독립망 인프라 슬라이싱 할당 SDN 환경 통제) 
889. 네트워크 펑션 오프로딩 다이렉트 처리 DPU 연동망 P4 기능 컴파일 구조 결합 지연 파급 최소 하드 이양 기술

## 18. 광/차세대 통신 및 자동화 운영 (50개)
890. 광통신 네트워크 이더넷(Optical Ethernet 단일 플랫폼망 고속 전이 통계 모델 구성)
891. 장거리 백본 해저 광케이블 아키텍처 및 증폭기 중계기 토폴로지 구조 연계
892. ASON (Automatically Switched Optical Network - 광망 자원 제어 평면 동적 설정 분산 연결 제어 ITU 표준 도입 아키텍처 모델 시스템 라우팅망 최적 동적 구성)
893. OTN (Optical Transport Network 광 데이터 포장 컨테이너 G.709 표준 프레이밍 망 장애 무결 캡슐 규격 동기화 방식 체재)
894. OAM (Operations, Administration, and Maintenance 망 이더넷 결함 링크 확인 루프 감지 폴링 오류 관리 통지 프레임 제어 모델망 구조 프로토콜 분석 기술)
895. SDH (Synchronous Digital Hierarchy 동기식 디지털 통신 위계망 STM-1, 백본 멀티플렉스 고전 프레임 구조) 
896. SONET (Synchronous Optical Networking 북미 동기식 광통신망 통신 모델/ OC 규격 프레임 오버헤드 구조망 제어 분산 링 토폴로지 생존망 결함 치유 기반) 
897. ROF (Radio over Fiber 밀리미터파 등 고주파 안테나 베이스밴드 신호 광섬유로 중앙 기지국 아날로그 파장 전달망 구조 효율화 장비 소형화 기반 연구 동향 구성망 요약 구조)
898. NG-PON2 표준 광통신 파장 동적 분할 시분할 TWDM 결합/대칭 40Gbps 가입자망 구조 확장 연계 스케일 업 망 토폴로지 적용 모델 광단말(ONT/OLT) 분리 배분 기반)
899. 다크 파이버 (Dark Fiber 상용 미사용 예비 여유 광케이블 인프라 자산망의 활용 구성 전용 회선 구축 기술 적용 규제 한도 모델링망 파악 인프라)
900. 무선 광통신 대기권 전송 FSO 기상 조건 감쇠(안개/비) 대응 라디오 백업 융합 모델 다이버시티 페이딩 극복 통제망 시스템 체계.
901. AIOps (Artificial Intelligence for IT Operations 망 자산 수만 건 텔레메트리/Syslog 인공지능 머신러닝 분석 이상 전조 통보 자가 치유 자동 네트워크 운영 인프라망 관제(Observability) 시스템 전환)
902. 자율-구동 네트워크 (Autonomous Driving Network, ADN 무개입 레벨 별 0~5망 트래픽 AI 지능형 최적 라우팅/침해 자동 결단 차단 통제 룰 분산 적용망 시스템 설계 철학)
903. 디지털 트윈 네트워크 실시간 토폴로지 동기 트래픽 시뮬레이션 영향도/병목 사전 검증망 인프라 연계 메타 공간 결합 통신 검토 망 적용 체계
904. 퍼시스턴트 토폴로지 관리 (동적 장비/컨테이너 프로비저닝 추적 자산 매핑 그래프 DB 저장 기반 가시성 확보망 시스템 구현 원리)
905. 멀티캐스트 오디오/비디오 스트리밍 프로토콜 (HLS HTTP Live Streaming) 세그먼트 단편 파일 분할 + M3U8 인덱스 파일 전송 해상도 대역폭 자동 적응 스트리밍 기술
906. CMAF (Common Media Application Format DASH/HLS 파편화 인코딩 단일 미디어 컨테이너 포맷 규격화 통일 지연 단축 기술 인프라 규정)
907. 화상 회의 지터 버퍼 (Jitter Buffer 패킷 도달 시간편차 무작위성 완충 재생 지연 최신 동기화 체계망 오디오 왜곡 관리 기술망 트러블슈팅 해법) 
908. FEC 실시간 비디오 손실 은닉 기법 미디어 품질 보상 (에러 패킷 무시 보간 재생 보정망 통신 대역 폭증 대비 잉여 비트 기술 적용망 제어 모델 통신 기초)
909. MOS (Mean Opinion Score 음성/영상 체감 품질 사용자 5점 척도 측정 통신망 평가 주관식 및 E-Model 알고리즘 평가 체제 규약)
910. 네트워크 코딩 (Network Coding 중간 노드가 패킷 스토어 앤 포워드가 아닌 대수적 연산 병합/조합 전송 대역폭 절감 신뢰도 향상 분산 통신 기법 수학 모델 원리 개념) 
911. 에지 보안 SASE 진화 모델 SSE (Security Service Edge 네트워킹 라우팅 배제 클라우드 순수 보안 검증 엣지 통제 모델 프레임웍) 적용 플랫폼)
912. IPFS (InterPlanetary File System 콘텐츠 주소 지정 영구 분산 P2P 해시 기반 웹 스토리지 프로토콜 파일 망 탈중앙 분산망 구성 기술 요지 HTTP 위치 지정 대체망 구조 분석 원리망)
913. V2I 노변 기지국 RSU 교통 관제 시스템 인프라망 MEC 배치 자율협력주행 오프맵 다운 지연망 극복 패러다임 로컬 통신 반경 지연) 
914. 철도 통신망 LTE-R (PS-LTE 기반 고속철도 특화 관제망 QPP 재난망 우선 순위 제어 터널링 오버랩 구성망 생존 시스템 적용 이중 링 기반 네트워크 스위치 통신 토폴로지 구축망)
915. 해상 통신망 LTE-M / e-Navigation 인프라 대역폭 전파 초고주파 해수면 반사 (다중경로) 채널 무선 구간 간섭 대응망 설계 모델 선박 통신) 
916. P2P (Peer-to-Peer) 네트워킹 (하이브리드, 순수 P2P, 슈퍼 노드 개념 스카이프/토렌트 트래커 해시 분배 매칭 비집중망 탐색 알고리즘 Gnutella 망 프로토콜 구성 통제망)
917. 비트토렌트 (BitTorrent) 초크/언초크 리치 통신 대역폭 인센티브 알고리즘망 파편화 전송 구성/다운 최적 효율망 동적 탐색 구조)
918. 블록체인 네트워크 계층 가십 프로토콜 (Gossip Protocol 플러딩 전파망 병목 회피 이웃 랜덤 메시지 전파 무작위 분산형 노드 동기화 상태 머신 통신 메커니즘 구축 개념 원리)
919. DLT (Distributed Ledger Technology 노드 간 분산망 데이터 브로드캐스트 합의 컨센서스 패킷 검증 동기 트래픽 부하망 처리 병목 지연 문제 파급 관리 기술 시스템 기반 모델)
920. 스마트 컨트랙트 분산망 오라클 (Oracle 외부 오프체인 데이터 API 인터넷 연동 진실성 보장 서명 데이터망 접목 통신 체계 신뢰 취약 모델 극복 구성 체제 검토)
921. 양자 중계기 (Quantum Repeater 노-클로닝 복제 불가 양자 얽힘 텔레포트 통신 장거리 확산 릴레이 시스템 구현 한계 모델 기술 기초 원리 요약) 
922. QKD (Quantum Key Distribution) 프로토콜 (BB84 송수신 편광 빔 측정 스니핑 노출 파동 붕괴 탐지 보안 체계 개념망 인프라 구성 한계 암호 분배 융합 전용선 적용 구조 분석) 
923. 시맨틱 통신 망 (Semantic Communication 단순 비트 전달 섀논 통신 넘어서 의미/맥락 AI 추출/전달 압축 복원 대역 절감 패러다임 6G 응용 연구 목적 시스템) 
924. 메타버스 네트워크 대역/QoS 렌더링 오프로드 분산 처리 동기 통신망 공간 식별 데이터 통신 프로토콜 요구 스펙 지표 동향망 적용)
925. 오픈API 클라우드 망 연동 / MaaS (Mobility as a Service 통신망 객체 분산망 연계 라우팅 데이터 통합 통신 처리) 
926. 지향성 안테나 MAC 계층 노출/은닉 망 탐색 알고리즘 무선망 방향 제어 최적화 스위프 전파 관리 체계 기술 통제 모델 진화 
927. 스마트 헬스케어 BAN (Body Area Network 무선 인체 통신망 WBAN 보안 인가 전력 최소망 구성 흡수율 대응 전파 송신 제어 통계 모델 망 구성 기초 보안 설계 개념 탑재) 
928. 수중 통신 무선 음파(Acoustic) 다중경로 반사 지연 한계 OFDM 적용 UWSN (Underwater Sensor Network 전파 도달 손실 통체 주파수 대안 설계 채널망 적용 프로토콜 분산 기술)
929. 지중 통신(Underground Radio / MI 자기유도 통신 토양 수분 손실 저주파 전파 터널망 IoT 붕괴 통지 시스템 결합망 구성)
930. 재난 통신망 (PS-LTE MCPTT 미션 크리티컬 푸시투톡 단말 개입 고속 통제 무선망 복구 기지국 애드혹 망 생존 체계 오버레이 구축 연대망 모델 통신 시스템 지표 보장망)
931. EMP (전자기 펄스 방호 케이블 광망 쉴딩 시스템 패러데이 케이지 네트워크 장비 물리적 안전 보호 시설 지침 템플릿 파악 절연 구성)
932. 스니핑 탐지 - ARP 핑(Ping) 테스트 네트워크 지연 감지 (Promiscuous 모드 응답성 시간차 망 분석 진단 통제 통신 구조 확인 체제 도구 기초)
933. 패킷 단편화 오프셋 중첩 검증 룰 방화벽 모니터 (비정상 IDS 시그니처 연동 패턴 매치 PCAP 망 추출 페이로드 파싱 정규표현 구조 모델 설계망 원리 지표)  
934. 라우팅 프로토콜 인증 방어망 MD5/SHA 인증 해시 키 연동 BGP TCP 세션 탈취 방지 RST 스푸핑 우회 라우터 연계 BCP(Best Current Practice) 설정 보안 모델 
935. RPKI (Resource Public Key Infrastructure - BGP 스푸핑/BGP 하이재킹 경로 위조 공격 차단 인터넷 라우팅 테이블 서명/인증서 기반 인가 검증 라우팅 결함 예방 라우팅망 안전 표준 체계 인프라 기술 모델 분석 설계)
936. DNS 싱크홀 (Zombie PC 봇넷 C&C 서버 질의 블랙리스트 감지/경로 우회 KISA 차단 연계 악성 도메인 룩업망 접속 억제 무효화 처리 방화 정책) 
937. 하이브리드 암호 시스템 (성능과 키배포 장점 결합: 대칭키로 데이터 암호화(세션키), 대칭키를 RSA 비대칭키로 암호화 분배 통신망 전송 모델 SSL/PGP 기본 원리 기초 개념 정리 체계 비교 모델망 특성)
938. 파일 카빙 (File Carving 네트워크 포렌식 덤프 이진 PCAP 시그니처 획득 페이로드 헤더/푸터 복구 멀웨어 캡슐 파싱 통신 재구성 분석 기술 모델 보안 관제 기초 툴킷 활용 방식망 적용)
939. 포니팟 (Honeypot) 허니넷(Honeynet) 유인 분리망 분석 시스템 / 사이버 기만 기술 (Deception Technology, 동적 가짜 자산/호스트 할당 공격 표적 교란망 대응 시스템 지능 체계 통제 모델화)

## 19. 통신/네트워크 시험 빈출 및 토픽 단어 (60개)
940. 기저대역(Baseband) 선로 부호 (RZ, NRZ, 맨체스터 등) 
941. 샤논-하틀리(Shannon-Hartley) 
942. 에일리어싱 (Aliasing) 
943. 펄스부호변조 (PCM) 
944. 다중화기 (MUX) / 역다중화기 (DEMUX)
945. 직교주파수분할다중접속 (OFDMA) 
946. FDM 가드 밴드 (Guard Band)
947. OFDM 사이클릭 프리픽스 (Cyclic Prefix, CP)
948. 해밍 거리 (Hamming Distance) 
949. 자동 재전송 요구 (ARQ) 선택적/GBN
950. HDLC 비트 스터핑 (Bit Stuffing)
951. 반송파 감지 다중 접속 및 충돌 검출 (CSMA/CD)
952. 은닉 단말 (Hidden Terminal) 문제 (CSMA/CA RTS/CTS) 
953. 매체 접근 제어 (MAC)
954. 확산 스펙트럼 (Spread Spectrum)
955. FHSS (주파수 도약) 
956. DSSS (직접 확산)
957. 코드 분할 다중 접속 (CDMA)
958. VLAN 트렁킹 (IEEE 802.1Q 태그)
959. 스패닝 트리 
960. 루프 어보이던스 (STP 적용)
961. OSPF 링크 상태 데이터베이스 (LSDB)
962. BGP AS-Path
963. 서브넷 마스크 (Subnet Mask) / CIDR
964. IPv6 헤더 압축 / SLAAC
965. NAT 횡단 (NAT Traversal)
966. 멀티캐스트 (IGMP, PIM)
967. TCP 슬라이딩 윈도우 
968. TCP 쓰리웨이 핸드셰이크
969. 혼잡 윈도우 (Congestion Window)
970. 슬로우 스타트 (Slow Start)
971. 홀오브라인 블로킹 (HOL Blocking)
972. QUIC (0-RTT 핸드셰이크)
973. HTTP/2 멀티플렉싱 
974. RESTful API
975. 웹소켓 (WebSocket)
976. DNS 스푸핑
977. DHCP 릴레이 에이전트
978. SNMP MIB 구조
979. IPSec 터널/수송 모드 
980. AH (Authentication Header) 
981. ESP (Encapsulating Security Payload)
982. SSL/TLS 핸드셰이크
983. VPN (가상 사설망)
984. PKI 공개키 인프라
985. X.509 인증서
986. 대칭키 / 비대칭키 구조 비교 
987. 해시 함수 
988. 전자 서명
989. 서비스 거부 공격 (DoS)
990. 봇넷 (Botnet) C&C 
991. ARP 스푸핑 
992. 방화벽 (Stateful Inspection)
993. WAF (웹 방화벽)
994. IDS / IPS 탐지 차단율 
995. 네트워크 슬라이싱 
996. NFV 기반 가상화 VNF
997. SDN 데이터/컨트롤 플레인
998. OpenFlow 프로토콜 
999. MEC (모바일 엣지 컴퓨팅)
1000. 클라우드 네이티브 네트워크 (CNI)

## 20. 네트워크 성능 평가 및 심화/기타 실무 용어 (200개 요약집)
1001. QoS / QoE 차이 비교 
1002. 네트워크 지연 (Rtt vs 단방향 Delay) 
1003. 처리량 (Throughput) 수식화
1004. Erlang (얼랑, 통신 트래픽 부하 단위량)
1005. 호손율 / 블로킹 확률 (Blocking Probability)
1006. 망 신뢰도 (네트워크 토폴로지 연결도 계산법) 
1007. MTBF (평균 무고장 시간) 통신망 생존성
1008. MTTR (평균 수리 시간) 회선 이중화
1009. 백홀 (Backhaul) 
1010. 미드홀 (Midhaul) 
1011. 프론트홀 (Fronthaul) 
1012. 셀 엣지 수율 (Cell Edge Throughput)
1013. CoMP (협력 통신) 
1014. 캐리어 어그리게이션 (CA) 
1015. 언면허 대역망 (Unlicensed Band LTE-U / NR-U) 
1016. LAA (Licensed Assisted Access)
1017. 와이파이 오프로딩
1018. 밀리미터파 (mmWave) 전파 감쇠
1019. 테라헤르츠 (THz) 대역 
1020. 자유 공간 광통신 (FSO)
1021. 가시광 통신 (VLC) 라이파이 (Li-Fi)
1022. 저궤도 위성망 스타링크 
1023. 위성 통신 핸드오버 (ISL - Inter-Satellite Link) 
1024. V2X (차량사물 연결) 
1025. C-V2X / WAVE (DSRC) 매체 제어 
1026. 스마트 그리드 통신 인프라망
1027. 수중 음파 통신망
1028. 체내 통신 (WBAN)
1029. LPWAN 로라 (LoRa)
1030. 시그폭스 (SigFox) 협대역 통신
1031. NB-IoT 전력 최적화 (PSM/eDRX)
1032. 블루투스 LE (BLE)
1033. 지그비 (Zigbee) 메쉬
1034. NFC 표준 (13.56MHz) 
1035. RFID 충돌 방지 알고리즘 (알로하 기반) 
1036. EPCglobal 망 아키텍처
1037. ONS (Object Name Service) 구조
1038. MQTT 퍼블리시 서브스크라이브 모드
1039. CoAP 프로토콜 및 REST 인터페이스
1040. Thread / Matter (스마트홈) 표준 망 
1041. SD-WAN 중앙 정책 관리형 브랜치
1042. SASE 네트워킹/보안 융합 클라우드
1043. 제로 트러스트 구조
1044. 마이크로 세그멘테이션
1045. eBPF 커널 네트워킹 후킹 시스템
1046. P4 네트워크 프로그래밍 모델 플로우 
1047. 타임 센시티브 네트워킹 (TSN 인프라망) 
1048. IEEE 1588 PTP 시각 동기망
1049. NTP / GPS 동기화 
1050. RDMA / RoCE 스토리지 서버 네트워킹
1051. VXLAN 오버레이 VTEP 터널링 연결기법
1052. EVPN-VXLAN BGP 컨트롤 플레인 전이
1053. Spine-Leaf 대용량 클로스 구조
1054. IBN(의도기반망) 선행 AI 설계 
1055. 화이트박스 OCP 스위치
1056. ONOS / OpenDaylight 구조 모델 비교 
1057. NETCONF / YANG 모델링 규격체 
1058. 트래픽 텔레메트리 (Streaming Telemetry) 
1059. 디지털 트윈 및 관제 시스템 연동 
1060. 양자 암호 키 분배 (QKD 인프라 기반망)
1061. BGP RPKI 라우팅 보안 망 
1062. DNSSEC 존 
1063. DoH / DoT (웹/전송 보안 계층 DNS 암호화)
1064. ESNI (TLS 1.3 평문 노출 보안)
1065. HTTP/3 QUIC 혼잡 윈도우 이식
1066. 마이크로서비스 서비스 메시 패싱
1067. 이스티오(Istio) 사이드카 프록시
1068. gRPC / 프로토콜 버퍼 직렬화 
1069. WebRTC NAT 횡단 (STUN/TURN/ICE 통합)
1070. CDN 엣지 노드 분산 
1071. GSLB 지리적 DNS 라우팅 
1072. SIP INVITE 기반 핸드셰이크
1073. IP PBX 멀티캐스트
1074. IPv6 SLAAC 자동할당
1075. 멀티캐스트 MLD / IGMP 스누핑 기법
1076. ARP 스푸핑 중간자 방어 (동적 검사 체계)
1077. DDoS 반사 증폭 원조 (NTP, DNS 포트망) 
1078. 클라우스 보안 워크로드 CWPP 통제망 
1079. 망분리 논리적 / 물리적 VDI 전이 모델 
1080. 네트워크 포렌식 패킷 덤프 파싱
1081. IPS 시그니처 정규식 
1082. 웹쉘 탐지 프로토콜 파서
1083. 블록체인 가십 프로토콜 P2P 연결 
1084. 다크 웹 Tor 통신 프로토콜 암호화층 
1085. IPsec IKEv2 터널 협상
1086. WireGuard 라우팅 고속망 체계 
1087. BBR 구글 TCP 동적 모델 지연 기반 혼잡 
1088. ECN 징후 큐 통지 
1089. DiffServ DSCP 분류 PHB
1090. RSVP 자원 예약 플로우
1091. GRE 일반 캡슐화 포맷 오버헤드 
1092. DMVPN 동적 라우팅 결합형 지점 
1093. MPLS VPN L3 경로 격리 라벨 스위치
1094. OSPF ABR / ASBR Area 위계 분산망 
1095. BGP 속성 (Local Pref, MED, AS-path 구성비)
1096. EIGRP DUAL 지연 스케일 분산
1097. 브로드캐스트 스톰 (루프 발생)
1098. LACP 이더채널 포트 논리 그룹화
1099. VLAN 간 라우팅 
1100. 스위치 포트 미러링 (SPAN/TAP)
1101. UTP 배선 카테고리
1102. 광섬유 싱글모드 다중모드 
1103. WDM 무손실 광 증폭 
1104. O-RAN 프론트홀 개방 사양 
1105. vCPE NFV 고객 구내 망 통합 전환 
1106. 마이크로그리드 통신 규격
1107. 산업용 이더넷 PROFINET 망 
1108. OT 망 (운영 기술 망) 분리 원단 통제
1109. OPC UA 자동화 프레임 표준 통신
1110. 무손실 이더넷 (PFC 체제) 
1111. DPDK 패킷 바이패스 
1112. 스마트NIC 가속 오프로딩 시스템 
1113. 5G SA/NSA 아키텍처 비교망
1114. 스몰 셀 조밀화 간섭 통제망
1115. Massive MIMO 빔 관리 시스템 
1116. 자율 구동 네트워크 레벨링 
1117. 네트워크 보안 (Zero Trust 정책) 
1118. 정보통신 기술사 최근 기출 토픽 기반
1119. 6G 융합 테라헤르츠 예측 지표망
1120. 위성 기반 도심항공교통(UAM) 라우팅 통신 구조 모델

---
**총정리 네트워크 키워드 : 총 1,120개 수록** (+관련 항목 파생 개념 수련시 약 1,500개 커버 가능)
(네트워크 기초, 심화, 보안, 최신 클라우드 및 통신 아키텍처 전반을 심도있게 다룬 완전판입니다.)
