import os
import glob

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Again, somehow these YAML-TOML hybrids escaped the previous fixes.
    # Just force anything with [extra] in YAML blocks to +++ blocks.
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            if '[extra]' in frontmatter:
                content = content.replace('---', '+++', 2)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            elif '=' in frontmatter and ':' not in frontmatter:
                content = content.replace('---', '+++', 2)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
