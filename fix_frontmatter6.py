import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if content.startswith('+++'):
        parts = content.split('+++', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # YAML -> TOML : 를 = 로 변경
            lines = frontmatter.split('\n')
            for i in range(len(lines)):
                if ':' in lines[i] and not lines[i].strip().startswith('[') and '=' not in lines[i]:
                    lines[i] = re.sub(r'^([a-zA-Z_]+)\s*:\s*(.*)$', r'\1 = \2', lines[i])
            
            frontmatter = '\n'.join(lines)
            
            new_content = f'+++{frontmatter}+++{body}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
