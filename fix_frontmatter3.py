import os
import glob
import re

def fix_frontmatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('+++'):
        parts = content.split('+++', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # YAML -> TOML 로 변환해야 함 (+++ 면)
            frontmatter = re.sub(r'^([a-zA-Z_]+)\s*:\s*(.*)$', r'\1 = \2', frontmatter, flags=re.MULTILINE)
            
            new_content = f'+++{frontmatter}+++{body}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
    elif content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # YAML 로 통일하기
            frontmatter = re.sub(r'^([a-zA-Z_]+)\s*=\s*(.*)$', r'\1: \2', frontmatter, flags=re.MULTILINE)
            
            new_content = f'---{frontmatter}---{body}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_frontmatter(filepath)
