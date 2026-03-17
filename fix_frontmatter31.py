import os
import glob

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Some files still have --- wrapper around TOML
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            if '=' in frontmatter and not ':' in frontmatter:
                # It's TOML disguised as YAML
                new_content = content.replace('---', '+++', 2)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            elif '[extra]' in frontmatter:
                new_content = content.replace('---', '+++', 2)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
