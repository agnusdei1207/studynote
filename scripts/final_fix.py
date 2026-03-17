import os
import glob

def fix_delimiters(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        # Check if it ends with +++
        first_line_end = content.find('\n', 3)
        if first_line_end != -1:
            second_delim_idx = content.find('+++', first_line_end)
            if second_delim_idx != -1 and second_delim_idx < content.find('\n#'):
                # Mismatch found: starts with ---, ends with +++
                # Change starting to +++
                content = '+++' + content[3:]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    return

    if content.startswith('+++'):
        # Check if it ends with ---
        first_line_end = content.find('\n', 3)
        if first_line_end != -1:
            second_delim_idx = content.find('---', first_line_end)
            if second_delim_idx != -1 and second_delim_idx < content.find('\n#'):
                # Mismatch found: starts with +++, ends with ---
                # Change ending to +++
                content = content[:second_delim_idx] + '+++' + content[second_delim_idx+3:]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    fix_delimiters(filepath)
