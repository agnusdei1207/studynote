import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Zola front matter parsing
    if not (content.startswith('+++') or content.startswith('---')):
        # No front matter found
        # Extract title from first H1 or first line
        title = "Title"
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Add basic TOML front matter
        frontmatter = f'''+++
title = "{title}"
date = "2026-03-14"
[extra]
subject = "Unknown"
+++
'''
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
