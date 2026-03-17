import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Many files seem to have `+++` wrapper but still fail because of `key= value` without spaces or something, 
    # but actually the error says `YAML deserialize error: Error("invalid type: string "+++ title= ... +++"`
    # This means Zola thinks the file is YAML because it either has `---` somewhere or Zola's TOML parser failed and fell back to YAML parsing on the whole string.
    # Actually, if the file starts with `\n+++` or ` +++` or similar, Zola might not recognize it as TOML.
    
    # Let's ensure the file starts exactly with `+++\n` with no leading space or newline.
    if content.lstrip().startswith('+++'):
        content = content.lstrip()
        
        # Split by `+++`
        parts = content.split('+++', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            
            # Fix keys like `title= "..."` to `title = "..."`
            fm = re.sub(r'^([a-zA-Z_]+)=\s*(.*)$', r'\1 = \2', fm, flags=re.MULTILINE)
            
            # Ensure `[extra]` exists if `categories` or `tags` exist
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
            
            content = f'+++\n{fm.strip()}\n+++\n{body.lstrip()}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    elif content.lstrip().startswith('---'):
        # Similar for ---
        content = content.lstrip()
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            
            # if fm has `=`, it's TOML, so change to `+++`
            if '=' in fm and ':' not in fm:
                fm = re.sub(r'^([a-zA-Z_]+)=\s*(.*)$', r'\1 = \2', fm, flags=re.MULTILINE)
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
                content = f'+++\n{fm.strip()}\n+++\n{body.lstrip()}'
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_file(filepath)
