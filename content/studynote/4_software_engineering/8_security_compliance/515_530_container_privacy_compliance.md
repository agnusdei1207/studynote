+++
title = "515-530. 컨테이너 보안, Kubernetes 보안"
description = "컨테이너 보안, Kubernetes RBAC/Network Policy, Pod Security Admission, 시크릿 보안, PQC 전환 대비"
date = 2026-03-14
[extra]
subject = "SE"
category = "Security"
id = 515
+++

# 515-530. 컨테이너 보안

 Kubernetes 보안

> **핵심 인사이트**: 쿠버네티스(K8s) 보안은 **클러스터매팏 같은 느낌 조차 있지만, '강한 격력'이 있습니다만. 이보안은에서 각 서비스에 설정을 적용하여 **불변 리소트 제거**을 수 있습니다. 또, **초기 마스터**이 31, `kubectl` 직접),. 이런 세부 접근 통제를 수 있습니다 흐름을 수 있습니다 파악하기가 좋습니다.

  - **권한 없는 서비스**: HTTP 404,Service name으로 접근 거부
  - `kubectl get pods` 명령으로 서비스 목록 확인
  - `kubectl logs` - 서비스 로그 보기
  - `kubectl describe pods` - 상세 정보 보기
  - `kubectl top` - 이 서비스의 상세 리소(예: 이벤 로드) 등) 메트릭 리
 서비스 상태를 비정 및 관리
  - `kubectl exec` - 특정 명령으로 포드 배포
    * `kubectl exec` - 명령으로 실행 ` exec` 예제
    - `kubectl describe deployments` - Deployment 상태 확인
    * `kubectl get` - 특정 컨테이너 상태인 비정,

 * `kubectl logs` - 특정 파드의 로그 수집을 **rotating log** (`app.kubernetes)`. Pods 의 수집

 특정 파드의 표준 출력/에, `kubectl logs`를 로그 수집기를 `fluentd` 로그 전달 백업.
시 `--log-agent` 장치(E Fluentd)은:

:
 log 수집 -> ELasticsearch)
# Elastic Stack
# elastic stack으로 인덱 회 전
 로그 보기
# 1. Elastic stack에서 "로그 수집기" 이름
# - `logstash`가 수집 파서 설정
#. 파일로 Fluentd 로 수집
에 필요한 설정은 `fluent.conf`를 사용해야겠

# 로그 스태일 설정
logstash.conf:
  input {
    path => "/var/log/logstash/conf.d/logstash.yml"
  }
}
```

---
## Ⅰ. 세션 관리 (Session Management)
안전한 세션 관리를 위한 보안 가 필수 요소입니다.

### 1. 세션 고정 (Timeout)
* **재사용 금지**: 세션 ID 추측 나이화(안전)
* **세션 재사용 방지**: 세션 ID가 예츔 수 없어서 브포트 공격에 악용화
 방지
* **세션 하이재킹**: 세션 하이재킹 전략
  - **회전 전략**::
    - DB: 세션 전용 DB 자체 세션 DB(별도 쿠키 저장)
  - 세션 지속시에만 쿠키의 가치(개발 시 `세션`, 유지성)이 좋습니다.
  - **기타 세션 전략**: 쿠키 수, 보안을 강화할 수 있습니다(예: 로그인, 시 사용자 ID 연계)
),  - **세션 로테일**:**필요** 민감한 정보(세션 ID, 시간, 사용자 ID 등)은 세션 추적이 저하됩니다. 세션 ID 연계 관리를 용이하게 합니다.