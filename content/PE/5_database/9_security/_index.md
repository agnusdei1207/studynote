+++
title = "데이터베이스 보안 및 거버넌스"
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-database"
+++

# 데이터베이스 보안 및 거버넌스

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터베이스 보안은 기밀성(Confidentiality), 무결성(Integrity), 가용성(Availability)을 보장하기 위해 접근 통제, 암호화, 감사 추적 등 다층적 방어 체계를 구축하는 것이다.
> 2. **가치**: TDE(Transparent Data Encryption), 컬럼 암호화, 데이터 마스킹 등의 기술로 민감 정보를 보호하고, SQL 인젝션 방어와 DB 방화벽으로 외부 공격을 차단한다.
> 3. **융합**: 데이터 거버넌스, 메타데이터 관리, 데이터 리니지 추적은 규제 대응(ISMS, GDPR)과 데이터 품질 관리의 핵심 요소이며, DataOps로 파이프라인 자동화를 실현한다.

---

### 학습 키워드 목록

#### 데이터 암호화
- TDE (Transparent Data Encryption) - 휴지 상태 암호화
- 컬럼 레벨 암호화
- FPE (Format Preserving Encryption)
- 동형 암호 (Homomorphic Encryption)

#### 접근 통제 및 감사
- DB 방화벽 - SQL 인젝션 차단
- 접근 통제 정책 - IP/포트/시간 제어
- DB 감사 (Auditing) 추적 로그
- 데이터 마스킹/난독화

#### SQL 인젝션 방어
- Prepared Statement / 바인드 변수
- 파라미터화 쿼리
- 입력값 검증 및 필터링
- WAF 연동

#### 데이터 거버넌스
- 데이터 거버넌스 - 원칙, 조직, 프로세스
- 메타데이터 관리 시스템 (MMS)
- 데이터 리니지 (Data Lineage)
- 데이터 표준화
- MDM (Master Data Management)
- DataOps - 파이프라인 자동화
