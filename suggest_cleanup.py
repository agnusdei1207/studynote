import os
import re

# Load keyword list
def load_keywords(filepath):
    keywords = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Simple regex to find "Num. Name" patterns
        matches = re.findall(r"(\d+)\.\s+(.+)", content)
        for num, name in matches:
            # Clean up name (remove English in parens for easier matching if needed)
            clean_name = name.split('(')[0].strip().lower()
            keywords[int(num)] = clean_name
    return keywords

def audit_and_suggest(dir_path, keywords):
    all_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".md") and not file.startswith("_"):
                all_files.append((file, os.path.join(root, file)))
    
    suggestions = []
    for file, full_path in all_files:
        match = re.match(r"^(\d+)_", file)
        if match:
            num = int(match.group(1))
            name_in_file = file.replace(f"{num}_", "").replace(".md", "").replace("_", " ").lower()
            
            if num in keywords:
                expected_name = keywords[num]
                # If name doesn't match keyword, it's likely misnumbered
                if name_in_file not in expected_name and expected_name not in name_in_file:
                    # Search if this name matches another keyword
                    found_correct_num = None
                    for k_num, k_name in keywords.items():
                        if name_in_file in k_name or k_name in name_in_file:
                            found_correct_num = k_num
                            break
                    if found_correct_num:
                        suggestions.append(f"MOVE: {full_path} -> should be {found_correct_num}")
                    else:
                        suggestions.append(f"UNKNOWN: {full_path} (Num {num} is {expected_name})")
            else:
                suggestions.append(f"OUT_OF_RANGE: {full_path} (Num {num} not in keyword list)")
    
    return suggestions

if __name__ == "__main__":
    kw = load_keywords("content/studynote/1_computer_architecture/_keyword_list.md")
    sug = audit_and_suggest("content/studynote/1_computer_architecture/", kw)
    for s in sorted(sug):
        print(s)
