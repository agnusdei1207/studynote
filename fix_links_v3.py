import os
import re

content_root = 'content/studynotes/'
abs_content_root = os.path.abspath(content_root)

# Get all md files
all_files = []
for root, dirs, files in os.walk(content_root):
    for file in files:
        if file.endswith('.md'):
            all_files.append(os.path.join(root, file))

# Create a map of filename to path for searching
file_map = {}
for f in all_files:
    basename = os.path.basename(f)
    if basename not in file_map:
        file_map[basename] = []
    file_map[basename].append(f)

def resolve_link(current_file, link_path):
    # Handle both relative and already absolute @/ links
    original_path = link_path
    if link_path.startswith('@/'):
        # Only re-evaluate if it's in studynotes
        if not link_path.startswith('@/studynotes/'):
            return None
        # Convert to local path for evaluation
        eval_path = link_path.replace('@/', 'content/')
    elif link_path.startswith(('http', 'mailto', '/', '#')):
        return None
    else:
        eval_path = None # Will be calculated below

    # Remove query or fragment
    path_only = link_path.split('?')[0].split('#')[0]
    if not path_only:
        return None
        
    if eval_path is None:
        current_dir = os.path.dirname(current_file)
        target_path = os.path.normpath(os.path.join(current_dir, path_only))
    else:
        target_path = eval_path

    # 1. Check if it exists as is
    if os.path.exists(target_path):
        # If it's an @/ link and it exists, we might still want to check if there's a better match
        # especially if it's pointing to a top-level _index.md
        if not (link_path.startswith('@/') and target_path.endswith('_index.md')):
             return target_path
    
    # 2. Try to match the path components from the end
    # Use the path from the link, not the normalized target_path
    # For @/ links, remove the prefix
    if link_path.startswith('@/'):
        clean_path = link_path.replace('@/studynotes/', '')
    else:
        clean_path = path_only

    path_parts = clean_path.replace('\\', '/').split('/')
    filtered_parts = [p for p in path_parts if p and p not in ('.', '..')]
    
    if filtered_parts:
        for i in range(len(filtered_parts)):
            suffix = '/'.join(filtered_parts[i:])
            for f in all_files:
                if f.endswith(suffix):
                    return f
    
    # 3. Check if it's just the basename that exists elsewhere
    basename = os.path.basename(path_only)
    if basename in file_map:
        return file_map[basename][0]
    
    # 4. Point to closest _index.md
    search_dir = os.path.dirname(target_path)
    while search_dir.startswith(content_root):
        index_path = os.path.join(search_dir, '_index.md')
        if os.path.exists(index_path):
            return index_path
        search_dir = os.path.dirname(search_dir)
        
    return os.path.join(content_root, '_index.md')

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def replace_link(match):
        text = match.group(1)
        link = match.group(2)
        
        resolved = resolve_link(file_path, link)
        if resolved:
            rel_to_content = os.path.relpath(resolved, 'content')
            new_link = f"@/{rel_to_content}"
            return f"[{text}]({new_link})"
        return match.group(0)

    new_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

updated_count = 0
for f in all_files:
    if update_file(f):
        updated_count += 1
        print(f"Updated: {f}")

print(f"Total files updated: {updated_count}")
