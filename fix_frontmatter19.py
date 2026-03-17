import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Some files don't have properly closed frontmatter. They have +++ at the start, and then the content starts without a closing +++.
    if content.startswith('+++'):
        # Check if the second +++ exists
        parts = content.split('+++', 2)
        if len(parts) == 3:
            # Check if the frontmatter part contains markdown headers (like # 527. ...)
            # If so, it means the closing +++ was missed or placed too far down.
            fm = parts[1]
            if '\n# ' in fm:
                # the frontmatter is actually mixed with body
                # Let's try to extract proper frontmatter
                lines = fm.split('\n')
                actual_fm = []
                body_start_idx = -1
                for i, line in enumerate(lines):
                    if line.startswith('# '):
                        body_start_idx = i
                        break
                    if line.strip() != '':
                        actual_fm.append(line)
                
                if body_start_idx != -1:
                    new_fm = '\n'.join(actual_fm)
                    new_body = '\n'.join(lines[body_start_idx:]) + '\n' + parts[2]
                    
                    # Ensure basic fields exist
                    if 'date =' not in new_fm:
                        new_fm += '\ndate = "2026-03-14"'
                        
                    new_content = f'+++\n{new_fm}\n+++\n\n{new_body}'
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
