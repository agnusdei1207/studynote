
import os
import re
import shutil

keyword_list_path = 'content/studynote/2_operating_system/_keyword_list.md'
base_dir = 'content/studynote/2_operating_system'
temp_dir = 'content/studynote/2_operating_system_temp'

sections = [
    (1, 80, '1_overview_architecture', '1. 운영체제 개요 및 아키텍처'),
    (81, 160, '2_process_thread', '2. 프로세스와 스레드'),
    (161, 220, '3_cpu_scheduling', '3. CPU 스케줄링'),
    (221, 290, '4_synchronization', '4. 병행성 및 동기화'),
    (291, 330, '5_deadlock', '5. 교착 상태'),
    (331, 400, '6_memory_management', '6. 메인 메모리 관리'),
    (401, 460, '7_virtual_memory', '7. 가상 메모리 관리'),
    (461, 520, '8_io_storage_system', '8. 저장장치 및 입출력 시스템'),
    (521, 590, '9_file_system', '9. 파일 시스템 관리'),
    (591, 690, '10_security_performance_virtualization', '10. 시스템 보안, 보호, 그리고 성능/가상화 심화'),
    (691, 820, '11_exam_summary', '11. 시험 빈출 / 핵심 요약 노트 및 추가 토픽'),
]

# Ensure temp dir exists
os.makedirs(temp_dir, exist_ok=True)

# Parse keyword list
topic_map = {} 
topic_list = [] # Store list to maintain order and full info
with open(keyword_list_path, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
        if match:
            num = int(match.group(1))
            full_name = match.group(2).strip()
            topic_list.append((num, full_name))
            
            # Map various parts
            topic_map[full_name.lower()] = (num, full_name)
            subnames = re.split(r'[()\-/,]', full_name)
            for sn in subnames:
                clean_sn = sn.strip().lower()
                if clean_sn and len(clean_sn) > 1:
                    if clean_sn not in topic_map: topic_map[clean_sn] = (num, full_name)

# Hardcoded fallback mappings for common terms
fallbacks = {
    'lvm': (514, '파티션 (Partition) / 슬라이스 / 볼륨 (Volume)'),
    'logical volume': (514, '파티션 (Partition) / 슬라이스 / 볼륨 (Volume)'),
    'scsi': (446, '포트 (Port) / 버스 (Bus) - PCIe, USB, SATA, NVMe'),
    'sata': (446, '포트 (Port) / 버스 (Bus) - PCIe, USB, SATA, NVMe'),
    'bios': (30, 'UEFI (Unified Extensible Firmware Interface) vs BIOS'),
    'fstab': (516, '마운트 (Mount) 메커니즘'),
    'swap': (390, '스왑 공간 (Swap Space) / 베이킹 스토어 (Backing Store)'),
    'path': (509, '절대 경로 (Absolute Path) / 상대 경로 (Relative Path)'),
    'link': (511, '하드 링크 (Hard Link)'),
    'permission': (547, '파일 시스템 접근 제어 (Access Control)'),
    'f2fs': (563, '플래시 전용 파일 시스템 (F2FS, JFFS2, YAFFS)'),
}

# 1. Collect and move all files to temp_dir
all_files = []
for root, dirs, files in os.walk(base_dir):
    if root == base_dir: continue
    for file in files:
        if file.endswith('.md'):
            old_path = os.path.join(root, file)
            temp_path = os.path.join(temp_dir, file)
            if os.path.exists(temp_path): # Handle duplicates in naming
                temp_path = temp_path.replace('.md', f'_{len(all_files)}.md')
            shutil.move(old_path, temp_path)
            all_files.append(temp_path)

# 2. Cleanup old folders
for root, dirs, files in os.walk(base_dir, topdown=False):
    if root == base_dir: continue
    shutil.rmtree(root)

# 3. Re-create folders and _index.md
for start, end, folder_name, section_title in sections:
    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, '_index.md'), 'w', encoding='utf-8') as f:
        f.write(f'+++\ntitle = "{section_title}"\nweight = {start}\n+++\n')

# 4. Process all files from temp_dir
moved_count = 0
unmatched_count = 0

for file_path in all_files:
    if os.path.basename(file_path).startswith('_'):
        os.remove(file_path) # Skip old _index.md
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'title\s*=\s*"([^"]+)"', content)
    current_title = title_match.group(1) if title_match else os.path.basename(file_path)
    clean_title = re.sub(r'^\d+[\._\s]*', '', current_title).strip()
    clean_title_lower = clean_title.lower()
    
    best_match = None
    if clean_title_lower in topic_map:
        best_match = topic_map[clean_title_lower]
    elif clean_title_lower in fallbacks:
        best_match = fallbacks[clean_title_lower]
    else:
        # Fuzzy/Partial
        simple_title = re.sub(r'[^a-z0-9]+', '', clean_title_lower)
        for t_name, t_info in topic_map.items():
            if re.sub(r'[^a-z0-9]+', '', t_name) == simple_title:
                best_match = t_info; break
        if not best_match:
            for t_name, t_info in topic_map.items():
                if t_name in clean_title_lower or clean_title_lower in t_name:
                    if len(clean_title_lower) > 3:
                        best_match = t_info; break

    if best_match:
        num, full_name = best_match
        folder_name = None
        for start, end, fn, st in sections:
            if start <= num <= end:
                folder_name = fn; break
        
        if folder_name:
            # Generate slug from English if possible
            eng_match = re.search(r'([a-z0-9 \-_]+)', full_name, re.I)
            slug = re.sub(r'[^a-z0-9]+', '_', clean_title.lower()).strip('_')
            new_filename = f"{num}_{slug}.md"
            new_path = os.path.join(base_dir, folder_name, new_filename)
            
            if os.path.exists(new_path):
                new_path = new_path.replace('.md', f'_alt_{moved_count}.md')
                
            new_title = f"{num}. {full_name}"
            new_content = re.sub(r'title\s*=\s*"[^"]+"', f'title = "{new_title}"', content)
            if 'weight =' in new_content:
                new_content = re.sub(r'weight\s*=\s*\d+', f'weight = {num}', new_content)
            else:
                new_content = re.sub(r'(title\s*=\s*"[^"]+")', f'\\1\nweight = {num}', new_content)
            
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            moved_count += 1
        else:
            unmatched_count += 1
    else:
        unmatched_count += 1

shutil.rmtree(temp_dir)
print(f"Final: Moved {moved_count}, Unmatched {unmatched_count}")
