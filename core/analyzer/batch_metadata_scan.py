import os
import json
from collections import defaultdict

from core.analyzer.internal_metadata import extract_metadata


SUPPORTED_EXTENSIONS = (
    ".bin",
    ".rom",
    ".fd",
    ".cap",
    ".bio"
)


def batch_metadata_scan(directory_path):
    if not os.path.exists(directory_path):
        print("Directory not found.")
        return

    vendor_statistics = defaultdict(int)

    total_files = 0
    successful_scans = 0
    failed_scans = 0

    metadata_reports = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):

                total_files += 1

                full_path = os.path.join(root, file)

                print(f"\nAnalyzing metadata: {full_path}")

                try:
                    result = extract_metadata(full_path)

                    if result["status"] == "success":

                        successful_scans += 1

                        detected_vendor = result.get(
                            "detected_vendor",
                            "Unknown"
                        )

                        vendor_statistics[detected_vendor] += 1

                        metadata_reports.append({
                            "file_path": full_path,
                            "vendor": detected_vendor,
                            "confidence": result.get(
                                "confidence_level",
                                "Unknown"
                            ),
                            "score": result.get(
                                "confidence_score",
                                0
                            )
                        })

                        print(
                            f"Detected: {detected_vendor} "
                            f"({result.get('confidence_level')})"
                        )

                    else:
                        failed_scans += 1

                except Exception as e:
                    failed_scans += 1
                    print(f"Error: {e}")

    final_report = {
        "total_files": total_files,
        "successful_scans": successful_scans,
        "failed_scans": failed_scans,
        "vendor_statistics": dict(vendor_statistics),
        "metadata_reports": metadata_reports
    }

    os.makedirs("reports", exist_ok=True)

    output_path = os.path.join(
        "reports",
        "batch_metadata_report.json"
    )

    with open(output_path, "w", encoding="utf-8") as report_file:
        json.dump(final_report, report_file, indent=4)

    print("\n--- Batch Metadata Scan Summary ---")
    print(f"Total files analyzed: {total_files}")
    print(f"Successful scans: {successful_scans}")
    print(f"Failed scans: {failed_scans}")

    print("\nVendor Statistics:")
    for vendor, count in vendor_statistics.items():
        print(f"{vendor}: {count}")

    print(f"\nMetadata report saved to: {output_path}")


if __name__ == "__main__":
    target_directory = input(
        "Enter BIOS dataset directory path: "
    ).strip().strip('"')

    batch_metadata_scan(target_directory)