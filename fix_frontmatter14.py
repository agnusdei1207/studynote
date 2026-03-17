import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Some files still have ---\n as wrapper for what is actually TOML
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # If it has = but not :, it's TOML
            if '=' in frontmatter and not ':' in frontmatter:
                new_content = f'+++{frontmatter}+++{body}'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            elif '[extra]' in frontmatter:
                new_frontmatter = frontmatter.replace(':', '=')
                new_content = f'+++{new_frontmatter}+++{body}'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
