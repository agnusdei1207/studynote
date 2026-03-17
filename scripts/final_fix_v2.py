import os
import glob

def fix_yaml_to_toml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            if '=' in fm and ':' not in fm:
                # TOML content but YAML delimiter
                new_content = '+++' + fm + '+++' + parts[2]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            elif '[extra]' in fm:
                # TOML extra but YAML delimiter
                new_content = '+++' + fm + '+++' + parts[2]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_yaml_to_toml(filepath)
