import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Sometimes files start with --- but end with +++ or vice versa, but we missed it.
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            pass
        else:
            # Let's completely replace the first --- with +++ if there's a +++ ending
            if '+++' in content:
                content = content.replace('---', '+++', 1)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
