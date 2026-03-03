+++
title = "파일 시스템 (File System)"
date = 2025-03-02

[extra]
categories = "pe_exam-operating_system"
+++

# 파일 시스템 (File System)

## 핵심 인사이트 (3줄 요약)
> **저장장치의 데이터를 파일 단위로 체계적으로 관리**. inode로 메타데이터 관리, 블록 할당 방식으로 디스크 공간 활용. 저널링·Copy-on-Write로 데이터 무결성 보장이 핵심.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 파일 시스템(File System)은 운영체제가 저장장치(디스크, SSD)의 데이터를 파일 단위로 체계적으로 생성·삭제·읽기·쓰기하는 방법이다. 사용자와 응용 프로그램에 편리한 파일 인터페이스를 제공한다.

> 💡 **비유**: "도서관 분류 시스템" — 수많은 책(데이터)을 체계적으로 정리하고, 도서 카드(inode)로 책 위치를 찾고, 대출·반납(읽기·쓰기)을 관리해요.

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점**: 초기 컴퓨터는 데이터를 물리적 주소로 직접 접근해야 했음. 사용자가 트랙, 섹터 번호를 알아야 했고, 데이터 관리가 매우 복잡했음.
2. **기술적 필요성**: 사용자 친화적 인터페이스(파일 이름) 제공, 디스크 공간 효율적 관리, 데이터 보호 및 무결성 보장, 다중 사용자 접근 제어 필요.
3. **시장/산업 요구**: 빅데이터, 클라우드 스토리지, 컨테이너 이미지 관리 등으로 대용량·고성능 파일 시스템 수요 급증.

