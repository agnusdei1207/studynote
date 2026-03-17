import os
import glob

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Some files still have ---\n as wrapper for what is actually TOML
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            if '=' in frontmatter and not ':' in frontmatter:
                # IT's actually TOML
                new_content = f'+++\n{frontmatter}+++\n{body}'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            elif '[extra]' in frontmatter:
                # also TOML but probably mixed
                new_frontmatter = frontmatter.replace(':', '=')
                new_content = f'+++\n{new_frontmatter}+++\n{body}'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
