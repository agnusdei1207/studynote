import os
import glob
import re

def clean_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception: return

    # 1. 모든 내부 링크 제거
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', content)

    # 2. 본문 분리 (마크다운 특수문자 기준)
    content = content.lstrip()
    body_match = re.search(r'\n(#+ |> |📢 |Ⅰ\. |Ⅱ\. |Ⅲ\. |Ⅳ\. |Ⅴ\. )', content)
    
    if body_match:
        potential_fm = content[:body_match.start()]
        body_part = content[body_match.start():].strip()
    else:
        potential_fm = ""
        body_part = content.strip()

    # 3. 메타데이터 정밀 정제 (유효한 키-값만 추출)
    fm_map = {}
    extra_map = {}
    in_extra = False
    
    # 찌꺼기 및 AI 태그 제거
    potential_fm = re.sub(r'<[^>]+>', '', potential_fm)
    potential_fm = potential_fm.replace('+++', '').replace('---', '').replace('```markdown', '').replace('```', '')
    
    for line in potential_fm.split('\n'):
        line = line.strip()
        if not line: continue
        
        if line.lower() in ['[extra]', 'extra:', 'extra']:
            in_extra = True
            continue
            
        if '=' in line or ':' in line:
            p = re.split(r'[=:]', line, maxsplit=1)
            key = p[0].strip().lower()
            val = p[1].strip()
            
            # 유효한 키(영문+숫자+언더바)만 수용
            if re.match(r'^[a-z0-9_]+$', key):
                if in_extra: extra_map[key] = val
                else: fm_map[key] = val

    # 필수 값 보정
    title = fm_map.get('title', "").strip('"')
    if not title:
        for b_line in body_part.split('\n'):
            if b_line.startswith('# '):
                title = b_line[2:].strip().replace('"', '')
                break
    if not title: title = "Untitled Note"
    
    date = fm_map.get('date', '"2026-03-14"').strip('"')
    weight = fm_map.get('weight', None)

    # 4. 순수 TOML 재구성
    new_fm = []
    new_fm.append(f'title = "{title}"')
    new_fm.append(f'date = "{date}"')
    if weight: new_fm.append(f'weight = {weight}')
    
    if extra_map or 'subject' in fm_map:
        new_fm.append('[extra]')
        if 'subject' in fm_map:
            new_fm.append(f'subject = {fm_map["subject"]}')
        for ek, ev in extra_map.items():
            if ek != 'subject': # 중복 방지
                new_fm.append(f'{ek} = {ev}')

    # 5. 저장
    final_content = f'+++\n' + '\n'.join(new_fm) + f'\n+++\n\n' + body_part
    if final_content.rstrip().endswith('```'):
        final_content = final_content.rstrip()[:-3].rstrip()

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    if '_index.md' in filepath: continue
    clean_file(filepath)
