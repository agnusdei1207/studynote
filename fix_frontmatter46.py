import os
import glob

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content
    content = content.lstrip()
    
    # Sometimes files have:
    # ---
    # +++
    # title = "..."
    # ...
    # +++
    # ---
    # We should just regex search for the first `+++` and its closing `+++` and strip outer `---`
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            if '+++' in fm:
                # it's nested
                fm_clean = fm.replace('+++', '').strip()
                new_content = f'+++\n{fm_clean}\n+++\n{parts[2].lstrip()}'
                if new_content != orig_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            elif '=' in fm and ':' not in fm:
                new_content = f'+++\n{fm.strip()}\n+++\n{parts[2].lstrip()}'
                if new_content != orig_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
