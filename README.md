# 🔐 Local File Integrity Checker

A lightweight Python tool to monitor file integrity by detecting unauthorized or accidental changes to files in a specified directory. It generates and compares SHA-256 hashes, allowing users to detect new, deleted, or modified files between scans.

---

## 🚀 Features

- 🧾 Creates a SHA-256 hash baseline of all files in a directory
- 🔍 Compares current state of files with saved baseline
- 🆕 Detects:
  - New files
  - Deleted files
  - Modified files
- 📦 Stores baseline in a simple JSON file (`baseline_hashes.json`)
- 💡 Useful for basic change detection, monitoring static content, or catching tampering

---

## 📦 Installation

No special dependencies! Just make sure you have **Python 3.8+** installed.

Clone or download the script and run it from your terminal.

---

## 🧠 Usage

Run the script:

```bash
python file_integrity_checker.py
```

You’ll see a menu:

```bash
=== Local File Integrity Checker ===
1. Create baseline
2. Scan for changes
Choose an option (1 or 2):
```

📝 Option 1: Create Baseline
Creates a JSON file storing the current hashes of all files in the given folder.

🔍 Option 2: Scan for Changes
Compares the current file hashes with the stored baseline and prints:

-New files ➕

-Deleted files ❌

-Modified files 🔄

