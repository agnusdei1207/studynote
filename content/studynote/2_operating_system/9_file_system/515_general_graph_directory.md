+++
title = "515. 일반 그래프 디렉터리 (General Graph Directory) - 순환(Cycle) 문제"
date = "2026-03-14"
weight = 515
+++

# 515. 일반 그래프 디렉터리 (General Graph Directory) - 순환(Cycle) 문제

## # 핵심 인사이트 (3줄 요약)
> 1. **본질**: **일반 그래프 디렉터리 (General Graph Directory)**는 파일 시스템의 유연성을 극대화하기 위해 **트리(Tree)** 구조의 부모-자식 계층 제약을 제거하여, **공유(Subsharing)**와 **순환(Cycle)** 형성을 허용하는 가장 범용적인 그래프 구조입니다.
> 2. **위험**: 무분별한 **링크(Link)** 생성으로 인해 디렉터리 간 순환 경로가 발생하면, **순회(Traversal)** 알고리즘의 **무한 루프(Infinite Loop)**와 **참조 계수(Reference Count)** 기반의 자원 해제 불능(메모리 누수) 현상을 초래하여 시스템 신뢰성을 심각하게 저해합니다.
> 3. **해결**: 이를 해결하기 위해 OS 커널 레벨에서 **가비지 컬렉션(Garbage Collection)**을 통한 도달 불가능한 객체(Unreachable Object) 탐지(Reachability Analysis)나, **방문 비트(Visited Bit)** 및 **아이노드(Inode)** 기반의 순환 방지 로직을 필수적으로 구현해야 합니다.

---

## Ⅰ. 개요 (Context & Background) - [500자+]

**1. 개념 및 정의**
**일반 그래프 디렉터리 (General Graph Directory)**는 파일 시스템의 구조를 수학적인 **그래프(Graph)** 자료 구조로 모델링한 것입니다. 전통적인 **트리 구조 디렉터리 (Tree-Structured Directory)**가 하나의 노드(파일 또는 디렉터리)가 단 하나의 부모(Parent) 노드만을 가지는 엄격한 계층적(Hierarchical) 구조인 반면, 일반 그래프 구조는 **다중 부모(Multi-parent)** 개념을 허용합니다. 즉, 하나의 실제 데이터 파일(아이노드)이 서로 다른 여러 경로(Path)를 통해 참조될 수 있도록 하여, 사용자에게 논리적인 데이터 공유를 제공하는 구조입니다.

**2. 배경 및 철학 (Evolution)**
초기 파일 시스템은 단순한 1계층(Single-Level) 또는 다계층(Tree) 구조로 충분했습니다. 그러나 시스템이 복잡해짐에 따라 동일한 프로그램이나 데이터를 여러 사용자가 중복 저장 없이 공유해야 하는 필요성이 대두되었습니다. 이를 위해 유닉스(UNIX) 계열 파일 시스템은 **하드 링크(Hard Link)**라는 메커니즘을 도입하여 물리적인 데이터는 하나지만, 여러 디렉터리 엔트리가 이를 가리키도록 허용했습니다. 이로 인해 파일 시스템의 위상(Topology)은 트리에서 그래프로 확장되었습니다.

**3. 핵심 기술적 난제: 순환(Cycle)과 자원 관리**
일반 그래프 구조의 도입은 필연적으로 **순환 참조(Circular Reference)**, 즉 **사이클(Cycle)** 문제를 야기했습니다. 사용자가 실수 혹은 의도적으로 하위 디렉터리가 상위 디렉터리를 다시 가리키는 링크를 생성하면, 경로 탐색(Traversal) 시 무한히 되돌아오는 구조가 형성됩니다. 또한, 트리 구조에서는 부모 노드가 삭제되면 자식 노드의 존재 여부가 명확했으나, 그래프 구조에서는 외부에서의 참조가 끊겼더라도 내부적으로 서로를 참조하는 고립된 섬(Isolated Island)이 발생하여, 참조 계수(Reference Count)만으로는 여전히 살아있는 객체로 오인하여 메모리(디스크 블록)를 해제하지 못하는 **자원 누수(Resource Leak)** 현상이 발생합니다.

```text
      [ 구조적 진화 과정 ]
    
    (1) Single-Level          (2) Tree-Structured         (3) General Graph
    +------------------+      +------------------+       +------------------+
    | Root             |      | Root             |       | Root             |
    |  - file1         |      |  +--+--+         |       |  +--+--+         |
    |  - file2         |      |  |A |B |         |       |  |A |B |<--+      |
    |  - file3         |      |  +--+--+         |       |  +--+--+   |      |
    +------------------+      |     |            |       |     |      |      |
                              |  +--+--+        |       |  +--+--+  |      |
                              |  |C |D |        |       |  |C |D |--+      |
    (단순, 빠름, 혼잡)        |  +--+--+        |       |  +--+--+         |
                              | (계층화됨)       |       | (공유 & 순환 위험) |
                              +------------------+       +------------------+
```

