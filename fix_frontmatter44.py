import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # If the file doesn't start with +++ or ---, but has it somewhere, it means there's garbage at the top.
    if not content.startswith('+++') and not content.startswith('---'):
        match = re.search(r'^(\+\+\+|---)\n', content, flags=re.MULTILINE)
        if match:
            start_idx = match.start()
            cleaned_content = content[start_idx:]
            
            # also if the file ends with ```, strip it
            if cleaned_content.rstrip().endswith('```'):
                cleaned_content = cleaned_content.rstrip()[:-3].rstrip()
                
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
