import os
import json


def normalize_dataset(inventory_file):
    if not os.path.exists(inventory_file):
        print("Inventory file not found.")
        return

    with open(inventory_file, "r", encoding="utf-8") as file:
        inventory = json.load(file)

    duplicates = inventory.get("duplicates", {})

    os.makedirs("reports", exist_ok=True)

    unique_report_path = os.path.join("reports", "unique_files.json")
    duplicates_report_path = os.path.join("reports", "duplicate_files.json")

    unique_files = []
    duplicate_files = []

    for file_hash, file_list in duplicates.items():
        if len(file_list) > 0:
            unique_files.append(file_list[0])

            if len(file_list) > 1:
                duplicate_files.extend(file_list[1:])

    report_unique = {
        "unique_file_count": len(unique_files),
        "unique_files": unique_files
    }

    report_duplicates = {
        "duplicate_file_count": len(duplicate_files),
        "duplicate_files": duplicate_files
    }

    with open(unique_report_path, "w", encoding="utf-8") as unique_file:
        json.dump(report_unique, unique_file, indent=4)

    with open(duplicates_report_path, "w", encoding="utf-8") as duplicate_file:
        json.dump(report_duplicates, duplicate_file, indent=4)

    print("\n--- Dataset Normalization Summary ---")
    print(f"Unique files identified: {len(unique_files)}")
    print(f"Duplicate redundant files identified: {len(duplicate_files)}")
    print(f"Unique report saved to: {unique_report_path}")
    print(f"Duplicate report saved to: {duplicates_report_path}")


if __name__ == "__main__":
    inventory_path = input("Enter dataset_inventory.json path: ").strip().strip('"')

    normalize_dataset(inventory_path)