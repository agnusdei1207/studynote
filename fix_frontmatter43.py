import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The file has:
    # ---
    # +++
    # title = "..."
    # ...
    # +++
    # OR 
    # +++
    # ---
    # title = "..."
    # ---
    
    if content.startswith('---\n+++\n'):
        content = content[4:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    if content.startswith('+++\n---\n'):
        content = content[4:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            fm = parts[1]
            if '+++' in fm:
                # Remove the inner +++
                fm = fm.replace('+++', '')
                fm = fm.replace('\n\n', '\n')
                new_content = f'+++\n{fm}+++\n{parts[2]}'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
