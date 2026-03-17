import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The file has:
    # +++
    # [PE GUIDELINE]
    # date = "2026-03-14"
    # +++
    # It seems the file was overwritten with PE_GUIDELINE content somehow.
    # We should restore basic front matter if it's completely broken like this.
    if '[PE GUIDELINE]' in content[:100] and '+++' in content[:10]:
        title = "Title Placeholder"
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        new_fm = f'+++\ntitle = "{title}"\ndate = "2026-03-14"\n[extra]\n+++\n'
        parts = content.split('+++', 2)
        if len(parts) >= 3:
            body = parts[2]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_fm + body)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
