import os


def find_signature_offsets(binary_data, signatures):
    results = {}

    for name, signature in signatures.items():
        offset = binary_data.find(signature)
        if offset != -1:
            results[name] = hex(offset)

    return results


def classify_bios(offsets):
    if "Intel Flash Descriptor" in offsets:
        return "Intel UEFI/Modern BIOS"
    elif "UEFI Firmware Volume" in offsets:
        return "UEFI BIOS"
    elif "AMI BIOS" in offsets:
        return "AMI BIOS"
    elif "Phoenix BIOS" in offsets:
        return "Phoenix/Legacy BIOS"
    elif "Insyde BIOS" in offsets:
        return "Insyde BIOS"
    else:
        return "Unknown"


def analyze_bios_file(file_path):
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
        }

    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as bios_file:
        binary_data = bios_file.read()

    signatures = {
        "UEFI Firmware Volume": b"_FVH",
        "Intel Flash Descriptor": b"$FPT",
        "AMI BIOS": b"AMI",
        "Phoenix BIOS": b"Phoenix",
        "Insyde BIOS": b"Insyde"
    }

    detected_offsets = find_signature_offsets(binary_data, signatures)

    bios_type = classify_bios(detected_offsets)

    return {
        "status": "success",
        "file_path": file_path,
        "file_size_bytes": file_size,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
        "bios_type": bios_type,
        "detected_regions": detected_offsets if detected_offsets else {"Unknown": "N/A"}
    }


if __name__ == "__main__":
    bios_file = input("Enter BIOS file path: ").strip().strip('"')

    result = analyze_bios_file(bios_file)

    print("\n--- BIOS Structural Analysis Result ---")
    for key, value in result.items():
        print(f"{key}: {value}")