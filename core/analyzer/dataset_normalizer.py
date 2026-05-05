import os
import json


def normalize_dataset(inventory_file):
    if not os.path.exists(inventory_file):
        print("Inventory file not found.")
        return

    with open(inventory_file, "r", encoding="utf-8") as file:
        inventory = json.load(file)

    duplicates = inventory.get("duplicates", {})
    total_files = inventory.get("total_files", 0)

    os.makedirs("reports", exist_ok=True)

    complete_unique_report_path = os.path.join("reports", "complete_unique_library.json")
    duplicates_report_path = os.path.join("reports", "duplicate_files.json")

    complete_unique_files = []
    duplicate_files = []

    all_duplicate_paths = set()

    for file_hash, file_list in duplicates.items():
        if len(file_list) > 0:
            # One representative kept
            complete_unique_files.append(file_list[0])

            # Remaining are duplicates
            if len(file_list) > 1:
                duplicate_files.extend(file_list[1:])

            # Track all duplicate group members
            all_duplicate_paths.update(file_list)

    # Include files that were not part of duplicate groups
    # These were unique in original dataset
    inventory_duplicates = inventory.get("duplicates", {})

    duplicate_group_files = set()
    for group in inventory_duplicates.values():
        duplicate_group_files.update(group)

    # Since dataset_inventory only tracks duplicates,
    # unique standalone files are already accounted via counts,
    # but not paths. For now, complete library = duplicate reps + standalone estimate.

    report_complete_unique = {
        "estimated_total_unique_library_size": inventory.get("unique_files", 0),
        "duplicate_group_representatives": len(complete_unique_files),
        "known_representative_files": complete_unique_files
    }

    report_duplicates = {
        "duplicate_file_count": len(duplicate_files),
        "duplicate_files": duplicate_files
    }

    with open(complete_unique_report_path, "w", encoding="utf-8") as unique_file:
        json.dump(report_complete_unique, unique_file, indent=4)

    with open(duplicates_report_path, "w", encoding="utf-8") as duplicate_file:
        json.dump(report_duplicates, duplicate_file, indent=4)

    print("\n--- Dataset Normalization Summary v2 ---")
    print(f"Estimated complete unique BIOS library size: {inventory.get('unique_files', 0)}")
    print(f"Duplicate group representatives identified: {len(complete_unique_files)}")
    print(f"Duplicate redundant files identified: {len(duplicate_files)}")
    print(f"Complete library report saved to: {complete_unique_report_path}")
    print(f"Duplicate report saved to: {duplicates_report_path}")


if __name__ == "__main__":
    inventory_path = input("Enter dataset_inventory.json path: ").strip().strip('"')

    normalize_dataset(inventory_path)