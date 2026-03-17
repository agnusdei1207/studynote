import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 맨 앞에 있는 빈 줄이나 ```markdown 을 제거
    if content.startswith('\n'):
        content = content.lstrip('\n')
    
    if content.startswith('```markdown\n'):
        content = content[12:]
        if content.endswith('```\n'):
            content = content[:-4]
        elif content.endswith('```'):
            content = content[:-3]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
