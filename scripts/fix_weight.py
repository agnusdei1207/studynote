import os
import re

base_dir = "content/studynote"
fixed_count = 0

for root, _, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith(".md") and not filename.startswith("_"):
            match = re.match(r"^(\d+)_", filename)
            if not match:
                continue
            
            weight_val = int(match.group(1))
            file_path = os.path.join(root, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if not lines or lines[0].strip() != "+++":
                continue # Skip if no proper front matter
                
            # Check if weight exists
            has_weight = False
            end_fm_idx = -1
            
            for i in range(1, len(lines)):
                if lines[i].startswith("weight =") or lines[i].startswith("weight="):
                    has_weight = True
                if lines[i].strip() == "+++":
                    end_fm_idx = i
                    break
                    
            if not has_weight and end_fm_idx != -1:
                # Insert weight right before the end of front matter
                # But carefully, place it after title or date
                lines.insert(end_fm_idx, f"weight = {weight_val}\n")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                fixed_count += 1

print(f"Added weight to {fixed_count} files.")
