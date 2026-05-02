import os


def detect_signatures(binary_data):
    signatures = {
        "UEFI Firmware Volume": b"_FVH",
        "Intel Flash Descriptor": b"$FPT",
        "AMI BIOS": b"AMI",
        "Phoenix BIOS": b"Phoenix",
        "Insyde BIOS": b"Insyde"
    }

    found = []

    for name, signature in signatures.items():
        if signature in binary_data:
            found.append(name)

    return found


def analyze_bios_file(file_path):
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
        }

    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as bios_file:
        binary_data = bios_file.read()

    detected_signatures = detect_signatures(binary_data)

    return {
        "status": "success",
        "file_path": file_path,
        "file_size_bytes": file_size,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
        "detected_signatures": detected_signatures if detected_signatures else ["Unknown"]
    }


if __name__ == "__main__":
    bios_file = input("Enter BIOS file path: ").strip().strip('"')

    result = analyze_bios_file(bios_file)

    print("\n--- BIOS Analysis Result ---")
    for key, value in result.items():
        print(f"{key}: {value}")