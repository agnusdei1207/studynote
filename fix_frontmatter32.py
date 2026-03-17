import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Some files have +++ followed by trailing spaces like "+++  \n"
    if content.startswith('+++ '):
        content = re.sub(r'^\+\+\+[ \t]+', '+++', content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    # Same for closing delimiter "+++  \n" -> "+++\n"
    content = re.sub(r'\n\+\+\+[ \t]+\n', '\n+++\n', content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
