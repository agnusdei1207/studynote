import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---\n'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            if '[extra]' in frontmatter:
                # YAML front matter with [extra] is invalid for Zola. 
                # Zola requires YAML to have nested structure for extra
                # e.g. 
                # extra:
                #   subject: "DevOps"
                
                new_frontmatter = frontmatter.replace('[extra]', 'extra:')
                # Add two spaces before lines after extra:
                lines = new_frontmatter.split('\n')
                in_extra = False
                for i in range(len(lines)):
                    if lines[i].strip() == 'extra:':
                        in_extra = True
                        continue
                    if in_extra and lines[i].strip() != '' and not lines[i].startswith(' '):
                        if ':' in lines[i]:
                            lines[i] = '  ' + lines[i]
                        else:
                            in_extra = False
                
                new_frontmatter = '\n'.join(lines)
                new_content = f'---{new_frontmatter}---{body}'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
