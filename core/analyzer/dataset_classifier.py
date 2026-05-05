import os
import json
from collections import defaultdict


VENDOR_KEYWORDS = {
    "HP": [
        "hp", "probook", "elitebook", "pavilion", "envy", "zbook"
    ],
    "Dell": [
        "dell", "latitude", "inspiron", "precision", "vostro", "xps"
    ],
    "Lenovo": [
        "lenovo", "thinkpad", "ideapad", "legion", "yoga"
    ],
    "ASUS": [
        "asus", "rog", "vivobook", "zenbook", "tuf"
    ],
    "Acer": [
        "acer", "aspire", "nitro", "predator", "travelmate"
    ],
    "MSI": [
        "msi", "katana", "stealth", "raider"
    ],
    "Gigabyte": [
        "gigabyte", "aorus"
    ],
    "Toshiba": [
        "toshiba", "satellite", "dynabook"
    ],
    "Samsung": [
        "samsung", "np", "galaxy book"
    ],
    "Sony": [
        "sony", "vaio"
    ],
    "Fujitsu": [
        "fujitsu", "lifebook"
    ],
    "Clevo": [
        "clevo"
    ],
    "Compal": [
        "compal"
    ],
    "Quanta": [
        "quanta"
    ]
}


def detect_vendor(file_path):
    lower_path = file_path.lower()

    for vendor, keywords in VENDOR_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lower_path:
                return vendor

    return "Unknown"


def classify_dataset(unique_library_file):
    if not os.path.exists(unique_library_file):
        print("Unique library file not found.")
        return

    with open(unique_library_file, "r", encoding="utf-8") as file:
        library = json.load(file)

    files = library.get("known_representative_files", [])

    vendor_groups = defaultdict(list)

    for file_path in files:
        vendor = detect_vendor(file_path)
        vendor_groups[vendor].append(file_path)

    classification_report = {
        "total_classified_files": len(files),
        "vendors": {
            vendor: {
                "count": len(paths),
                "files": paths
            }
            for vendor, paths in vendor_groups.items()
        }
    }

    os.makedirs("reports", exist_ok=True)

    output_path = os.path.join("reports", "dataset_classification.json")

    with open(output_path, "w", encoding="utf-8") as report_file:
        json.dump(classification_report, report_file, indent=4)

    print("\n--- Dataset Classification Summary ---")
    print(f"Total classified files: {len(files)}")

    for vendor, paths in vendor_groups.items():
        print(f"{vendor}: {len(paths)}")

    print(f"Classification report saved to: {output_path}")


if __name__ == "__main__":
    library_path = input("Enter complete_unique_library.json path: ").strip().strip('"')

    classify_dataset(library_path)