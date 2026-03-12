import os
import re

dir_path = "/Users/pf/workspace/brainscience/content/studynote/2_operating_system/2_process_thread/"
files = [f for f in os.listdir(dir_path) if f.endswith(".md") and f != "_index.md"]

for f in sorted(files):
    path = os.path.join(dir_path, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        weight_match = re.search(r"weight = (\d+)", content)
        title_match = re.search(r'title = "(\d+)\. (.*?)"', content)
        
        weight = weight_match.group(1) if weight_match else "N/A"
        title_num = title_match.group(1) if title_match else "N/A"
        title_text = title_match.group(2) if title_match else "N/A"
        
        print(f"{f}: weight={weight}, title_num={title_num}, title='{title_text}'")
