import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if content.startswith('---\n+++'):
        new_content = content.replace('---\n+++', '+++', 1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    elif content.startswith('+++\n---'):
        new_content = content.replace('+++\n---', '+++', 1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    elif content.startswith('---\n---'):
        new_content = content.replace('---\n---', '---', 1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    elif content.startswith('+++\n+++'):
        new_content = content.replace('+++\n+++', '+++', 1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
