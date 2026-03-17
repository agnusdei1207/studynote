import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Zola YAML is --- and TOML is +++
    # There are still some files with --- that contain `title = "..."`
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            if '=' in frontmatter and not ':' in frontmatter:
                # It's TOML disguised as YAML. Zola will fail.
                new_content = content.replace('---', '+++', 2)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            elif '[extra]' in frontmatter:
                # Another case of TOML
                new_content = content.replace('---', '+++', 2)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
    elif content.startswith('+++'):
        parts = content.split('+++', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            # Check if TOML has colons which it shouldn't for key-value unless it's a string
            # Just ensure no `key: value` exists outside of strings.
            # Easiest is just checking if it contains `extra:` instead of `[extra]`
            if 'extra:\n' in frontmatter:
                new_fm = frontmatter.replace('extra:\n', '[extra]\n')
                # Also replace `: ` with ` = `
                new_fm = re.sub(r'^([a-zA-Z_]+)\s*:\s*(.*)$', r'\1 = \2', new_fm, flags=re.MULTILINE)
                new_content = f'+++{new_fm}+++{parts[2]}'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
