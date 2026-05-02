import os


def find_all_offsets(binary_data, signature):
    offsets = []
    start = 0

    while True:
        offset = binary_data.find(signature, start)
        if offset == -1:
            break
        offsets.append(hex(offset))
        start = offset + 1

    return offsets


def detect_firmware_structure(binary_data):
    signatures = {
        "UEFI Firmware Volume": b"_FVH",
        "Intel Flash Descriptor": b"$FPT",
        "AMI BIOS": b"AMI",
        "Phoenix BIOS": b"Phoenix",
        "Insyde BIOS": b"Insyde"
    }

    structure = {}

    for name, sig in signatures.items():
        found_offsets = find_all_offsets(binary_data, sig)
        if found_offsets:
            structure[name] = found_offsets

    return structure


def classify_bios(structure):
    if "Intel Flash Descriptor" in structure:
        return "Intel UEFI/Modern BIOS", "High"
    elif "UEFI Firmware Volume" in structure:
        return "UEFI BIOS", "Medium"
    elif "AMI BIOS" in structure:
        return "AMI BIOS", "Medium"
    elif "Phoenix BIOS" in structure:
        return "Phoenix/Legacy BIOS", "Medium"
    elif "Insyde BIOS" in structure:
        return "Insyde BIOS", "Medium"
    else:
        return "Unknown", "Low"


def basic_health_check(file_size, structure):
    warnings = []

    if file_size < 1024 * 1024:
        warnings.append("Unusually small BIOS file")

    if "UEFI Firmware Volume" not in structure:
        warnings.append("No UEFI volumes detected")

    if not structure:
        warnings.append("No known firmware signatures detected")

    return warnings if warnings else ["No obvious structural issues detected"]


def analyze_bios_file(file_path):
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
        }

    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as bios_file:
        binary_data = bios_file.read()

    structure = detect_firmware_structure(binary_data)

    bios_type, confidence = classify_bios(structure)

    health_warnings = basic_health_check(file_size, structure)

    return {
        "status": "success",
        "file_path": file_path,
        "file_size_bytes": file_size,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
        "bios_type": bios_type,
        "confidence_level": confidence,
        "detected_structure": structure if structure else {"Unknown": "N/A"},
        "health_check": health_warnings
    }


if __name__ == "__main__":
    bios_file = input("Enter BIOS file path: ").strip().strip('"')

    result = analyze_bios_file(bios_file)

    print("\n--- BIOS Structural Intelligence Report ---")
    for key, value in result.items():
        print(f"{key}: {value}")