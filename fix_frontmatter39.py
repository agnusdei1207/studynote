import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove leading whitespaces/newlines and any ``` or ```markdown or ```toml etc.
    # basically anything that is before the first +++ or ---
    
    # regex to find the first +++ or --- and strip anything before it
    match = re.search(r'^(\+\+\+|---)', content, flags=re.MULTILINE)
    if match:
        start_idx = match.start()
        if start_idx > 0:
            # We found garbage before the first frontmatter delimiter
            cleaned_content = content[start_idx:]
            
            # also if the file ends with ```, strip it
            if cleaned_content.rstrip().endswith('```'):
                cleaned_content = cleaned_content.rstrip()[:-3].rstrip()
                
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
