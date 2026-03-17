import os
import glob

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Some files still have ---\n at the beginning, but end with +++ or have TOML syntax
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            if '=' in frontmatter and not ':' in frontmatter:
                # Replace the first two ---\n with +++\n
                content = content.replace('---\n', '+++\n', 2)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
        else:
            parts2 = content.split('+++\n', 1)
            if len(parts2) >= 2 and parts2[0].startswith('---\n'):
                content = content.replace('---\n', '+++\n', 1)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
