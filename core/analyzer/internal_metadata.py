import os
import re
import json
from collections import defaultdict


VENDOR_PATTERNS = {
    "HP": [
        rb"ProBook",
        rb"EliteBook",
        rb"Pavilion",
        rb"ZBook",
        rb"OMEN"
    ],
    "Dell": [
        rb"Dell",
        rb"Alienware",
        rb"Latitude",
        rb"Vostro",
        rb"Inspiron",
        rb"Precision"
    ],
    "Lenovo": [
        rb"Lenovo",
        rb"ThinkPad",
        rb"IdeaPad",
        rb"Legion",
        rb"Yoga"
    ],
    "ASUS": [
        rb"ASUS",
        rb"ROG",
        rb"ZenBook",
        rb"VivoBook",
        rb"TUF"
    ],
    "Acer": [
        rb"Acer",
        rb"Aspire",
        rb"Nitro",
        rb"Predator",
        rb"TravelMate"
    ],
    "Samsung": [
        rb"Samsung",
        rb"Galaxy Book"
    ],
    "Sony": [
        rb"VAIO"
    ],
    "Toshiba": [
        rb"Toshiba",
        rb"Dynabook",
        rb"Satellite"
    ],
    "MSI": [
        rb"MSI",
        rb"Katana",
        rb"Raider",
        rb"Stealth"
    ],
    "Gigabyte": [
        rb"Gigabyte",
        rb"AORUS"
    ]
}


GENERAL_PATTERNS = [
    rb"AMI",
    rb"Phoenix",
    rb"Insyde"
]


def extract_metadata(file_path):
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
        }

    with open(file_path, "rb") as bios_file:
        binary_data = bios_file.read()

    vendor_scores = defaultdict(int)
    general_findings = {}

    # Vendor scoring
    for vendor, patterns in VENDOR_PATTERNS.items():
        for pattern in patterns:
            matches = list(re.finditer(pattern, binary_data, re.IGNORECASE))
            vendor_scores[vendor] += len(matches)

    # Filename heuristic boost
    lower_filename = file_path.lower()
    for vendor, patterns in VENDOR_PATTERNS.items():
        for pattern in patterns:
            keyword = pattern.decode(errors="ignore").lower()
            if keyword in lower_filename:
                vendor_scores[vendor] += 5

    # General BIOS metadata
    for pattern in GENERAL_PATTERNS:
        matches = list(re.finditer(pattern, binary_data, re.IGNORECASE))

        if matches:
            general_findings[pattern.decode(errors="ignore")] = [
                hex(match.start()) for match in matches[:10]
            ]

    # Determine best vendor
    if vendor_scores:
        best_vendor = max(vendor_scores, key=vendor_scores.get)
        confidence_score = vendor_scores[best_vendor]

        if confidence_score >= 15:
            confidence_level = "High"
        elif confidence_score >= 5:
            confidence_level = "Medium"
        else:
            confidence_level = "Low"
    else:
        best_vendor = "Unknown"
        confidence_score = 0
        confidence_level = "Unknown"

    return {
        "status": "success",
        "file_path": file_path,
        "detected_vendor": best_vendor,
        "confidence_score": confidence_score,
        "confidence_level": confidence_level,
        "vendor_score_breakdown": dict(vendor_scores),
        "general_metadata": general_findings if general_findings else {"Unknown": "No BIOS family markers detected"}
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