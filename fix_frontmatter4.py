import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # YAML 로 통일하기
            frontmatter = re.sub(r'^([a-zA-Z_]+)\s*=\s*(.*)$', r'\1: \2', frontmatter, flags=re.MULTILINE)
            
            # extra: 아래의 것들을 들여쓰기
            lines = frontmatter.split('\n')
            in_extra = False
            for i in range(len(lines)):
                if lines[i].strip() == 'extra:':
                    in_extra = True
                    continue
                if in_extra and lines[i].strip() != '':
                    if not lines[i].startswith(' '):
                        lines[i] = '  ' + lines[i]
            
            frontmatter = '\n'.join(lines)
            
            new_content = f'---{frontmatter}---{body}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
    elif content.startswith('+++'):
        parts = content.split('+++', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # TOML 형식 유지하되 ':' 로 된 것은 '=' 로 고치기
            # 그리고 extra: 를 [extra] 로 고치기
            frontmatter = frontmatter.replace('extra:\n', '[extra]\n')
            frontmatter = re.sub(r'^([a-zA-Z_]+)\s*:\s*(.*)$', r'\1 = \2', frontmatter, flags=re.MULTILINE)
            
            new_content = f'+++{frontmatter}+++{body}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
