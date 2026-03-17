import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Zola front matter parsing can be tricky. Let's force everything to valid TOML.
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # Full YAML block
            frontmatter = parts[1]
            body = parts[2]
            
            # YAML to TOML mapping manually
            lines = frontmatter.split('\n')
            new_lines = []
            for line in lines:
                if ':' in line and not line.strip().startswith('[') and not line.strip().startswith('extra'):
                    # Replace first : with =
                    line = line.replace(':', '=', 1)
                new_lines.append(line)
            
            frontmatter = '\n'.join(new_lines)
            
            # Change 'extra:' or '[extra]' or 'extra=' to '[extra]'
            frontmatter = re.sub(r'^extra[\s:=]*$', '[extra]', frontmatter, flags=re.MULTILINE)
            
            new_content = f'+++{frontmatter}+++{body}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
    elif content.startswith('+++'):
        parts = content.split('+++', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            lines = frontmatter.split('\n')
            new_lines = []
            for line in lines:
                if ':' in line and not line.strip().startswith('[') and not line.strip().startswith('extra') and '=' not in line:
                    # Replace first : with =
                    line = line.replace(':', '=', 1)
                new_lines.append(line)
            
            frontmatter = '\n'.join(new_lines)
            
            # Change 'extra:' or 'extra=' to '[extra]'
            frontmatter = re.sub(r'^extra[\s:=]*$', '[extra]', frontmatter, flags=re.MULTILINE)
            
            new_content = f'+++{frontmatter}+++{body}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
