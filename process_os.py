
import os
import re
import shutil

keyword_list_path = 'content/studynote/2_operating_system/_keyword_list.md'
base_dir = 'content/studynote/2_operating_system'

sections = [
    (1, 80, '1_overview_architecture'),
    (81, 160, '2_process_thread'),
    (161, 220, '3_cpu_scheduling'),
    (221, 290, '4_synchronization'),
    (291, 330, '5_deadlock'),
    (331, 400, '6_memory_management'),
    (401, 460, '7_virtual_memory'),
    (461, 520, '8_io_storage_system'),
    (521, 590, '9_file_system'),
    (591, 690, '10_security_performance_virtualization'),
    (691, 820, '11_exam_summary'),
]

# Ensure all target folders exist
for _, _, folder in sections:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

def get_section_folder(number):
    for start, end, folder in sections:
        if start <= number <= end:
            return folder
    return None

# Parse keyword list
topic_map = {} # topic_name (lowercase) -> (number, full_name)
with open(keyword_list_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
    if match:
        num = int(match.group(1))
        full_name = match.group(2).strip()
        
        # Add the full name
        topic_map[full_name.lower()] = (num, full_name)
        
        # Split by various delimiters to get all possible names
        # delimiters: (, ), -, /, ,
        subnames = re.split(r'[()\-/,]', full_name)
        for sn in subnames:
            clean_sn = sn.strip().lower()
            if clean_sn and len(clean_sn) > 1: # Skip single chars
                if clean_sn not in topic_map:
                    topic_map[clean_sn] = (num, full_name)

# Process files
files_to_process = []
for root, dirs, files in os.walk(base_dir):
    if root == base_dir:
        continue
    for file in files:
        if file.endswith('.md') and not file.startswith('_'):
            files_to_process.append(os.path.join(root, file))

unmatched = []
moved_count = 0

for file_path in files_to_process:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    title_match = re.search(r'title\s*=\s*"([^"]+)"', content)
    if not title_match:
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        
    if title_match:
        current_title = title_match.group(1)
        clean_title = re.sub(r'^\d+[\._\s]*', '', current_title).strip()
        clean_title_lower = clean_title.lower()
        
        best_match = None
        # 1. Exact match on clean title
        if clean_title_lower in topic_map:
            best_match = topic_map[clean_title_lower]
        
        # 2. Try simple alphanumeric match
        if not best_match:
            simple_title = re.sub(r'[^a-z0-9]+', '', clean_title_lower)
            if simple_title:
                for t_name, t_info in topic_map.items():
                    if re.sub(r'[^a-z0-9]+', '', t_name) == simple_title:
                        best_match = t_info
                        break
        
        # 3. Try matching English terms if present
        if not best_match:
            # If title is like "Topic (English)", try to match English
            eng_match = re.search(r'\(([^)]+)\)', clean_title)
            if eng_match:
                eng_part = eng_match.group(1).lower()
                if eng_part in topic_map:
                    best_match = topic_map[eng_part]

        # 4. Try matching title parts if multiple words
        if not best_match and ' ' in clean_title_lower:
            parts = clean_title_lower.split()
            for part in parts:
                if len(part) > 3 and part in topic_map:
                    # Be careful with partial word matches, but here we check if the WHOLE part is a topic
                    best_match = topic_map[part]
                    break

        if best_match:
            num, full_name = best_match
            section_folder = get_section_folder(num)
            if section_folder:
                slug = re.sub(r'[^a-z0-9]+', '_', clean_title.lower()).strip('_')
                if not slug: slug = "topic"
                new_filename = f"{num}_{slug}.md"
                new_path = os.path.join(base_dir, section_folder, new_filename)
                
                new_title = f"{num}. {full_name}"
                new_content = re.sub(r'title\s*=\s*"[^"]+"', f'title = "{new_title}"', content)
                if 'weight =' in new_content:
                    new_content = re.sub(r'weight\s*=\s*\d+', f'weight = {num}', new_content)
                else:
                    new_content = re.sub(r'(title\s*=\s*"[^"]+")', f'\\1\nweight = {num}', new_content)
                
                if os.path.exists(new_path) and os.path.abspath(new_path) != os.path.abspath(file_path):
                    new_path = new_path.replace('.md', f'_alt_{moved_count}.md')

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(file_path, new_path)
                moved_count += 1
                print(f"MOVED: {file_path} -> {new_path}")
            else:
                unmatched.append(f"No section for {num}: {full_name} in {file_path}")
        else:
            unmatched.append(f"No match for {current_title} in {file_path}")

print(f"\nTotal moved: {moved_count}")
print(f"Unmatched: {len(unmatched)}")
# for u in unmatched: print(u)

# Cleanup
for root, dirs, files in os.walk(base_dir, topdown=False):
    if root == base_dir: continue
    if not any(root.endswith(s[2]) for s in sections):
        remaining = os.listdir(root)
        if not remaining or (len(remaining) == 1 and remaining[0] == '_index.md'):
            print(f"Removing redundant folder: {root}")
            shutil.rmtree(root)
