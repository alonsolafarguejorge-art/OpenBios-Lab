import os

def analyze_bios_file(file_path):
    """
    Basic BIOS file analysis:
    - Checks existence
    - Gets file size
    """

    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
        }

    file_size = os.path.getsize(file_path)

    return {
        "status": "success",
        "file_path": file_path,
        "file_size_bytes": file_size,
        "file_size_mb": round(file_size / (1024 * 1024), 2)
    }


if __name__ == "__main__":
    bios_file = input("Enter BIOS file path: ").strip().strip('"')

    result = analyze_bios_file(bios_file)

    print("\n--- BIOS Analysis Result ---")
    for key, value in result.items():
        print(f"{key}: {value}")