**핵심 목적**: 데이터의 체계적 관리, 디스크 공간 효율적 활용, 데이터 무결성과 보안 보장.

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **Superblock** | 파일 시스템 전체 메타데이터 | 크기, 블록 수, inode 수, 마운트 정보 | 도서관 전체 안내판 |
| **Inode** | 파일 메타데이터 (이름 제외) | 권한, 크기, 시간, 블록 포인터 | 도서 카드 |
| **Data Block** | 실제 파일 데이터 저장 | 4KB 단위, 할당 방식에 따라 배치 | 책 내용 |
| **Directory** | 파일 이름과 inode 매핑 | 계층적 구조, 경로 탐색 | 책장 분류표 |
| **Journal/Log** | 변경 사항 기록 | 크래시 복구, 무결성 보장 | 작업 일지 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌────────────────────────────────────────────────────────────────────────┐
│                    파일 시스템 계층 구조                                │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  📂 응용 프로그램 (Application)                                        │
│     ↓ open(), read(), write(), close()                                │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  📁 논리 파일 시스템 (Logical File System)                      │   │
│  │  • 파일 이름 → inode 번호 변환 (디렉터리 탐색)                  │   │
│  │  • 권한 검사, 파일 Lock 관리                                    │   │
│  └────────────────────────────────────────────────────────────────┘   │
│     ↓ 논리 블록 번호 (Logical Block Number)                           │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  💾 파일 조직 모듈 (File Organization Module)                   │   │
│  │  • 할당 방식: 연속/연결/색인(Inode)                             │   │
│  │  • 블록 매핑, 간접 블록 처리                                    │   │
│  └────────────────────────────────────────────────────────────────┘   │
│     ↓ 물리 블록 번호 (Physical Block Number)                          │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  💿 기본 파일 시스템 (Basic File System)                        │   │
│  │  • 버퍼 캐시 관리                                               │   │
│  │  • 디스크 블록 읽기/쓰기                                        │   │
│  └────────────────────────────────────────────────────────────────┘   │
│     ↓ I/O 요청                                                        │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  🔌 I/O 제어 (I/O Control)                                     │   │
│  │  • 장치 드라이버                                                │   │
│  │  • 인터럽트 처리, DMA                                           │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                    Inode 구조 (ext4 기준)                              │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │                        Inode (128B ~ 256B)                      │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │  mode (권한/타입)     │  uid (소유자)      │  gid (그룹)        │   │
│  │  size (파일 크기)     │  atime (접근 시간) │  mtime (수정 시간) │   │
│  │  ctime (변경 시간)    │  links_count       │  blocks            │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │  📍 직접 블록 포인터 (Direct Block Pointers) - 12개            │   │
│  │  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐│   │
│  │  │ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │ 8  │ 9  │ 10 │ 11 ││   │
│  │  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘│   │
│  │       ↓ 직접 접근 (0 ~ 48KB 파일)                               │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │  📍 단일 간접 블록 (Single Indirect) - 1개                      │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │ 1024개 블록 번호 저장 (4KB * 1024 = 4MB)                │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │  📍 이중 간접 블록 (Double Indirect) - 1개                      │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │ 1024 * 1024 블록 = 4GB                                   │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │  📍 삼중 간접 블록 (Triple Indirect) - 1개                      │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │ 1024 * 1024 * 1024 블록 = 4TB (실제 제한은 더 복잡)      │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  📊 최대 파일 크기: 약 16TB (ext4, 4KB 블록 기준)                      │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                    디스크 할당 방식 비교                                │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ① 연속 할당 (Contiguous Allocation)                                  │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  [파일 A: 블록 0-2] [파일 B: 블록 3-5] [   빈 공간   ]          │   │
│  │                                                                 │   │
│  │  장점: 빠른 순차/직접 접근                                      │   │
│  │  단점: 외부 단편화, 파일 크기 변경 어려움                       │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  ② 연결 할당 (Linked Allocation)                                      │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  [A:0→] → [A:1→] → [A:2→] → [B:0→] → [B:1→] → [B:2→null]      │   │
│  │                                                                 │   │
│  │  장점: 외부 단편화 없음, 파일 크기 유연                         │   │
│  │  단점: 순차 접근만 가능, 포인터 오버헤드                        │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  ③ 색인 할당 (Indexed Allocation) - Inode 방식                        │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  Inode: [0][1][2][3][4][5][간접]...                            │   │
│  │           ↓  ↓  ↓  ↓  ↓  ↓                                     │   │
│  │         [블록들]  (불연속적 배치 가능)                          │   │
│  │                                                                 │   │
│  │  장점: 직접 접근, 외부 단편화 없음                              │   │
│  │  단점: 작은 파일에도 Inode 오버헤드, 큰 파일은 간접 블록 필요   │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 파일 열기 요청 → ② 경로 탐색 → ③ Inode 로드 → ④ 블록 매핑 → ⑤ 데이터 읽기/쓰기
```
- **1단계 (파일 열기)**: 응용 프로그램이 파일 경로로 open() 시스템 호출
- **2단계 (경로 탐색)**: 루트 디렉터리부터 순차 탐색, 각 디렉터리의 파일명→Inode 매핑 확인
- **3단계 (Inode 로드)**: 파일의 Inode를 메모리에 로드, 권한 검사 수행
- **4단계 (블록 매핑)**: 논리 블록 번호를 물리 블록 번호로 변환 (직접/간접 포인터)
- **5단계 (데이터 I/O)**: 버퍼 캐시 확인 후 디스크 읽기/쓰기 수행

**핵심 알고리즘/공식** (해당 시 필수):
```
[디스크 공간 효율]

내부 단편화 = 블록 크기 - (파일 크기 % 블록 크기)
평균 내부 단편화 = 블록 크기 / 2

[Inode 직접 접근 가능 크기]
= 12 × 블록 크기
= 12 × 4KB = 48KB (직접 블록만 사용)

[단일 간접 블록 용량]
= (블록 크기 / 4) × 블록 크기
= (4096 / 4) × 4096 = 4MB

