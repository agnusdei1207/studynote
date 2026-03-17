import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # strip leading empty lines and spaces
    content = content.lstrip()

    # if it starts with --- but ends frontmatter with +++
    if content.startswith('---'):
        parts = content.split('+++', 1)
        if len(parts) >= 2 and 'title =' in parts[0]:
            # This is definitely TOML with a wrong opening delimiter
            content = '+++' + content[3:]
            
            # ensure [extra] is present if categories/tags are
            fm_parts = content.split('+++', 2)
            if len(fm_parts) >= 3:
                fm = fm_parts[1]
                if 'categories' in fm or 'tags' in fm:
                    if '[extra]' not in fm:
                        lines = fm.split('\n')
                        new_lines = []
                        added_extra = False
                        for line in lines:
                            if ('categories' in line or 'tags' in line) and not added_extra:
                                new_lines.append('[extra]')
                                added_extra = True
                            new_lines.append(line)
                        fm = '\n'.join(new_lines)
                content = f'+++{fm}+++{fm_parts[2]}'
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
