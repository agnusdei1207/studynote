import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find ALL files that start with --- (with or without leading spaces/newlines)
    # and have `=` inside the first block before the closing ---
    
    # Strip leading whitespace completely
    orig_content = content
    content = content.lstrip()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            if '=' in fm and ':' not in fm:
                # This is TOML disguised as YAML
                new_content = f'+++{fm}+++{parts[2]}'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
