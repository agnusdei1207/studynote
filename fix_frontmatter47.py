import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content
    content = content.lstrip()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            if '=' in fm and ':' not in fm:
                new_content = f'+++{fm}+++{parts[2]}'
                if new_content != orig_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
