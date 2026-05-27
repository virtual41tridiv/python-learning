#!/usr/bin/env python3
"""
push_solution.py — Save and push a new Python file to your learning repo.

Usage:
    python push_solution.py
"""

import os
import subprocess
import sys
from datetime import date

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
EDITOR    = os.environ.get("EDITOR", "code")  # change to "nano" or "vim" if needed

TOPIC_FOLDERS = [
    "04_variables_numbers_strings",
    "05_lists_if_for_loop",
    "06_functions_dicts_tuples_file",
    "07_classes_exceptions",
    "08_numpy",
    "09_eda_pandas_matplotlib",
    "10_project1_hospitality_eda",
    "11_comprehensions_sets",
    "12_json_generators_decorators",
    "13_apis",
    "14_logging_pytest_pydantic_db",
    "15_project2_expense_tracker",
]

STATUS_MAP = {
    "04_variables_numbers_strings":    "✅ Done",
    "05_lists_if_for_loop":            "🔄 In Progress",
    "06_functions_dicts_tuples_file":  "⏳ Next",
    "07_classes_exceptions":           "⏳ Next",
    "08_numpy":                        "⏳ Next",
    "09_eda_pandas_matplotlib":        "⏳ Next",
    "10_project1_hospitality_eda":     "⏳ Next",
    "11_comprehensions_sets":          "⏳ Next",
    "12_json_generators_decorators":   "⏳ Next",
    "13_apis":                         "⏳ Next",
    "14_logging_pytest_pydantic_db":   "⏳ Next",
    "15_project2_expense_tracker":     "⏳ Next",
}


def run(cmd):
    result = subprocess.run(cmd, cwd=REPO_PATH)
    if result.returncode != 0:
        print(f"\n❌ Command failed: {' '.join(cmd)}")
        sys.exit(1)


def pick_folder():
    print("\n📁 Which module are you working on?\n")
    for i, folder in enumerate(TOPIC_FOLDERS, 1):
        status = STATUS_MAP.get(folder, "")
        print(f"  {i:>2}. {folder}  {status}")
    choice = input("\nEnter number: ").strip()
    try:
        return TOPIC_FOLDERS[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        sys.exit(1)


def mark_done(folder):
    """Update the status of a folder to ✅ Done in README.md."""
    readme_path = os.path.join(REPO_PATH, "README.md")
    with open(readme_path, "r") as f:
        content = f.read()

    # Find the folder's short name in the README table and mark it done
    folder_num = folder.split("_")[0]  # e.g. "05"
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if f"| {folder_num} |" in line:
            line = line.replace("🔄 In Progress", "✅ Done").replace("⏳ Next", "✅ Done")
        new_lines.append(line)

    with open(readme_path, "w") as f:
        f.write("\n".join(new_lines))


def main():
    print("=" * 55)
    print("  🐍 Python Learning — Push New File to GitHub")
    print("=" * 55)

    folder = pick_folder()
    folder_path = os.path.join(REPO_PATH, folder)
    os.makedirs(folder_path, exist_ok=True)

    filename = input("\nFilename (e.g. for_loop.py): ").strip()
    if not filename.endswith(".py"):
        filename += ".py"
    filepath = os.path.join(folder_path, filename)

    description = input("Short description (commit message): ").strip()
    if not description:
        description = f"Add {filename}"

    mark_done_choice = input("Mark this module as ✅ Done in README? (y/n): ").strip().lower()

    # Create file with starter template
    if not os.path.exists(filepath):
        today = date.today().isoformat()
        with open(filepath, "w") as f:
            f.write(f'"""\n{description}\nModule : {folder}\nDate   : {today}\n"""\n\n\n')
        print(f"\n✅ Created: {filepath}")
    else:
        print(f"\n📝 Opening existing file: {filepath}")

    input(f"\nPress Enter to open in your editor (save & close when done)...")
    subprocess.run([EDITOR, filepath])

    if mark_done_choice == "y":
        mark_done(folder)
        print("📋 README progress updated.")

    print("\n🚀 Pushing to GitHub...")
    run(["git", "add", "."])
    run(["git", "commit", "-m", f"✅ {description}"])
    run(["git", "push"])

    print(f"\n🎉 Done! '{filename}' is live on GitHub.")
    print(f"   Module : {folder}")
    print(f"   Commit : ✅ {description}")


if __name__ == "__main__":
    main()