📢 **섹션 요약 비유**: 일반 그래프 디렉터리는 "도시의 지하철 노선도"와 같습니다. 환승 구조(링크)를 통해 어디서든지 목적지로 갈 수 있도록 자유로운 연결을 허용하지만, 운영 실수로 순환선이 제대로 통제되지 않으면 열차(탐색 알고리즘)가 영원히 제자리를 맴도는 사고가 발생할 수 있는 위험한 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

### 1. 구조적 아키텍처 및 데이터 흐름 (Inode-based Graph)
일반 그래프 디렉터리의 핵심은 파일의 메타데이터와 실제 데이터를 분리하고, 메타데이터인 **아이노드(Inode, Index Node)**를 통해 그래프의 정점(Vertex)을 구현하는 것입니다. 디렉터리 엔트리는 단순히 `<파일명, 아이노드 번호>`의 쌍(Pair)일 뿐이며, 서로 다른 디렉터리가 동일한 아이노드 번호를 가리킴으로써 공유(Sharing)를 구현합니다. 이때 아이노드 내부의 `nlink` 필드(참조 카운트)를 통해 현재 몇 개의 경로가 이 파일을 가리키는지 추적합니다.

**ASCII 구조 다이어그램: Inode 기반 그래프 및 순환 발생 구조**

```text
+-----------------------------------------------------------------------+
|                         Disk Block Structure                          |
+-----------------------------------------------------------------------+
|                                                                       |
|  [Root Dir] (Inode #5)  ──────────────────────┐                       |
|  +--------------------------+                 │ (Hard Link)           |
|  | Name: "."  -> Inode: 5   |                 │                       |
|  | Name: "usr" -> Inode: 20 │----------------─┼─┐                     |
|  +--------------------------+                 │ │                     |
|                                                 ▼ ▼                     |
|                                    [Usr Dir] (Inode #20)                |
|                                    +--------------------------+         |
|                                    | Name: "."  -> Inode: 20  |         |
|                                    | Name: "bin" -> Inode: 21 |         |
|                                    +--------------------------+         |
|                                                 │                        |
|                                                 ▼                        |
|                                    [Bin Dir] (Inode #21)                 |
|                                    +--------------------------+         |
|                                    | Name: "."  -> Inode: 21  |         |
|  ⚠ CYCLE LINK ⚠                   | Name: "log" -> Inode: 15 |         |
|  (Admin Mistake)                   | Name: ".." -> Inode: 20  | <───┘  |
|  ln /usr /usr/bin/usr              +--------------------------+         |
|                                                                       |
|  (Description: 'Usr' directory is pointed by Root and also by 'Bin')  |
|               Creating a loop: Root -> Usr -> Bin -> Usr ...          |
+-----------------------------------------------------------------------+
```

**해설 (200자+)**: 위 다이어그램은 일반 그래프 디렉터리에서의 **하드 링크(Hard Link)**와 **순환(Cycle)** 형성 과정을 도식화한 것입니다. 기본적으로 `Root`는 `Usr(Inode #20)`을 가리키고, `Usr`는 `Bin(Inode #21)`을 가리키는 계층 구조를 가집니다. 그러나 관리자가 실수로 `Usr` 디렉터리를 가리키는 하드 링크를 `Bin` 디렉터리 내부에 생성하면(빨간색 화살표), `Usr -> Bin -> Usr` 형태의 순환이 발생합니다. 이 구조에서 `Root`에서부터 탐색을 시작하면 `Usr`에 도달한 후 `Bin`을 거쳐 다시 `Usr`로 돌아오며 무한 루프에 빠지게 됩니다. 또한, Inode #20의 `nlink`는 2(Root, Bin)가 되어, `Root`에서 삭제하더라도 `Bin`의 참조로 인해 디스크에서 실제로 삭제되지 않는 자원 누수 상황이 발생합니다.

### 2. 상세 동작 원리 및 순환 탐지 메커니즘 (Depth-First Search with Visited Bit)
일반 그래프 구조에서 파일을 검색하거나(`find`), 디스크 사용량을 계산하거나(`du`), 백업을 수행할 때(tar), 운영체제는 **그래프 순회(Graph Traversal)** 알고리즘을 사용합니다. 트리와 달리 그래프는 이미 방문한 노드를 다시 방문할 수 있으므로, 이를 방지하기 위해 **방문 비트(Visited Bit)** 또는 **색상 표시법(Color Marking: White/Gray/Black)**을 사용해야 합니다.

