+++
title = "DevSecOps - 보안 내재화 개발 방법론"
date = 2026-03-02

[extra]
categories = "pe_exam-software_engineering-methodology"
+++

# DevSecOps - 보안 내재화 개발 방법론

## 핵심 인사이트 (3줄 요약)
> **개발(Dev)·보안(Sec)·운영(Ops)을 통합**해 개발 초기부터 보안을 자동화하는 현대 SW 개발 패러다임이다. "Shift Left Security" - 보안 검사를 개발 초기(왼쪽)로 당긴다. SAST·DAST·SCA·SBOM이 핵심 도구다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: DevSecOps는 **소프트웨어 개발(Dev)·보안(Sec)·운영(Ops)을 통합하여 개발 초기부터 보안을 내재화하는 방법론**이다. "Shift Left Security" 원칙으로 보안 검증 시점을 개발 생명주기 왼쪽(초기 단계)으로 당긴다.

> 💡 **비유**: DevSecOps는 **"건축 중인 건물의 안전 검사"** 같아요. 완공 후에 소방 검사를 받는 대신, 기초 공사할 때부터 전기 배선할 때까지 계속 안전 점검을 해요. 나중에 큰 문제를 발견하면 건물을 헐어야 하니까요!

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점 - DevOps의 보안 공백**: DevOps로 배포 속도는 빨라졌지만, 보안은 여전히 출시 직전 검토. 취약점 발견 시 수정 비용 폭증 (IBM: 운영 단계는 설계 대비 100배 비용)

2. **기술적 필요성 - 공격 표면 증가**: 클라우드·컨테이너·마이크로서비스로 시스템 복잡도 급증. 수동 보안 검토 불가능, 자동화 필수

3. **시장/산업 요구 - 공급망 보안**: Log4Shell(2021), SolarWinds(2020) 등 공급망 공격으로 전 세계 타격. 오픈소스 의존성 보안 관리 시급

**핵심 목적**: **보안 취약점의 조기 발견으로 비용 절감, 빠른 배포 주기와 보안 수준 동시 확보**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **SAST** | 정적 분석, 소스 코드 스캔 | 실행 없이 코드 패턴 분석 | 설계도 검토 |
| **DAST** | 동적 분석, 실행 중 테스트 | 실제 공격 시뮬레이션 | 침입 테스트 |
| **SCA** | 오픈소스 취약점 분석 | CVE DB와 매핑 | 자재 성분 확인 |
| **SBOM** | 소프트웨어 구성 성분 목록 | 의존성 투명성 확보 | 제품 성분표 |
| **IaC 보안** | 인프라 코드 스캔 | Terraform/K8s YAML 검사 | 건축 규격 확인 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│              DevSecOps CI/CD 파이프라인                                  │
├──────┬────────┬───────┬──────────┬──────────┬────────────────────────────┤
│Plan  │ Code   │Build  │  Test    │ Release  │    Monitor                 │
├──────┼────────┼───────┼──────────┼──────────┼────────────────────────────┤
│위협  │IDE 보안│SCA    │SAST      │DAST      │런타임 보안 모니터링         │
│모델링│플러그인│(공개  │(정적     │(동적     │SIEM·SOAR                   │
│      │        │소스   │분석)     │분석)     │                            │
│      │시크릿  │취약점)│          │          │취약점 스캔                  │
│보안  │스캔    │       │IaC 보안  │침투      │(Twistlock, Falco)          │
│요구  │(Gitleaks│컨테이  │검사      │테스트    │                            │
│사항  │)       │너 스캔 │(tfscan)  │          │인시던트 대응                │
│      │        │(Trivy) │          │          │                            │
└──────┴────────┴───────┴──────────┴──────────┴────────────────────────────┘

