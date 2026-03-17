import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Some files somehow still have mismatched or corrupted delimiters
    # Let's clean it up thoroughly by recreating front matter correctly.
    if content.startswith('---\n') or content.startswith('+++\n'):
        # Split by the first delimiter and the second delimiter
        lines = content.split('\n')
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i] == '---' or lines[i] == '+++':
                end_idx = i
                break
        
        if end_idx != -1:
            fm_lines = lines[1:end_idx]
            
            # Check for corrupted lines like "+++ title = "
            for i, line in enumerate(fm_lines):
                if line.startswith('+++'):
                    fm_lines[i] = line[3:].strip()
                if line.startswith('---'):
                    fm_lines[i] = line[3:].strip()

            new_content = '+++\n' + '\n'.join(fm_lines) + '\n+++\n' + '\n'.join(lines[end_idx+1:])
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