**① 링크 생성 시스템 콜 (System Call: `link`)**
`link(const char *oldpath, const char *newpath)` 함수가 호출되면, 파일 시스템 드라이버는 다음 과정을 수행합니다.
1. `oldpath`가 가리키는 원본 파일의 **아이노드(Inode)**를 메모리에 로드합니다.
2. `newpath`가 위치할 디렉터리의 데이터 블록에 새로운 엔트리를 추가합니다(파일명 + 아이노드 번호).
3. 원본 아이노드의 `nlink` 필드를 원자적(Atomic) 연산으로 1 증가시킵니다.
4. 이때 만약 `newpath`가 디렉터리라면, 대부분의 현대 파일 시스템(ext4, NTFS 등)은 순환 방지를 위해 **디렉터리에 대한 하드 링크 생성을 슈퍼유저(Superuser)에게조차 제한**하거나 금지합니다.

**② 순회 알고리즘 및 탐지 (Traversal & Detection)**
그래프 순회는 주로 **깊이 우선 탐색(DFS, Depth-First Search)** 방식을 사용합니다.
- **탐지 로직**: 각 Inode마다 `visited` 플래그를 둡니다. 탐색 시작 시 `visited=true`로 설정하고, 자식 노드를 탐색할 때 이 플래그를 확인합니다. 만약 자식 노드가 이미 `visited=true`라면, 현재 경로 상에 존재하는 노드이므로 순환(Cycle)으로 간주하고 즉시 해당 경로의 탐색을 중단(Backtrack)합니다.

**③ 자원 해제의 문제점 (Reference Counting Limitation)**
순환이 발생하면 참조 계수(Reference Count) 방식만으로는 객체를 해제할 수 없습니다.
- **시나리오**: `A -> B -> C -> A` (Cycle)
- **동작**: 외부에서 `A`를 가리키는 참조를 모두 제거(`unlink`)하면, 논리적으로는 접근 불가능한 상태가 되어야 합니다.
- **결과**: 하지만 내부적으로 `A`는 `C`에 의해, `C`는 `B`에 의해, `B`는 `A`에 의해 참조되고 있으므로, 모든 노드의 `nlink`가 0이 되지 않습니다. 이를 해결하기 위해선 후술할 **Mark-and-Sweep(가비지 컬렉션)** 기법이 필요합니다.

### 3. 핵심 알고리즘: 순환 감지 순회 코드 (C 스타일 의사코드)

```c
#include <stdbool.h>
#include <stdio.h>

#define MAX_INODES 65536

// 시스템 전체의 Inode 방문 여부를 추적하는 비트맵 (또는 해시 테이블)
// OS 부팅 시 또는 탐색 시작 시 false로 초기화됨
bool visited_bitmap[MAX_INODES];

/**
 * 순환 감지 기능을 포함한 디렉터리 순회 함수 (DFS 기반)
 * @param dir_inode 현재 탐색 중인 디렉터리의 Inode 포인터
 * @param depth 현재 탐색 깊이 (Stack Overflow 방지용)
 */
void traverse_graph_directory(inode_ptr dir_inode, int depth) {
    // 안전 장치: 탐색 깊이 제한 (Symlink Attack 등 방지)
    if (depth > MAX_DEPTH_LIMIT) {
        printf("Error: Maximum depth limit reached. Possible symlink loop.\n");
        return;
    }

    // [핵심 로직] 순환 탐지: 이미 방문한 Inode인가?
    if (visited_bitmap[dir_inode->ino_num] == true) {
        printf("Warning: Cycle detected at Inode %d. Backtracking...\n", dir_inode->ino_num);
        return; // 더 이상 진행하지 않고 리턴하여 무한 루프 방지
    }

    // 현재 노드를 방문 상태로 표시 (Mark)
    visited_bitmap[dir_inode->ino_num] = true;

    // 디렉터리 내의 모든 엔트리에 대해 반복 (File System Layout에 따른 순회)
    dir_entry_t *entry;
    list_for_each_entry(dir_inode->entry_list, entry) {
        
        // 만약 엔트리가 디렉터리라면 재귀 호출 (Recursive Step)
        if (entry->file_type == FT_DIR) {
            // "."(현재) 이나 ".."(부모)에 대한 예외 처리는 필수적이나, 
            // Hard Link에 의한 일반 그래프에서는 ".."이 부모가 아닐 수 있음에 유의
            traverse_graph_directory(entry->target_inode, depth + 1);
        } else {
            // 파일인 경우 처리 로직 수행 (예: 백업, 검색)
            process_file(entry->target_inode);
        }
    }

    // (선택 사항) 모든 경로를 탐색해야 하는 경우가 아니라면, 
    // 방문 플래그를 해제하지 않음으로써 중복 방문을 차단 (성능 최적화)
    // visited_bitmap[dir_inode->ino_num] = false; 
}
```

📢 **섹션 요약 비유**: 일반 그래프의 내부 작동은 "전동 택배 시스템"과 같습니다. 물건(파일)을 배송하는 로봇(탐색 알고리즘)이 회전 교차로에서 길을 잃고 영원히 배달하지 못하는 것을 막기 위해, 로봇은 자신이 지나갔던 경로를 실시간으로 기록하는 억세스 카드(Visited Bit)를 반드시 소지해야 합니다. 이 카드가 없다면 로봇은