
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
topic_map = {}
with open(keyword_list_path, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
        if match:
            num = int(match.group(1))
            full_name = match.group(2).strip()
            topic_map[full_name.lower()] = (num, full_name)
            subnames = re.split(r'[()\-/,]', full_name)
            for sn in subnames:
                clean_sn = sn.strip().lower()
                if clean_sn and len(clean_sn) > 1:
                    if clean_sn not in topic_map: topic_map[clean_sn] = (num, full_name)

# Hardcoded fallbacks
fallbacks = {
    '장치 파일': (441, 'I/O 장치의 분류'),
    '블록 장치': (442, '블록 장치'),
    '문자 장치': (443, '문자 장치'),
    'lvm': (514, '파티션 (Partition) / 슬라이스 / 볼륨 (Volume)'),
    'swap': (390, '스왑 공간 (Swap Space)'),
    'bios': (30, 'UEFI vs BIOS'),
}

# Collect files
all_files = []
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.md') and not file.startswith('_'):
            all_files.append(os.path.join(root, file))

moved_count = 0
for file_path in all_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the first H1 header
    real_topic = None
    for line in lines:
        if line.startswith('# '):
            real_topic = line[2:].strip()
            break
    
    if not real_topic:
        # Fallback to current title in front matter if no H1
        content = "".join(lines)
        title_match = re.search(r'title\s*=\s*"([^"]+)"', content)
        if title_match:
            real_topic = title_match.group(1)
    
    if real_topic:
        # Clean the topic (remove numbers)
        clean_topic = re.sub(r'^\d+[\._\s]*', '', real_topic).strip()
        clean_topic_lower = clean_topic.lower()
        
        best_match = None
        if clean_topic_lower in topic_map:
            best_match = topic_map[clean_topic_lower]
        elif clean_topic_lower in fallbacks:
            best_match = fallbacks[clean_topic_lower]
        else:
            # Check if any subname in topic_map matches
            for t_name, t_info in topic_map.items():
                if t_name in clean_topic_lower or clean_topic_lower in t_name:
                    if len(clean_topic_lower) > 3:
                        best_match = t_info; break
        
        if best_match:
            num, full_name = best_match
            folder_name = get_section_folder(num)
            if folder_name:
                slug = re.sub(r'[^a-z0-9]+', '_', clean_topic.lower()).strip('_')
                if not slug: slug = "topic"
                new_filename = f"{num}_{slug}.md"
                new_path = os.path.join(base_dir, folder_name, new_filename)
                
                if os.path.abspath(new_path) == os.path.abspath(file_path):
                    continue
                if os.path.exists(new_path):
                    new_path = new_path.replace('.md', f'_v_{moved_count}.md')
                
                # Update content
                content = "".join(lines)
                new_title = f"{num}. {full_name}"
                content = re.sub(r'title\s*=\s*"[^"]+"', f'title = "{new_title}"', content)
                content = re.sub(r'weight\s*=\s*\d+', f'weight = {num}', content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(file_path, new_path)
                moved_count += 1
                print(f"RE-FIXED: {file_path} -> {new_path}")

print(f"Total re-fixed: {moved_count}")
