import os
import hashlib
import json
from datetime import datetime

BASELINE_FILE = "baseline_hashes.json"

# generate SHA-256 hash of a file
def hash_file(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return None  # could not read file

# recursively walk directory and return
def generate_file_hashes(root_dir):
    file_hashes = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            hash_val = hash_file(full_path)
            if hash_val:
                relative_path = os.path.relpath(full_path, root_dir)
                file_hashes[relative_path] = hash_val
    return file_hashes

# save baseline hash map to JSON
def save_baseline(file_hashes):
    with open(BASELINE_FILE, "w") as f:
        json.dump(file_hashes, f, indent=4)
    print(f"[✓] Baseline saved to {BASELINE_FILE}")

# load baseline hashes
def load_baseline():
    try:
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[!] Baseline file not found.")
        return None

# compare current hashes with baseline
def compare_hashes(baseline, current):
    new_files = []
    deleted_files = []
    modified_files = []

    for path in baseline:
        if path not in current:
            deleted_files.append(path)
        elif baseline[path] != current[path]:
            modified_files.append(path)

    for path in current:
        if path not in baseline:
            new_files.append(path)

    return new_files, deleted_files, modified_files

# print log report
def print_report(new, deleted, modified):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[🕒] Integrity Scan Report — {timestamp}")
    print("==========================================")

    if new:
        print(f"\n[+] New Files ({len(new)}):")
        for f in new:
            print(f"  ➕ {f}")
    if deleted:
        print(f"\n[-] Deleted Files ({len(deleted)}):")
        for f in deleted:
            print(f"  ❌ {f}")
    if modified:
        print(f"\n[~] Modified Files ({len(modified)}):")
        for f in modified:
            print(f"  🔄 {f}")

    if not any([new, deleted, modified]):
        print("\n[✓] No changes detected.")

# main menu
def main():
    print("=== Local File Integrity Checker ===")
    print("1. Create baseline")
    print("2. Scan for changes")
    choice = input("Choose an option (1 or 2): ").strip()

    folder = input("Enter the folder path to scan: ").strip()
    if not os.path.isdir(folder):
        print("[!] Invalid folder path.")
        return

    if choice == "1":
        hashes = generate_file_hashes(folder)
        save_baseline(hashes)
    elif choice == "2":
        baseline = load_baseline()
        if baseline is None:
            return
        current = generate_file_hashes(folder)
        new, deleted, modified = compare_hashes(baseline, current)
        print_report(new, deleted, modified)
    else:
        print("[!] Invalid option.")

if __name__ == "__main__":
    main()
