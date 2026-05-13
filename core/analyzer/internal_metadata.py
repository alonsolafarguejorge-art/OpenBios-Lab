import os
import re
import json


SEARCH_PATTERNS = [
    rb"AMI",
    rb"Phoenix",
    rb"Insyde",
    rb"Dell",
    rb"HP",
    rb"Lenovo",
    rb"ASUS",
    rb"Acer",
    rb"Samsung",
    rb"Sony",
    rb"Toshiba",
    rb"ThinkPad",
    rb"ProBook",
    rb"EliteBook",
    rb"Latitude",
    rb"Vostro",
    rb"ROG",
    rb"Legion"
]


def extract_metadata(file_path):
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
        }

    findings = {}

    with open(file_path, "rb") as bios_file:
        binary_data = bios_file.read()

    for pattern in SEARCH_PATTERNS:
        matches = list(re.finditer(pattern, binary_data, re.IGNORECASE))

        if matches:
            findings[pattern.decode(errors="ignore")] = [
                hex(match.start()) for match in matches[:10]
            ]

    return {
        "status": "success",
        "file_path": file_path,
        "detected_metadata": findings if findings else {"Unknown": "No metadata patterns detected"}
    }


def save_report(report):
    os.makedirs("reports", exist_ok=True)

    base_name = os.path.splitext(os.path.basename(report["file_path"]))[0]
    output_path = os.path.join(
        "reports",
        f"{base_name}_metadata.json"
    )

    with open(output_path, "w", encoding="utf-8") as report_file:
        json.dump(report, report_file, indent=4)

    return output_path


if __name__ == "__main__":
    bios_file = input("Enter BIOS file path: ").strip().strip('"')

    result = extract_metadata(bios_file)

    if result["status"] == "success":
        report_path = save_report(result)
        result["report_saved_to"] = report_path

    print("\n--- Internal BIOS Metadata Report ---")
    for key, value in result.items():
        print(f"{key}: {value}")