[무결성 보장 - 저널링]
1. 데이터 저널링: 데이터 + 메타데이터 모두 로그
2. 메타데이터 저널링: 메타데이터만 로그 (성능 ↑, 위험 ↑)
3. Writeback: 순서 보장 없음 (가장 빠름, 위험 최대)
```

**코드 예시** (필수: Python 또는 의사코드):
```python
"""
파일 시스템(File System) 핵심 알고리즘 구현
- Inode 기반 파일 시스템 시뮬레이션
- 블록 할당 (연속, 연결, 색인)
- 저널링 시스템
- 디렉터리 관리
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime
import random

class FileType(Enum):
    REGULAR = "일반 파일"
    DIRECTORY = "디렉터리"
    SYMLINK = "심볼릭 링크"

@dataclass
class Inode:
    """
    Inode (Index Node)
    - 파일의 모든 메타데이터 (파일 이름 제외)
    """
    inode_number: int
    file_type: FileType
    mode: int = 0o644  # 권한 (rwx)
    uid: int = 0       # 소유자 ID
    gid: int = 0       # 그룹 ID
    size: int = 0      # 파일 크기 (bytes)
    atime: datetime = field(default_factory=datetime.now)  # 접근 시간
    mtime: datetime = field(default_factory=datetime.now)  # 수정 시간
    ctime: datetime = field(default_factory=datetime.now)  # 변경 시간
    links_count: int = 1  # 하드 링크 수

    # 블록 포인터 (간단화를 위해 12개 직접 + 1개 간접)
    direct_blocks: List[Optional[int]] = field(default_factory=lambda: [None] * 12)
    indirect_block: Optional[int] = None

@dataclass
class DirectoryEntry:
    """디렉터리 엔트리 (파일명 → Inode 매핑)"""
    name: str
    inode_number: int

@dataclass
class Block:
    """디스크 블록"""
    block_number: int
    data: bytes = b''
    is_free: bool = True

@dataclass
class JournalEntry:
    """저널 엔트리"""
    sequence: int
    operation: str  # 'create', 'write', 'delete', 'rename'
    inode_number: int
    data: Dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    committed: bool = False


class SimpleFileSystem:
    """
    간단한 파일 시스템 시뮬레이터
    - Inode 기반
    - 블록 할당 관리
    - 저널링 지원
    """

    def __init__(self, total_blocks: int = 1024, block_size: int = 4096):
        self.total_blocks = total_blocks
        self.block_size = block_size

        # 디스크 블록
        self.blocks: Dict[int, Block] = {
            i: Block(i) for i in range(total_blocks)
        }

        # Inode 테이블
        self.inodes: Dict[int, Inode] = {}
        self.next_inode = 0

        # 블록 비트맵 (할당 상태)
        self.block_bitmap = [False] * total_blocks

        # 저널
        self.journal: List[JournalEntry] = []
        self.journal_sequence = 0

        # 루트 디렉터리 생성
        self._create_root()

    def _create_root(self):
        """루트 디렉터리 생성"""
        root_inode = self._allocate_inode(FileType.DIRECTORY)
        root_inode.mode = 0o755
        # 루트 디렉터리 데이터 초기화 (.와 .. 엔트리)
        self._write_directory_entries(root_inode, [
            DirectoryEntry('.', root_inode.inode_number),
            DirectoryEntry('..', root_inode.inode_number)
        ])

    def _allocate_inode(self, file_type: FileType) -> Inode:
        """새 Inode 할당"""
        inode = Inode(
            inode_number=self.next_inode,
            file_type=file_type
        )
        self.inodes[self.next_inode] = inode
        self.next_inode += 1
        return inode

    def _allocate_block(self) -> Optional[int]:
        """빈 블록 찾기"""
        for i, used in enumerate(self.block_bitmap):
            if not used:
                self.block_bitmap[i] = True
                self.blocks[i].is_free = False
                return i
        return None

    def _free_block(self, block_number: int):
        """블록 해제"""
        self.block_bitmap[block_number] = False
        self.blocks[block_number].is_free = True
        self.blocks[block_number].data = b''

    def _write_directory_entries(self, inode: Inode, entries: List[DirectoryEntry]):
        """디렉터리 엔트리 쓰기"""
        # 간단화: 엔트리를 문자열로 직렬화
        data = '\n'.join([f"{e.name}:{e.inode_number}" for e in entries]).encode()
        self._write_file_data(inode, data)

    def _read_directory_entries(self, inode: Inode) -> List[DirectoryEntry]:
        """디렉터리 엔트리 읽기"""
        data = self._read_file_data(inode)
        entries = []
        for line in data.decode().split('\n'):
            if ':' in line:
                name, ino = line.split(':')
                entries.append(DirectoryEntry(name, int(ino)))
        return entries

    def _write_file_data(self, inode: Inode, data: bytes) -> bool:
        """파일 데이터 쓰기"""
        # 저널에 기록
        self._journal_operation('write', inode.inode_number, {
            'old_size': inode.size,
            'new_size': len(data)
        })

        # 기존 블록 해제
        for block_num in inode.direct_blocks:
            if block_num is not None:
                self._free_block(block_num)
        inode.direct_blocks = [None] * 12

        # 새 블록 할당 및 데이터 쓰기
        offset = 0
        block_idx = 0
        while offset < len(data) and block_idx < 12:
            block_num = self._allocate_block()
            if block_num is None:
                return False

            chunk = data[offset:offset + self.block_size]
            self.blocks[block_num].data = chunk
            inode.direct_blocks[block_idx] = block_num

            offset += self.block_size
            block_idx += 1

        inode.size = len(data)
        inode.mtime = datetime.now()
        return True

    def _read_file_data(self, inode: Inode) -> bytes:
        """파일 데이터 읽기"""
        data = b''
        for block_num in inode.direct_blocks:
            if block_num is not None:
                data += self.blocks[block_num].data
        inode.atime = datetime.now()
        return data

    def _journal_operation(self, operation: str, inode_number: int, data: Dict):
        """저널에 작업 기록"""
        entry = JournalEntry(
            sequence=self.journal_sequence,
            operation=operation,
            inode_number=inode_number,
            data=data
        )
        self.journal.append(entry)
        self.journal_sequence += 1
        print(f"  [저널] #{entry.sequence}: {operation} inode={inode_number}")

    def create_file(self, path: str, content: bytes = b'') -> Optional[Inode]:
        """파일 생성"""
        # 경로 분석
        parent_path, name = self._split_path(path)

        # 부모 디렉터리 찾기
        parent_inode = self._resolve_path(parent_path)
        if parent_inode is None or parent_inode.file_type != FileType.DIRECTORY:
            print(f"  ❌ 부모 디렉터리 없음: {parent_path}")
            return None

        # 새 파일 Inode 생성
        new_inode = self._allocate_inode(FileType.REGULAR)

        # 저널에 기록
        self._journal_operation('create', new_inode.inode_number, {
            'name': name,
            'parent': parent_inode.inode_number
        })

        # 데이터 쓰기
        if content:
            self._write_file_data(new_inode, content)

        # 부모 디렉터리에 엔트리 추가
        entries = self._read_directory_entries(parent_inode)
        entries.append(DirectoryEntry(name, new_inode.inode_number))
        self._write_directory_entries(parent_inode, entries)

        print(f"  ✅ 파일 생성: {path} (inode={new_inode.inode_number}, 크기={new_inode.size})")
        return new_inode

    def read_file(self, path: str) -> Optional[bytes]:
        """파일 읽기"""
        inode = self._resolve_path(path)
        if inode is None or inode.file_type != FileType.REGULAR:
            print(f"  ❌ 파일 없음: {path}")
            return None

        data = self._read_file_data(inode)
        print(f"  ✅ 파일 읽기: {path} (크기={len(data)} bytes)")
        return data

    def delete_file(self, path: str) -> bool:
        """파일 삭제"""
        parent_path, name = self._split_path(path)

        parent_inode = self._resolve_path(parent_path)
        if parent_inode is None:
            return False

        # 디렉터리에서 엔트리 찾기
        entries = self._read_directory_entries(parent_inode)
        inode_number = None
        for e in entries:
            if e.name == name:
                inode_number = e.inode_number
                break

        if inode_number is None:
            return False

        inode = self.inodes[inode_number]

        # 저널에 기록
        self._journal_operation('delete', inode_number, {
            'name': name,
            'size': inode.size
        })

        # 블록 해제
        for block_num in inode.direct_blocks:
            if block_num is not None:
                self._free_block(block_num)

        # Inode 해제
        del self.inodes[inode_number]

        # 디렉터리에서 엔트리 제거
        entries = [e for e in entries if e.name != name]
        self._write_directory_entries(parent_inode, entries)

        print(f"  ✅ 파일 삭제: {path}")
        return True

    def list_directory(self, path: str) -> List[Tuple[str, str, int]]:
        """디렉터리 내용 나열"""
        inode = self._resolve_path(path)
        if inode is None or inode.file_type != FileType.DIRECTORY:
            return []

        entries = self._read_directory_entries(inode)
        result = []
        for e in entries:
            if e.inode_number in self.inodes:
                child_inode = self.inodes[e.inode_number]
                result.append((
                    e.name,
                    child_inode.file_type.value,
                    child_inode.size
                ))
        return result

    def _resolve_path(self, path: str) -> Optional[Inode]:
        """경로로 Inode 찾기"""
        if path == '/':
            return self.inodes.get(0)

        parts = [p for p in path.split('/') if p]
        current_inode = self.inodes.get(0)

        for part in parts:
            if current_inode is None:
                return None

            entries = self._read_directory_entries(current_inode)
            found = False
            for e in entries:
                if e.name == part:
                    current_inode = self.inodes.get(e.inode_number)
                    found = True
                    break

            if not found:
                return None

        return current_inode

    def _split_path(self, path: str) -> Tuple[str, str]:
        """경로를 부모 경로와 이름으로 분리"""
        if '/' not in path:
            return '/', path
        parts = path.rsplit('/', 1)
        parent = parts[0] if parts[0] else '/'
        return parent, parts[1]

    def get_stats(self) -> Dict:
        """파일 시스템 통계"""
        used_blocks = sum(self.block_bitmap)
        free_blocks = self.total_blocks - used_blocks

        return {
            'total_blocks': self.total_blocks,
            'used_blocks': used_blocks,
            'free_blocks': free_blocks,
            'total_inodes': len(self.inodes),
            'journal_entries': len(self.journal)
        }

    def recover_from_journal(self):
        """저널에서 복구"""
        print("\n=== 저널 복구 시작 ===")
        for entry in self.journal:
            if not entry.committed:
                print(f"  미완료 작업: {entry.operation} inode={entry.inode_number}")
                # 실제로는 롤백 또는 재실행 수행
                entry.committed = True
        print("=== 저널 복구 완료 ===")


# ============ 실행 예시 ============
if __name__ == "__main__":
    print("=" * 60)
    print("파일 시스템 핵심 알고리즘 시연")
    print("=" * 60)

    # 파일 시스템 생성
    fs = SimpleFileSystem(total_blocks=100, block_size=4096)

    # 1. 파일 생성 테스트
    print("\n" + "=" * 60)
    print("1. 파일 생성 및 쓰기")
    print("=" * 60)

    fs.create_file("/hello.txt", b"Hello, World!")
    fs.create_file("/data.txt", b"This is some test data." * 100)

    # 2. 디렉터리 생성 및 파일 추가
    print("\n" + "=" * 60)
    print("2. 디렉터리 생성 및 파일 추가")
    print("=" * 60)

    # documents 디렉터리 생성
    docs_inode = fs._allocate_inode(FileType.DIRECTORY)
    docs_inode.mode = 0o755

    root_entries = fs._read_directory_entries(fs.inodes[0])
    root_entries.append(DirectoryEntry("documents", docs_inode.inode_number))
    fs._write_directory_entries(fs.inodes[0], root_entries)

    fs._write_directory_entries(docs_inode, [
        DirectoryEntry('.', docs_inode.inode_number),
        DirectoryEntry('..', 0)
    ])

    # documents에 파일 생성
    fs.create_file("/documents/readme.md", b"# Readme File\n\nThis is a readme.")
    fs.create_file("/documents/notes.txt", b"My notes here...")

    # 3. 디렉터리 목록 확인
    print("\n" + "=" * 60)
    print("3. 디렉터리 목록")
    print("=" * 60)

    print("\n루트 디렉터리:")
    for name, ftype, size in fs.list_directory("/"):
        print(f"  {name:20} {ftype:15} {size:8} bytes")

    print("\n/documents 디렉터리:")
    for name, ftype, size in fs.list_directory("/documents"):
        print(f"  {name:20} {ftype:15} {size:8} bytes")

    # 4. 파일 읽기
    print("\n" + "=" * 60)
    print("4. 파일 읽기")
    print("=" * 60)

    content = fs.read_file("/hello.txt")
    if content:
        print(f"  내용: {content.decode()}")

    # 5. 파일 삭제
    print("\n" + "=" * 60)
    print("5. 파일 삭제")
    print("=" * 60)

    fs.delete_file("/data.txt")
    print("\n삭제 후 루트 디렉터리:")
    for name, ftype, size in fs.list_directory("/"):
        print(f"  {name:20} {ftype:15} {size:8} bytes")

    # 6. 파일 시스템 통계
    print("\n" + "=" * 60)
    print("6. 파일 시스템 통계")
    print("=" * 60)

    stats = fs.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # 7. 저널 확인
    print("\n" + "=" * 60)
    print("7. 저널 엔트리")
    print("=" * 60)

    for entry in fs.journal[:5]:  # 처음 5개만
        print(f"  #{entry.sequence}: {entry.operation} - inode {entry.inode_number}")

    print("\n" + "=" * 60)
    print("시연 완료")
    print("=" * 60)
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| 장점 | 단점 |
|-----|------|
| **데이터 체계적 관리**: 파일 이름으로 직관적 접근 | **단편화 문제**: 내부/외부 단편화로 공간 낭비 |
| **효율적 공간 활용**: 블록 할당으로 디스크 최적화 | **오버헤드**: Inode, 메타데이터, 저널링 비용 |
| **데이터 무결성**: 저널링, COW로 크래시 복구 | **복구 어려움**: 삭제/손상 시 데이터 복구 복잡 |

**대안 기술 비교** (필수: 최소 2개 대안):
| 비교 항목 | ext4 | XFS | ZFS | Btrfs |
|---------|------|-----|-----|-------|
| **핵심 특성** | 저널링, 안정적 | 고성능, 대용량 | COW, 무결성 | COW, 스냅샷 |
| **최대 볼륨** | 1EB | 8EB | 256TB(ZPOOL) | 16EB |
| **최대 파일** | 16TB | 8EB | 16EB | 16EB |
| **스냅샷** | ❌ | ❌ | ★ 지원 | ★ 지원 |
| **중복 제거** | ❌ | ❌ | ★ 지원 | 지원 |
| **RAID** | 별도 | 별도 | ★ 내장 | 내장 |
| **적합 환경** | 일반 Linux | 대용량 서버 | NAS/Enterprise | 최신 Linux |

> **★ 선택 기준**: 일반 서버 → **ext4**, 대용량/고성능 → **XFS**, 데이터 무결성 최우선 → **ZFS**, 최신 기능/스냅샷 → **Btrfs**.

**디스크 할당 방식 비교**:
| 할당 방식 | 순차 접근 | 직접 접근 | 단편화 | 적합 용도 |
|---------|---------|---------|--------|----------|
| 연속 할당 | ★ 최적 | ★ 최적 | 외부 심각 | CD-ROM, DVD |
| 연결 할당 | 양호 | ❌ 불가 | 외부 없음 | 구형 시스템 |
| FAT | 양호 | 느림 | 외부 있음 | USB, SD카드 |
| Inode (색인) | 양호 | ★ 양호 | 내부 있음 | ext4, XFS |

**기술 진화 계보** (해당 시):
```
FAT (1980) → ext2 (1993) → ext3 (저널링, 2001) → ext4 (extents, 2008)
                                              ↓
                            ZFS (COW, 2005) → Btrfs (2009)
                                              ↓
                            분산 파일 시스템: GFS, HDFS, Ceph
```

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **데이터베이스 서버** | XFS 사용, stripe size 튜닝, Direct I/O | IOPS 40% 향상, 지연 시간 30% 단축 |
| **컨테이너 플랫폼** | OverlayFS 레이어 최적화, 이미지 스냅샷 활용 | 이미지 풀 시간 60% 단축 |
| **NAS/스토리지** | ZFS RAID-Z + 스냅샷 + 중복 제거 | 스토리지 효율 50% 향상, 백업 시간 90% 단축 |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1: Facebook/Meta** - XFS를 메인 파일 시스템으로 사용. 수십억 개의 사진을 저장하는 Haystack 시스템. XFS의 대용량 파일 처리와 extent 기반 할당으로 성능 최적화.
- **사례 2: Netflix** - AWS EC2에서 XFS 사용. 대용량 비디오 스트리밍 데이터 처리. 4KB~1MB 다양한 파일 크기에 최적화된 성능.
- **사례 3: Docker** - OverlayFS를 기본 스토리지 드라이버로 사용. 컨테이너 이미지 레이어를 효율적으로 관리. Copy-on-Write로 디스크 공간 절약.

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**: 파일 시스템 선택(ext4 vs XFS vs ZFS), 블록 크기, 저널링 모드, 마운트 옵션
2. **운영적**: 백업 전략, 스냅샷 정책, quota 관리, fsck 주기
3. **보안적**: 파일 권한(ACL), 암호화(dmcrypt), SELinux 컨텍스트
4. **경제적**: 스토리지 비용 vs 성능, 압축/중복제거 ROI, 백업 스토리지 비용

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ **Inode 고갈**: 디스크 공간은 남았는데 Inode가 부족. 작은 파일 많은 시스템에서 주의.
- ❌ **저널링 비활성화**: 성능을 위해 저널 끄면 크래시 시 데이터 손실 위험.
- ❌ **잘못된 블록 크기**: 워크로드에 맞지 않는 블록 크기 선택 시 성능 저하.

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 파일 시스템 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  [파일 시스템] 핵심 연관 개념 맵                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [메모리 관리] ←──→ [파일 시스템] ←──→ [I/O 시스템]            │
│        ↓                  ↓                ↓                    │
│   [mmap]           [Inode/블록]         [버퍼 캐시]            │
│        ↓                  ↓                ↓                    │
│   [가상 메모리]    [저널링]           [RAID]                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 메모리 관리 | 연동 | mmap, 버퍼 캐시, 페이지 캐시 공유 | `[memory](./memory.md)` |
| I/O 시스템 | 하위 계층 | 디스크 드라이버, I/O 스케줄링 | `[file_descriptor](./file_descriptor.md)` |
| 동기화 | 함께 사용 | 파일 Lock, 동시 쓰기 제어 | `[synchronization](./synchronization.md)` |
| 교착상태 | 부작용 | 파일 Lock 순서로 교착상태 가능 | `[deadlock](./deadlock.md)` |
| 프로세스 | 사용자 | 파일 시스템 호출의 주체 | `[process](./process.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **데이터 무결성** | 저널링/COW로 크래시 복구 | 데이터 손실 0건 |
| **저장 효율** | 블록 할당 최적화, 압축 | 스토리지 활용률 90% 이상 |
| **접근 성능** | 캐시 활용, 적절한 할당 방식 | IOPS 30% 향상 |
| **관리 편의성** | 스냅샷, 백업 통합 | 백업 시간 80% 단축 |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**: NVMe 최적화 파일 시스템, Persistent Memory용 파일 시스템(NVDIMM), 분산 파일 시스템(Ceph, GlusterFS) 확산.
2. **시장 트렌드**: 오브젝트 스토리지(S3)와 파일 시스템의 경계 모호화, 컨테이너 네이티브 스토리지.
3. **후속 기술**: 벡터 파일 시스템(AI 워크로드용), 양자 내성 암호화 파일 시스템.

> **결론**: 파일 시스템은 운영체제의 핵심 구성 요소로, 데이터의 체계적 관리와 효율적 저장을 담당한다. 현대 파일 시스템은 저널링, Copy-on-Write, 스냅샷 등의 기능으로 데이터 무결성과 관리 편의성을 크게 개선했다. 워크로드 특성에 맞는 파일 시스템 선택(ext4/XFS/ZFS)과 튜닝이 성능과 안정성을 결정한다. 향후 NVMe, Persistent Memory, 분산 스토리지 환경에서 새로운 파일 시스템 기술이 요구된다.

> **※ 참고 표준**: POSIX File System Interfaces (IEEE 1003.1), ext4 Kernel Documentation, XFS Design, ZFS On Linux

---

## 어린이를 위한 종합 설명 (필수)

**파일 시스템을(를) 아주 쉬운 비유로 한 번 더 정리합니다.**

파일 시스템은 마치 **도서관 분류 시스템** 같아요.

도서관에는 수만 권의 책이 있어요. 이 책들을 아무 데나 두면 찾을 수가 없겠죠? 그래서 도서관은 체계적인 시스템을 만들었어요.

**핵심 아이디어들:**

1. **책(=파일)**: 우리가 저장하는 데이터예요. 사진, 문서, 동영상 모두 파일이에요.

2. **책장(=디렉터리)**: 책을 주제별로 정리하는 곳이에요. "과학", "역사", "소설"처럼요.

3. **도서 카드(=Inode)**: 책의 모든 정보가 적혀 있어요. 책 제목은 없지만, 어디에 있는지, 얼마나 큰지, 누가 읽을 수 있는지가 적혀 있어요.

4. **책 위치(=블록)**: 도서 카드를 보고 책장에서 책을 찾아요. 책은 여러 페이지로 나뉘어 여러 곳에 있을 수 있어요.

5. **작업 일지(=저널)**: 사서님이 무슨 일을 했는지 적어두는 공책이에요. 도서관에 불이 나도, 작업 일지를 보고 복구할 수 있어요!

**파일 시스템 덕분에:**
- 파일 이름으로 쉽게 찾을 수 있어요
- 다른 사람이 내 파일을 못 보게 할 수 있어요
- 컴퓨터가 꺼져도 파일이 사라지지 않아요

---

## ✅ 작성 완료 체크리스트

### 구조 체크
- [x] 핵심 인사이트 3줄 요약
- [x] Ⅰ. 개요: 개념 + 비유 + 등장배경(3가지)
- [x] Ⅱ. 구성요소: 표(4개 이상) + 다이어그램 + 단계별 동작 + 코드
- [x] Ⅲ. 비교: 장단점 표 + 대안 비교표 + 선택 기준
- [x] Ⅳ. 실무: 적용 시나리오(3개) + 실제 사례 + 고려사항(4가지) + 주의사항(3개)
- [x] Ⅴ. 결론: 정량 효과 표 + 미래 전망(3가지) + 참고 표준
- [x] 관련 개념: 5개 이상 나열 + 개념 맵 + 상호 링크
- [x] 어린이를 위한 종합 설명

### 품질 체크
- [x] 모든 표이 채워져 있음 (빈 칸 없음)
- [x] ASCII 다이어그램이 실제 구조를 잘 표현
- [x] 코드 예시가 실제 동작 가능한 수준
- [x] 정량적 수치가 포함됨 (XX% 향상 등)
- [x] 실제 기업/서비스 사례가 구체적으로 기재됨
- [x] 관련 표준/가이드라인이 인용됨
