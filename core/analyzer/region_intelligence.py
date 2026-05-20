import os
import json
import re


REGION_PATTERNS = {
    "Intel Flash Descriptor": rb"\x5A\xA5\xF0\x0F",
    "UEFI Firmware Volume": rb"_FVH",
    "Intel ME Region": rb"\$FPT",
    "BIOS Region": rb"BIOS",
    "GbE Region": rb"GbE",
    "EC Region": rb"KBC",
    "Phoenix BIOS": rb"Phoenix",
    "Insyde BIOS": rb"Insyde",
    "AMI BIOS": rb"AMI"
}


def analyze_regions(file_path):
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
        }

    with open(file_path, "rb") as bios_file:
        binary_data = bios_file.read()

    detected_regions = {}

    for region_name, pattern in REGION_PATTERNS.items():

        matches = list(re.finditer(pattern, binary_data, re.IGNORECASE))

        if matches:
            detected_regions[region_name] = [
                hex(match.start()) for match in matches[:20]
            ]

    # Architecture guess
    if "Intel ME Region" in detected_regions:
        platform_type = "Intel Platform"

    elif "AMD" in str(binary_data[:500000]):
        platform_type = "AMD Platform"

    else:
        platform_type = "Unknown Platform"

    # BIOS type
    if "UEFI Firmware Volume" in detected_regions:
        bios_mode = "UEFI"

    elif "Phoenix BIOS" in detected_regions:
        bios_mode = "Legacy/Phoenix"

    else:
        bios_mode = "Unknown"

    return {
        "status": "success",
        "file_path": file_path,
        "platform_type": platform_type,
        "bios_mode": bios_mode,
        "detected_regions": detected_regions if detected_regions else {
            "Unknown": "No known firmware regions detected"
        }
    }


def save_report(report):
    os.makedirs("reports", exist_ok=True)

    base_name = os.path.splitext(os.path.basename(report["file_path"]))[0]

    output_path = os.path.join(
        "reports",
        f"{base_name}_regions.json"
    )

    with open(output_path, "w", encoding="utf-8") as report_file:
        json.dump(report, report_file, indent=4)

    return output_path


if __name__ == "__main__":
    bios_file = input("Enter BIOS file path: ").strip().strip('"')

    result = analyze_regions(bios_file)

    if result["status"] == "success":
        report_path = save_report(result)
        result["report_saved_to"] = report_path

    print("\n--- Firmware Region Intelligence Report ---")

    for key, value in result.items():
        print(f"{key}: {value}")