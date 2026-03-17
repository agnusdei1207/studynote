import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Sometimes files start with --- but end with +++
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            pass # pure yaml or toml wrapped in yaml
        else:
            # maybe it closes with +++
            parts2 = content.split('+++', 1)
            if len(parts2) >= 2 and parts2[0].startswith('---\n'):
                new_content = '+++' + content[3:]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
