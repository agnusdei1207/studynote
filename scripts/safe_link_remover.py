import os
import glob
import re

def remove_links_safely(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Front Matter와 본문 분리
    if not content.startswith('+++') and not content.startswith('---'):
        return # Skip files without FM
        
    delim = '+++' if content.startswith('+++') else '---'
    parts = content.split(delim, 2)
    if len(parts) < 3: return
    
    fm = parts[1]
    body = parts[2]
    
    # 2. 본문에서만 링크 제거
    # [text](url) -> text
    new_body = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', body)
    
    if new_body != body:
        new_content = f'{delim}{fm}{delim}{new_body}'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

# 스터디 노트 파일들만 대상으로 안전하게 처리
for filepath in glob.glob('content/studynote/**/*.md', recursive=True):
    if '_index.md' in filepath: continue
    remove_links_safely(filepath)
