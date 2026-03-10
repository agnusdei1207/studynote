
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

def get_section_folder(number):
    for start, end, folder in sections:
        if start <= number <= end:
            return folder
    return None

# Parse keyword list
topic_map_exact = {}
topic_map_fuzzy = {}
with open(keyword_list_path, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
        if match:
            num = int(match.group(1))
            full_name = match.group(2).strip()
            topic_map_exact[full_name.lower()] = (num, full_name)
            
            subnames = re.split(r'[()\-/,]', full_name)
            for sn in subnames:
                clean_sn = sn.strip().lower()
                if clean_sn and len(clean_sn) > 1:
                    # Avoid too generic terms for fuzzy mapping
                    if clean_sn not in ["운영체제", "operating system", "system", "시스템", "management", "관리"]:
                        if clean_sn not in topic_map_fuzzy:
                            topic_map_fuzzy[clean_sn] = (num, full_name)

# Collect all md files
all_files = []
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.md') and not file.startswith('_'):
            all_files.append(os.path.join(root, file))

moved_count = 0
for file_path in all_files:
    filename = os.path.basename(file_path)
    # If it's a 1_alt or topic.md or similarly poorly matched
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'title\s*=\s*"([^"]+)"', content)
    if not title_match: continue
    
    current_title = title_match.group(1)
    # The current title might be like "1. 운영체제 (Operating System)의 목적" because it was already updated
    # We need the ORIGINAL topic name. Often it's in the filename slug if it was moved correctly.
    # But wait, if it's 1_alt, the slug might be 'topic'.
    
    # Let's try to find the original title from the filename or by looking at the content again.
    # If the filename has a slug, use it.
    slug_part = filename.split('_', 1)[1].replace('.md', '') if '_' in filename else ''
    if slug_part == 'topic' or filename.startswith('1_'):
        # Try to match based on the content?
        # Let's look for # Title or other clues.
        pass
    
    # Actually, many files were renamed to "Number. Full Name from List".
    # If it matched #1 incorrectly, we need to re-match.
    
    # Let's just try to match the slug or the current title's non-number part.
    clean_title = re.sub(r'^\d+[\._\s]*', '', current_title).strip()
    
    # If the current title is EXACTLY a list item, but it might be the wrong one.
    # We should have preserved the original title. Oh well.
    # Let's look at the filename. If it was "571_file.md", the slug is "file".
    
    # Let's try to match the slug first.
    best_match = None
    if slug_part and slug_part != 'topic':
        slug_clean = slug_part.replace('_', ' ')
        if slug_clean in topic_map_exact:
            best_match = topic_map_exact[slug_clean]
        elif slug_clean in topic_map_fuzzy:
            best_match = topic_map_fuzzy[slug_clean]
    
    if not best_match:
        # Try matching the clean title
        if clean_title.lower() in topic_map_exact:
            best_match = topic_map_exact[clean_title.lower()]
        elif clean_title.lower() in topic_map_fuzzy:
            best_match = topic_map_fuzzy[clean_title.lower()]

    if best_match:
        num, full_name = best_match
        folder_name = get_section_folder(num)
        if folder_name:
            slug = re.sub(r'[^a-z0-9]+', '_', clean_title.lower()).strip('_')
            if slug == 'topic' and slug_part and slug_part != 'topic':
                slug = slug_part
            
            new_filename = f"{num}_{slug}.md"
            new_path = os.path.join(base_dir, folder_name, new_filename)
            
            # Avoid overwriting or infinite loop
            if os.path.abspath(new_path) == os.path.abspath(file_path):
                continue
                
            if os.path.exists(new_path):
                new_path = new_path.replace('.md', f'_fix_{moved_count}.md')
            
            new_title = f"{num}. {full_name}"
            new_content = re.sub(r'title\s*=\s*"[^"]+"', f'title = "{new_title}"', content)
            new_content = re.sub(r'weight\s*=\s*\d+', f'weight = {num}', new_content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            shutil.move(file_path, new_path)
            moved_count += 1
            print(f"FIXED: {file_path} -> {new_path}")
