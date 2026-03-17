+++
title = "526. 해시 조인의 물리적 비용 - 메모리와 스왑의 전쟁"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 526
+++

# 526. 해시 조인의 물리적 비용 - 메모리와 스왑의 전쟁

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 해시 조인(Hash Join)은 선행 테이블(Build Input)을 메모리에 해시 테이블로 구축하고 후행 테이블(Probe Input)을 스캔하며 짝을 찾는 방식이며, 이 과정에서 **메모리(PGA) 점유 비용과 디스크 스왑(Swap) 오버헤드**가 성능의 핵심 변수가 된다.
> 2. **가치**: 인덱스가 없는 대량 데이터 조인 시 최고의 효율을 내지만, 메모리가 부족하여 **Grace Hash Join**으로 전이될 경우 디스크 I/O가 급증하여 성능이 수십 배 급락할 수 있다.
> 3. **융합**: 고도의 메모리 관리 기법과 해시 함수 분할 기술이 융합되어, 제한된 RAM 자원 하에서 최적의 조인 파티셔닝 전략을 수립한다.

+++

### Ⅰ. 해시 조인의 2단계 비용 분석

1. **Build Phase (빌드 단계)**:
    - 선행 테이블을 읽어 해시 테이블을 만드는 비용. 
    - **CPU 비용**: 해시 함수 연산량. 
    - **메모리 비용**: 해시 버킷과 데이터를 담을 PGA 공간.
2. **Probe Phase (프로브 단계)**:
    - 후행 테이블을 한 행씩 읽으며 해시 테이블을 뒤지는 비용.
    - **I/O 비용**: 후행 테이블 전체 스캔 비용.

+++

### Ⅱ. 메모리 부족 시의 성능 저하 시각화 (ASCII Model)

```text
[ Case 1: In-Memory Hash Join ] ✅
  [ Small Table ] ──▶ [ Hash Table in RAM ] ──◀ [ Big Table ]
  * Fast! (No Disk I/O for Join)

[ Case 2: Multi-Pass / Grace Hash Join ] 💥
  [ Small Table ] ──▶ (Too Big for RAM!) ──▶ [ Temp Disk Shards ] 💾
                                                    │
  [ Big Table ]   ──▶ (Sharding by Hash) ──▶ [ Temp Disk Shards ] 💾
                                                    │
  * [ Join Shard A ] ◀──(Fetch from Disk)──▶ [ Join Shard B ] 💥
  * Slow! (Massive Random I/O and Swapping)
```

+++

### Ⅲ. 실무적 튜닝 포인트

- **선행 테이블(Build Input) 최소화**: 해시 테이블을 만드는 테이블이 가급적 작아야 메모리 내에서 조인이 끝납니다. (Join Order 중요)
- **PGA_AGGREGATE_TARGET**: 조인을 위한 메모리 한도 설정을 최적화하여 디스크 쓰기를 미연에 방지합니다.
- **해시 충돌(Collision) 방지**: 해시 버킷의 개수를 충분히 확보하여 체이닝(Chaining)으로 인한 CPU 부하를 줄입니다.

- **📢 섹션 요약 비유**: 해시 조인은 **'친구의 얼굴을 미리 사진첩(해시 테이블)에 넣어두고 길 가는 사람들(큰 테이블)과 대조하는 것'**과 같습니다. 사진첩이 가벼워 내 손(메모리)에 쏙 들린다면 아주 빠르게 사람을 찾겠지만, 사진첩이 수천 권이라 손에 들 수 없다면 땅바닥에 늘어놓고(디스크 스왑) 매번 허리를 굽혀 확인해야 하므로 속도가 엄청나게 느려지는 것과 같습니다.

+++

### Ⅳ. 개념 맵 및 요약

- **[One-pass vs Multi-pass]**: 메모리 한 번으로 끝나느냐, 디스크를 여러 번 오가느냐의 구분.
- **[Grace Hash Join]**: 메모리 부족 시 데이터를 조각내어 디스크에서 처리하는 알고리즘.
- **[Hash Partitioning]**: 큰 테이블 조인을 위해 데이터를 해시값 기준으로 쪼개는 기술.

📢 **마무리 요약**: **Hash Join Cost**는 메모리의 경제학입니다. 선행 테이블을 극한으로 줄이고 가용 메모리를 확보하는 것만이 대용량 데이터의 정글에서 승리하는 지름길입니다.