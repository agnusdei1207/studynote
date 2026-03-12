import os
import re

def get_numbers(dir_path):
    numbers = {}
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".md") and not file.startswith("_"):
                match = re.match(r"^(\d+)_", file)
                if match:
                    num = int(match.group(1))
                    if num not in numbers:
                        numbers[num] = []
                    numbers[num].append(os.path.join(root, file))
    return numbers

def audit_numbers(dir_path, end_num):
    numbers = get_numbers(dir_path)
    missing = []
    duplicates = []
    for i in range(1, end_num + 1):
        if i not in numbers:
            missing.append(i)
        elif len(numbers[i]) > 1:
            duplicates.append((i, numbers[i]))
    return missing, duplicates

if __name__ == "__main__":
    dir_path = "content/studynote/1_computer_architecture/"
    end_num = 627
    missing, duplicates = audit_numbers(dir_path, end_num)
    
    print(f"--- Missing Numbers (1-{end_num}) ---")
    print(missing)
    print(f"Total Missing: {len(missing)}")
    
    print(f"\n--- Duplicate Numbers ---")
    for num, files in duplicates:
        print(f"[{num}]: {files}")
    print(f"Total Duplicates: {len(duplicates)}")
