import os
import glob
import re

def robust_fix(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 파일 앞부분의 불필요한 공백, 개행, 마크다운 코드 블록 태그 제거
    content = content.lstrip()
    content = re.sub(r'^```(markdown|toml|yaml)?\n', '', content, flags=re.IGNORECASE)
    
    # 2. Front Matter 추출 시도 (+++ 또는 ---)
    # 가장 먼저 나오는 구분자를 찾음
    match = re.search(r'^(\+\+\+|---)', content)
    if not match:
        # Front Matter가 아예 없는 경우: 제목을 추출해서 생성
        title = "Untitled"
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        new_header = f'+++\ntitle = "{title}"\ndate = "2026-03-14"\n[extra]\nsubject = "General"\n+++\n\n'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_header + content)
        return

    # 구분자 유형 (+++ 또는 ---)
    delim = match.group(1)
    # 시작점 이전의 모든 데이터 삭제
    content = content[match.start():]
    
    # 닫는 구분자 찾기
    parts = content.split(delim, 2)
    if len(parts) < 3:
        # 닫는 구분자가 없는 경우 (예: +++만 있고 끝남)
        # 본문 시작(보통 # 또는 ##) 전까지를 Front Matter로 간주
        body_match = re.search(r'\n#+ ', content)
        if body_match:
            fm_part = content[:body_match.start()].replace(delim, '').strip()
            body_part = content[body_match.start():].strip()
            # 무조건 TOML(+++)로 재구성
            new_content = f'+++\n{fm_part}\n+++\n\n{body_part}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        return

    fm_part = parts[1].strip()
    body_part = parts[2].lstrip()

    # 3. 내부 형식 정제 (YAML/TOML 혼용 방지)
    # Zola는 [extra]를 사용할 때 TOML(+++)을 선호함. 무조건 TOML로 변환.
    lines = fm_part.split('\n')
    new_fm_lines = []
    has_extra = False
    
    for line in lines:
        line = line.strip()
        if not line: continue
        if line == '[extra]' or line == 'extra:':
            has_extra = True
            new_fm_lines.append('[extra]')
            continue
        
        # 'key: value' -> 'key = value'
        if ':' in line and '=' not in line and not line.startswith('['):
            line = re.sub(r'^([a-zA-Z_]+)\s*:\s*(.*)$', r'\1 = \2', line)
        
        # 'key=value' -> 'key = value' (공백 추가)
        if '=' in line and ' = ' not in line and not line.startswith('['):
            line = line.replace('=', ' = ', 1)
            
        new_fm_lines.append(line)

    # 필수 필드 보정
    fm_str = '\n'.join(new_fm_lines)
    if 'title =' not in fm_str:
        # 제목이 없으면 본문 첫 줄에서 가져옴
        title = "Untitled"
        for line in body_part.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip().replace('"', '\\"')
                break
        new_fm_lines.insert(0, f'title = "{title}"')
    
    if 'date =' not in fm_str:
        new_fm_lines.append('date = "2026-03-14"')

    # 4. 최종 저장 (무조건 +++ 구분자 사용)
    final_content = f'+++\n' + '\n'.join(new_fm_lines) + f'\n+++\n\n' + body_part
    
    # 마지막에 ``` 가 남는 경우 제거
    if final_content.rstrip().endswith('```'):
        final_content = final_content.rstrip()[:-3].rstrip()

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

# 모든 마크다운 파일에 대해 실행
for filepath in glob.glob('content/**/*.md', recursive=True):
    if '_index.md' in filepath: continue # _index.md는 별도 관리
    robust_fix(filepath)
