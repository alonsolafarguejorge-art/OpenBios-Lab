import os
from core.parser.bios_parser import analyze_bios_file


SUPPORTED_EXTENSIONS = (
    ".bin",
    ".rom",
    ".fd",
    ".cap",
    ".bio"
)


def batch_scan_directory(directory_path):
    if not os.path.exists(directory_path):
        print("Directory not found.")
        return

    total_files = 0
    successful_scans = 0
    failed_scans = 0

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                total_files += 1

                full_path = os.path.join(root, file)

                print(f"\nScanning: {full_path}")

                try:
                    result = analyze_bios_file(full_path)

                    if result["status"] == "success":
                        successful_scans += 1
                        print("Scan successful.")
                    else:
                        failed_scans += 1
                        print("Scan failed.")

                except Exception as e:
                    failed_scans += 1
                    print(f"Error: {e}")

    print("\n--- Batch Scan Summary ---")
    print(f"Total BIOS files found: {total_files}")
    print(f"Successful scans: {successful_scans}")
    print(f"Failed scans: {failed_scans}")


if __name__ == "__main__":
    target_directory = input("Enter directory path for batch scan: ").strip().strip('"')

    batch_scan_directory(target_directory)