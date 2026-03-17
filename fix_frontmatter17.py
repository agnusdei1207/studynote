import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Zola is complaining because SOME files still have mismatched delimiters.
    # Let's forcibly ensure that if the frontmatter contains `=`, it uses `+++` on BOTH sides.
    # And if it contains ONLY `:`, it uses `---` on BOTH sides.
    
    # Check for anything that starts with `---` or `+++`
    lines = content.split('\n')
    if len(lines) > 2 and (lines[0] == '---' or lines[0] == '+++'):
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i] == '---' or lines[i] == '+++':
                end_idx = i
                break
        
        if end_idx != -1:
            fm_lines = lines[1:end_idx]
            has_eq = any('=' in line and not line.strip().startswith('[') for line in fm_lines)
            
            if has_eq:
                # Force TOML
                lines[0] = '+++'
                lines[end_idx] = '+++'
            else:
                # Force YAML
                lines[0] = '---'
                lines[end_idx] = '---'
                
            new_content = '\n'.join(lines)
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
