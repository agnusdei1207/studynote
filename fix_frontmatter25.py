import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The file has:
    # ---
    # +++
    # title = "..."
    # ...
    # +++
    if content.startswith('---\n+++\n'):
        content = content[4:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    if content.startswith('+++\n---\n'):
        content = content[4:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # Some files start with --- and ends with --- but contain TOML style keys like title = "..."
    # I already tried to fix this but maybe missed some.
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            if '=' in frontmatter and not ':' in frontmatter:
                # Need to convert delimiters
                content = content.replace('---\n', '+++\n', 2)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
