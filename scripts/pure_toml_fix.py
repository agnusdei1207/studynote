import os
import re

base_dir = "content/studynote"
fixed_count = 0

for root, _, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith(".md") and not filename.startswith("_"):
            file_path = os.path.join(root, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if not lines or lines[0].strip() != "+++":
                continue
                
            # Find the end of front matter
            end_fm_idx = -1
            for i in range(1, len(lines)):
                if lines[i].strip() == "+++":
                    end_fm_idx = i
                    break
            
            if end_fm_idx == -1:
                continue

            fm_lines = lines[1:end_fm_idx]
            
            weight_val = None
            new_fm_lines = []
            
            # Extract existing weight and filter it out
            for line in fm_lines:
                if line.startswith("weight =") or line.startswith("weight="):
                    weight_val = line.split("=")[1].strip()
                else:
                    new_fm_lines.append(line)
            
            if weight_val:
                # Insert weight at the very beginning of the front matter
                new_fm_lines.insert(0, f"weight = {weight_val}\n")
                
                # Reconstruct file
                new_lines = ["+++\n"] + new_fm_lines + ["+++\n"] + lines[end_fm_idx+1:]
                
                # Check if it was actually modified
                if lines != new_lines:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    fixed_count += 1

print(f"Fixed weight location in {fixed_count} files.")
