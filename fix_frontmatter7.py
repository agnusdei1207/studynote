import os
import glob

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('\n---'):
        content = content.replace('\n---', '---', 1)
    if content.startswith('\n+++'):
        content = content.replace('\n+++', '+++', 1)

    if content.startswith('---\n'):
        # Find closing
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            pass # pure yaml
        else:
            # maybe it closes with +++
            parts2 = content.split('+++\n', 1)
            if len(parts2) == 2 and parts2[0].startswith('---\n'):
                # mismatched
                content = '+++' + content[3:]
                
    if content.startswith('+++\n'):
        # Find closing
        parts = content.split('+++\n', 2)
        if len(parts) >= 3:
            pass # pure toml
        else:
            # maybe it closes with ---
            parts2 = content.split('---\n', 1)
            if len(parts2) == 2 and parts2[0].startswith('+++\n'):
                # mismatched
                content = content.replace('---\n', '+++\n', 1)
                
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
