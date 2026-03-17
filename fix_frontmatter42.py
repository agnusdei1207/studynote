import os
import glob

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Many files have --- followed by TOML `key = "value"`
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            if '=' in fm and ':' not in fm:
                # Replace the '---' with '+++'
                content = content.replace('---', '+++', 2)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
