import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Zola parser strictly checks the first line.
    # If the file starts with `---` but it's formatted like TOML, it fails.
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # Check if it looks like TOML (contains '=')
            if '=' in frontmatter and not ':' in frontmatter:
                # It's TOML disguised as YAML
                new_content = f'+++{frontmatter}+++{body}'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
