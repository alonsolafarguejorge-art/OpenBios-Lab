import os
import json
import hashlib
from collections import defaultdict

SUPPORTED_EXTENSIONS = (
    ".bin",
    ".rom",
    ".fd",
    ".cap",
    ".bio"
)


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def analyze_dataset(directory_path):
    if not os.path.exists(directory_path):
        print("Directory not found.")
        return

    total_files = 0
    unique_files = 0
    duplicate_files = 0

    hash_database = defaultdict(list)

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                total_files += 1

                full_path = os.path.join(root, file)

                try:
                    file_hash = calculate_sha256(full_path)
                    hash_database[file_hash].append(full_path)

                except Exception as e:
                    print(f"Error processing {full_path}: {e}")

    duplicates_report = {}

    for file_hash, file_list in hash_database.items():
        if len(file_list) > 1:
            duplicate_files += len(file_list) - 1
            duplicates_report[file_hash] = file_list
        else:
            unique_files += 1

    report = {
        "total_files": total_files,
        "unique_files": unique_files,
        "duplicate_files": duplicate_files,
        "duplicate_groups": len(duplicates_report),
        "duplicates": duplicates_report
    }

    os.makedirs("reports", exist_ok=True)

    output_path = os.path.join("reports", "dataset_inventory.json")

    with open(output_path, "w", encoding="utf-8") as report_file:
        json.dump(report, report_file, indent=4)

    print("\n--- Dataset Intelligence Summary ---")
    print(f"Total files: {total_files}")
    print(f"Unique files: {unique_files}")
    print(f"Duplicate files: {duplicate_files}")
    print(f"Duplicate groups: {len(duplicates_report)}")
    print(f"Inventory saved to: {output_path}")


if __name__ == "__main__":
    target_directory = input("Enter dataset directory path: ").strip().strip('"')

    analyze_dataset(target_directory)