Shift Left Security:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
계획 → 설계 → 개발 → 테스트 → 출시 → 운영
[위협│  [SCA │[SAST][DAST][침투│[런타임
모델링│  설계 │ 코드  │ 동적│ 테스트│ 보안 모니터링
     │  검토]│분석]  │분석]│      │

↑                              ↑
일찍 발견 → 수정 비용 ↓        늦게 발견 → 수정 비용 100배↑
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

핵심 도구:
SAST (Static Analysis): SonarQube, Checkmarx, Fortify
SCA (Software Composition Analysis): Snyk, OWASP Dependency Check
DAST (Dynamic Analysis): OWASP ZAP, Burp Suite
Container Security: Trivy, Clair, Twistlock
Secret Scanning: Gitleaks, TruffleHog
IaC Security: Checkov, tfsec, KICS
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 위협 모델링 → ② 코딩(시크릿 스캔) → ③ 빌드(SCA+컨테이너) → ④ 테스트(SAST+DAST) → ⑤ 배포(SBOM) → ⑥ 모니터링
```

- **1단계 (Plan - 위협 모델링)**: 설계 단계에서 잠재적 위협 식별, 보안 요구사항 정의, STRIDE/DREAD 분석
- **2단계 (Code - 시크릿 스캔)**: IDE 플러그인으로 실시간 취약점 탐지, Git pre-commit으로 API 키 하드코딩 방지
- **3단계 (Build - SCA/컨테이너)**: 오픈소스 의존성 CVE 스캔, 컨테이너 이미지 취약점 검사
- **4단계 (Test - SAST/DAST)**: 소스 코드 정적 분석, 실행 중 동적 분석, IaC 보안 검사
- **5단계 (Release - SBOM)**: 소프트웨어 구성 성분 문서화, 서명된 아티팩트 배포
- **6단계 (Monitor - 런타임 보안)**: 실시간 위협 탐지, SIEM 연동, 인시던트 대응

**핵심 알고리즘/공식**:

```
[SAST vs DAST vs SCA 비교]

┌─────────────────────────────────────────────────────────────────────┐
│                     보안 테스트 도구 비교                            │
├───────────────┬───────────────┬───────────────┬───────────────────┤
│     항목      │     SAST      │     DAST      │       SCA         │
├───────────────┼───────────────┼───────────────┼───────────────────┤
│ 분석 대상     │ 소스 코드     │ 실행 중인 앱  │ 오픈소스 의존성   │
│ 실행 여부     │ X (미실행)    │ O (실행)      │ X (미실행)        │
│ 탐지 내용     │ 코드 패턴     │ 런타임 취약점 │ 알려진 CVE        │
│ 장점          │ 초기 발견     │ 실제 공격 시뮬│ 공급망 보안       │
│ 단점          │ 오탐 많음     │ 코드 커버리지 │ 0-day 미탐지      │
│ 대표 도구     │ SonarQube     │ OWASP ZAP     │ Snyk              │
│               │ Checkmarx     │ Burp Suite    │ Black Duck        │
└───────────────┴───────────────┴───────────────┴───────────────────┘

[취약점 심각도 분류 (CVSS)]

Critical (9.0-10.0): 즉시 악용 가능, 원격 코드 실행
High (7.0-8.9): 중요 데이터 노출, 권한 상승
Medium (4.0-6.9): 제한된 영향, 사용자 개입 필요
Low (0.1-3.9): 최소 영향, 특수 조건 필요

[SBOM (Software Bill of Materials)]

소프트웨어에 포함된 모든 구성 성분 목록:
├── 직접 의존성 (Direct Dependencies)
│   ├── react@18.2.0
│   └── express@4.18.2
├── 간접 의존성 (Transitive Dependencies)
│   ├── react → loose-envify@1.4.0
│   └── express → body-parser@1.20.0
└── 취약점 매핑
    └── log4j@2.14.1 → CVE-2021-44228 (Critical)

형식: SPDX (Linux 재단), CycloneDX (OWASP)

[SLSA (Supply chain Levels for Software Artifacts)]

Level 1: 빌드 스크립트 형식화
Level 2: 서명된 출처(Provenance) 생성
Level 3: 신뢰할 수 있는 빌드 플랫폼
Level 4: 두 명 검토, 밀봉된 빌드
```

**코드 예시** (필수: Python 보안 스캐너):

```python
"""
DevSecOps 보안 스캐너 시뮬레이터
- SAST: 정적 코드 분석
- SCA: 의존성 취약점 스캔
- Secret Scanner: 하드코딩된 시크릿 탐지
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum, auto
import json

class Severity(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    INFO = 5

@dataclass
class Vulnerability:
    """취약점"""
    id: str
    name: str
    severity: Severity
    description: str
    file_path: str
    line_number: int
    recommendation: str

@dataclass
class Dependency:
    """의존성"""
    name: str
    version: str
    direct: bool = True
    vulnerabilities: List[Dict] = field(default_factory=list)

# ============================================================
# 1. SAST (Static Application Security Testing)
# ============================================================

class SASTScanner:
    """정적 코드 분석기"""

    # 취약점 패턴 정의
    VULNERABILITY_PATTERNS = {
        "SQL_INJECTION": {
            "pattern": r"(execute|exec)\s*\(\s*[\"'].*\+.*[\"']",
            "severity": Severity.CRITICAL,
            "message": "SQL 인젝션 위험: 문자열 연결로 쿼리 생성"
        },
        "XSS": {
            "pattern": r"innerHTML\s*=\s*[^\"'].*\+",
            "severity": Severity.HIGH,
            "message": "XSS 위험: 사용자 입력이 innerHTML에 직접 할당"
        },
        "HARDCODED_PASSWORD": {
            "pattern": r"(password|passwd|pwd)\s*=\s*[\"'][^\"']+[\"']",
            "severity": Severity.HIGH,
            "message": "하드코딩된 비밀번호"
        },
        "DEBUG_MODE": {
            "pattern": r"DEBUG\s*=\s*True",
            "severity": Severity.MEDIUM,
            "message": "프로덕션에서 디버그 모드 활성화"
        },
        "WEAK_CRYPTO": {
            "pattern": r"(md5|sha1)\s*\(",
            "severity": Severity.MEDIUM,
            "message": "약한 암호화 알고리즘 사용"
        }
    }

    def scan_file(self, file_path: str, content: str) -> List[Vulnerability]:
        """파일 스캔"""
        vulnerabilities = []
        lines = content.split('\n')

        for vuln_type, config in self.VULNERABILITY_PATTERNS.items():
            pattern = re.compile(config["pattern"], re.IGNORECASE)

            for line_num, line in enumerate(lines, 1):
                if pattern.search(line):
                    vulnerabilities.append(Vulnerability(
                        id=f"SAST-{vuln_type}-{line_num}",
                        name=vuln_type,
                        severity=config["severity"],
                        description=config["message"],
                        file_path=file_path,
                        line_number=line_num,
                        recommendation=self._get_recommendation(vuln_type)
                    ))

        return vulnerabilities

    def _get_recommendation(self, vuln_type: str) -> str:
        recommendations = {
            "SQL_INJECTION": "파라미터화된 쿼리 또는 ORM을 사용하세요",
            "XSS": "입력을 이스케이프하거나 textContent를 사용하세요",
            "HARDCODED_PASSWORD": "환경 변수나 시크릿 매니저를 사용하세요",
            "DEBUG_MODE": "프로덕션에서는 DEBUG=False로 설정하세요",
            "WEAK_CRYPTO": "SHA-256 이상 또는 bcrypt를 사용하세요"
        }
        return recommendations.get(vuln_type, "코드를 검토하세요")


# ============================================================
# 2. SCA (Software Composition Analysis)
# ============================================================

class SCAScanner:
    """의존성 취약점 스캐너"""

    # 모의 CVE 데이터베이스
    CVE_DATABASE = {
        ("log4j", "2.14.1"): [
            {"cve": "CVE-2021-44228", "severity": "CRITICAL",
             "description": "Log4Shell RCE", "cvss": 10.0}
        ],
        ("express", "4.17.0"): [
            {"cve": "CVE-2022-24999", "severity": "HIGH",
             "description": "qs prototype pollution", "cvss": 7.5}
        ],
        ("lodash", "4.17.15"): [
            {"cve": "CVE-2020-8203", "severity": "HIGH",
             "description": "Prototype pollution", "cvss": 7.4}
        ]
    }

    def scan_dependencies(self, dependencies: List[Dependency]) -> List[Dict]:
        """의존성 스캔"""
        results = []

        for dep in dependencies:
            key = (dep.name.lower(), dep.version)
            if key in self.CVE_DATABASE:
                for vuln in self.CVE_DATABASE[key]:
                    results.append({
                        "dependency": f"{dep.name}@{dep.version}",
                        "cve": vuln["cve"],
                        "severity": vuln["severity"],
                        "description": vuln["description"],
                        "cvss": vuln["cvss"],
                        "direct": dep.direct
                    })

        return results

    def get_fixed_version(self, package: str, current_version: str) -> Optional[str]:
        """수정된 버전 조회"""
        fixed_versions = {
            ("log4j", "2.14.1"): "2.17.1",
            ("express", "4.17.0"): "4.18.2",
            ("lodash", "4.17.15"): "4.17.21"
        }
        return fixed_versions.get((package.lower(), current_version))


# ============================================================
# 3. Secret Scanner
# ============================================================

class SecretScanner:
    """시크릿 스캐너"""

    SECRET_PATTERNS = {
        "AWS_ACCESS_KEY": r"AKIA[0-9A-Z]{16}",
        "AWS_SECRET_KEY": r"(?i)aws(.{0,20})?['\"][0-9a-zA-Z/+=]{40}['\"]",
        "GITHUB_TOKEN": r"ghp_[0-9a-zA-Z]{36}",
        "PRIVATE_KEY": r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----",
        "API_KEY_GENERIC": r"(?i)(api[_-]?key|apikey)['\"]?\s*[:=]\s*['\"][0-9a-zA-Z]{20,}['\"]"
    }

    def scan_file(self, file_path: str, content: str) -> List[Dict]:
        """시크릿 스캔"""
        findings = []
        lines = content.split('\n')

        for secret_type, pattern in self.SECRET_PATTERNS.items():
            regex = re.compile(pattern)

            for line_num, line in enumerate(lines, 1):
                matches = regex.findall(line)
                if matches:
                    findings.append({
                        "type": secret_type,
                        "file": file_path,
                        "line": line_num,
                        "match": matches[0] if isinstance(matches[0], str) else matches[0][0] if matches[0] else "",
                        "recommendation": "시크릿을 환경 변수나 시크릿 매니저로 이동하세요"
                    })

        return findings


# ============================================================
# 4. SBOM 생성기
# ============================================================

class SBOMGenerator:
    """SBOM 생성기"""

    def generate(self, dependencies: List[Dependency],
                 project_name: str, version: str) -> Dict:
        """CycloneDX 형식 SBOM 생성"""
        components = []

        for dep in dependencies:
            component = {
                "type": "library",
                "name": dep.name,
                "version": dep.version,
                "scope": "required" if dep.direct else "optional",
                "properties": [
                    {"name": "directDependency",
                     "value": str(dep.direct).lower()}
                ]
            }

            if dep.vulnerabilities:
                component["vulnerabilities"] = dep.vulnerabilities

            components.append(component)

        sbom = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "serialNumber": f"urn:uuid:{self._generate_uuid()}",
            "version": 1,
            "metadata": {
                "component": {
                    "type": "application",
                    "name": project_name,
                    "version": version
                },
                "timestamp": self._get_timestamp()
            },
            "components": components
        }

        return sbom

    def _generate_uuid(self) -> str:
        import uuid
        return str(uuid.uuid4())

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"


# ============================================================
# 5. 보안 게이트
# ============================================================

class SecurityGate:
    """CI/CD 보안 게이트"""

    def __init__(self, fail_on: List[Severity] = None):
        self.fail_on = fail_on or [Severity.CRITICAL, Severity.HIGH]

    def evaluate(self, vulnerabilities: List[Vulnerability]) -> Tuple[bool, str]:
        """보안 게이트 평가"""
        blocked_severities = [v for v in vulnerabilities
                             if v.severity in self.fail_on]

        if blocked_severities:
            summary = f"❌ 보안 게이트 실패: {len(blocked_severities)}개 취약점"
            for v in blocked_severities[:5]:  # 최대 5개 표시
                summary += f"\n  - [{v.severity.name}] {v.name}: {v.file_path}:{v.line_number}"
            return False, summary

        return True, f"✅ 보안 게이트 통과: {len(vulnerabilities)}개 취약점 (차단 기준 미만)"


# ============================================================
# 6. DevSecOps 파이프라인
# ============================================================

class DevSecOpsPipeline:
    """DevSecOps 파이프라인"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.sast = SASTScanner()
        self.sca = SCAScanner()
        self.secret_scanner = SecretScanner()
        self.sbom_generator = SBOMGenerator()
        self.security_gate = SecurityGate()

    def run_security_scan(self, source_files: Dict[str, str],
                         dependencies: List[Dependency]) -> Dict:
        """전체 보안 스캔 실행"""
        results = {
            "project": self.project_name,
            "sast_findings": [],
            "sca_findings": [],
            "secret_findings": [],
            "gate_passed": True,
            "summary": {}
        }

        # SAST 스캔
        for file_path, content in source_files.items():
            vulns = self.sast.scan_file(file_path, content)
            results["sast_findings"].extend(vulns)

            secrets = self.secret_scanner.scan_file(file_path, content)
            results["secret_findings"].extend(secrets)

        # SCA 스캔
        results["sca_findings"] = self.sca.scan_dependencies(dependencies)

        # 보안 게이트 평가
        gate_passed, gate_message = self.security_gate.evaluate(
            results["sast_findings"]
        )
        results["gate_passed"] = gate_passed
        results["gate_message"] = gate_message

        # 요약
        results["summary"] = {
            "total_sast": len(results["sast_findings"]),
            "total_sca": len(results["sca_findings"]),
            "total_secrets": len(results["secret_findings"]),
            "critical": sum(1 for v in results["sast_findings"]
                          if v.severity == Severity.CRITICAL),
            "high": sum(1 for v in results["sast_findings"]
                       if v.severity == Severity.HIGH)
        }

        return results

    def generate_sbom(self, dependencies: List[Dependency],
                     version: str) -> Dict:
        """SBOM 생성"""
        return self.sbom_generator.generate(dependencies, self.project_name, version)


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DevSecOps 보안 스캐너")
    print("=" * 60)

    # 테스트 소스 코드
    source_files = {
        "app.py": """
password = "admin123"  # 하드코딩된 비밀번호

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id  # SQL 인젝션
    return execute(query)

DEBUG = True  # 디버그 모드
        """,
        "config.js": """
const apiKey = "sk-1234567890abcdefghijklmnop";  # API 키 하드코딩
const awsKey = "AKIAIOSFODNN7EXAMPLE";  # AWS 키
        """
    }

    # 테스트 의존성
    dependencies = [
        Dependency("log4j", "2.14.1", direct=True),
        Dependency("express", "4.17.0", direct=True),
        Dependency("lodash", "4.17.15", direct=False),
        Dependency("react", "18.2.0", direct=True),
    ]

    # 파이프라인 실행
    pipeline = DevSecOpsPipeline("SecureApp")
    results = pipeline.run_security_scan(source_files, dependencies)

    print(f"\n📊 스캔 결과 요약:")
    print(f"  SAST 취약점: {results['summary']['total_sast']}개")
    print(f"  SCA 취약점: {results['summary']['total_sca']}개")
    print(f"  시크릿 노출: {results['summary']['total_secrets']}개")
    print(f"  Critical/High: {results['summary']['critical']}/{results['summary']['high']}")

    print(f"\n🚪 {results['gate_message']}")

    # SCA 상세
    print(f"\n📦 SCA 취약점 상세:")
    for vuln in results["sca_findings"]:
        print(f"  - {vuln['dependency']}: {vuln['cve']} ({vuln['severity']})")

    # SBOM 생성
    sbom = pipeline.generate_sbom(dependencies, "1.0.0")
    print(f"\n📋 SBOM 생성: {len(sbom['components'])}개 컴포넌트")
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| **조기 취약점 발견**: 개발 단계에서 발견 → 수정 비용 100배 절감 | **오탐지(False Positive)**: SAST 오탐으로 개발 생산성 저하 |
| **자동화된 컴플라이언스**: 지속적 검증으로 규정 준수 증명 | **도구 복잡성**: SAST/DAST/SCA 각각 도구·설정 필요 |
| **속도와 보안 동시 확보**: 빠른 배포 속도 유지하며 보안 강화 | **학습 곡선**: 보안 지식 없는 개발자에게 진입 장벽 |
| **공급망 보안**: SBOM으로 0-day 발생 시 영향 범위 신속 파악 | **초기 비용**: 도구 도입·파이프라인 구축 비용 |

**DevOps vs DevSecOps 비교** (필수: 2개 대안):

| 비교 항목 | DevOps | DevSecOps | SecDevOps |
|---------|--------|-----------|-----------|
| **보안 처리 시점** | 출시 전 별도 검토 | ★ SDLC 전 단계 통합 | 설계부터 보안 최우선 |
| **보안 담당** | 별도 보안팀 | ★ 전 팀 공동 책임 | 보안팀 주도 |
| **자동화 범위** | CI/CD | ★ CI/CD + 보안 검사 | 보안 검사 우선 |
| **배포 속도** | 빠름 | 빠름 (자동화 시) | 중간 (보안 검사 충분) |
| **컴플라이언스** | 사후 감사 | ★ 자동화된 지속 검증 | 실시간 모니터링 |

> **★ 선택 기준**: 일반 서비스 → DevSecOps, 금융·의료 등 높은 보안 요구 → SecDevOps

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **금융권** | DevSecOps 파이프라인 + SIEM 통합 | 보안 사고 80% 감소, 감사 대응 시간 90% 단축 |
| **SaaS 서비스** | SCA + SBOM 자동화 | Log4Shell 대응 시간: 3일 → 3시간 |
| **공공 클라우드** | IaC 보안 + 컨테이너 스캔 | 인프라 취약점 95% 조기 차단 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: Netflix** - Chaos Engineering + DevSecOps. 보안을 "개발자 경험"의 일부로 통합. 하루 4,000회 배포, 보안 사고 0

- **사례 2: GitLab** - Auto DevOps로 SAST/DAST/SCA 자동화. 모든 MR에 보안 스캔. 취약점 발견~수정 시간 2주 → 2일

- **사례 3: 카카오** - DevSecOps 도입 후 Log4Shell 대응. SBOM으로 30분 내 영향받는 서비스 식별 완료

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: CI/CD 플랫폼과 통합, SAST/DAST/SCA 도구 선정, 오탐 튜닝
2. **운영적**: 보안 챔피언 양성, 개발자 보안 교육, 인시던트 대응 프로세스
3. **보안적**: 규제 요구사항(PCI-DSS, ISMS-P), 데이터 분류, 암호화 표준
4. **경제적**: 도구 라이선스, 인력 교육, 오탐으로 인한 지연 비용

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **보안 병목**: 모든 빌드에 30분 SAST → 개발 속도 저하. 해결: 증분 스캔, 병렬화
- ❌ **오탐 무시**: "이건 오탐이야" → 진짜 취약점 놓침. 해결: 오탐 튜닝, 심각도 조정
- ❌ **공급망 무시**: 직접 의존성만 스캔 → 간접 의존성 취약점 누락. 해결: 전체 의존성 트리 스캔

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  DevSecOps 핵심 연관 개념 맵                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [CI/CD] ←──→ [DevSecOps] ←──→ [OWASP]                        │
│        ↓              ↓               ↓                         │
│   [컨테이너]       [SBOM]         [Zero Trust]                  │
│        ↓              ↓               ↓                         │
│   [Kubernetes]    [SLSA]          [SIEM]                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| CI/CD | 기반 인프라 | 자동화된 파이프라인 | `[software_testing](../testing/software_testing.md)` |
| OWASP | 보안 표준 | Top 10, ASVS | `[software_security](../../security/)` |
| 플랫폼 엔지니어링 | 확장 개념 | IDP 내 보안 내재화 | `[platform_engineering](./platform_engineering.md)` |
| 애자일 | 프로세스 기반 | 스프린트 내 보안 | `[agile_methodology](./agile_methodology.md)` |
| 컨테이너 | 기술 대상 | 이미지 보안 스캔 | `[cloud_native](../../cloud/)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **보안 비용 절감** | 조기 취약점 탐지로 수정 비용 절감 | 개발 단계 발견 시 운영 대비 100배 절감 |
| **배포 속도** | 자동화된 보안 게이트 | 배포 주기 30~50% 단축 |
| **컴플라이언스** | 자동 감사 로그 | ISMS-P, ISO 27001 감사 대응 시간 90% 단축 |
| **공급망 대응** | SBOM 기반 영향 분석 | 0-day 대응 시간: 일 → 시간 |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: AI 기반 취약점 탐지, 자동 수정 제안, AI-Powered DevSecOps. GitHub Copilot에 보안 분석 내재화

2. **시장 트렌드**: SBOM 의무화 확대(미국 EO 14028 → EU, 한국), 공급망 보안 인증(SLSA) 필수화

3. **후속 기술**: Policy-as-Code(Open Policy Agent), Runtime Application Self-Protection(RASP), Confidential Computing

> **결론**: DevSecOps는 소프트웨어 개발에서 보안을 **비용이 아닌 경쟁력**으로 변환하는 패러다임이다. 오픈소스 의존성이 90% 이상인 현대 소프트웨어에서 SCA와 SBOM은 필수다. "Shift Left"는 단순한 구호가 아니라 비즈니스 생존 전략이다.

> **※ 참고 표준**: OWASP Top 10, NIST SP 800-218 (SSDF), 미국 EO 14028, KISA 소프트웨어 개발 보안 가이드

---

## 어린이를 위한 종합 설명

DevSecOps는 마치 **"집 짓는 중에 계속 안전 검사"** 같아요!

**기존 방식은:**
집을 다 지은 다음에 "화재 검사 해주세요!" 하고 요청해요. 그런데 문제가 발견되면? 벽을 허물고 다시 지어야 해요. 😱

**DevSecOps(Shift Left)는:**
- 기초 공사할 때 → "흙은 단단한가요?"
- 벽 세울 때 → "전선은 안전한가요?"
- 지붕 올릴 때 → "번개 맞아도 괜찮나요?"
- 계속 검사! 🔍

이렇게 하면 문제를 **일찍 발견**해서 **돈도 아끼고** **시간도 절약**해요!

**세 가지 도구:**

1. **SAST** (설계도 검토): 코드를 실행하지 않고 읽어만 봐요
   - "이건 위험해 보여!"

2. **DAST** (침입 테스트): 실제로 들어가서 공격해 봐요
   - "이 문은 따기 쉬워!"

3. **SCA** (자재 성분 확인): 사용한 재료가 안전한지 봐요
   - "이 벽돌은 결함이 있어!"

**Log4Shell 이야기:**
2021년에 Log4j라는 도구에 치명적인 구멍이 발견됐어요. 전 세계 수만 개 회사가 영향을 받았죠!

SBOM(성분표)이 있으면: "우리도 이거 썼어! 얼른 고치자!" 하고 1시간 만에 알 수 있어요.
없으면: "우리가 뭘 썼는지 모르겠어..." 하고 며칠을 헤매야 해요. 😭

이게 바로 DevSecOps의 힘이에요! 🛡️
