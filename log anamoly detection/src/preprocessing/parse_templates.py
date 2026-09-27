import csv
import re
import os


# ============================================================
# CONFIGURATION
# ============================================================

input_file = "data/processed/HDFS_2k_timestamp.csv"
output_file = "data/processed/HDFS_2k_template.csv"


# ============================================================
# TEMPLATE GENERATION
# ============================================================

def generate_template(message):

    template = message

    # --------------------------------------------------------
    # Replace HDFS block IDs
    # Example:
    # blk_123456789
    # blk_-123456789
    # --------------------------------------------------------
    template = re.sub(
        r"blk_-?\d+",
        "<*>",
        template
    )

    # --------------------------------------------------------
    # Replace IP addresses
    # Example:
    # 192.168.1.10
    # --------------------------------------------------------
    template = re.sub(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "<*>",
        template
    )

    # --------------------------------------------------------
    # Replace hexadecimal-like IDs
    # Example:
    # abc123456789
    # --------------------------------------------------------
    template = re.sub(
        r"\b[0-9a-fA-F]{8,}\b",
        "<*>",
        template
    )

    # --------------------------------------------------------
    # Replace numbers
    # Example:
    # 123
    # 4567
    # --------------------------------------------------------
    template = re.sub(
        r"\b\d+\b",
        "<*>",
        template
    )

    return template


# ============================================================
# PROCESS CSV
# ============================================================

total_rows = 0
processed_rows = 0
failed_rows = 0


with open(
    input_file,
    "r",
    newline="",
    encoding="utf-8"
) as file, \
open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    reader = csv.DictReader(file)

    # Check that Message column exists
    if "Message" not in reader.fieldnames:
        raise ValueError(
            "ERROR: 'Message' column not found in input CSV."
        )

    fieldnames = reader.fieldnames + ["EventTemplate"]

    writer = csv.DictWriter(
        csv_file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    for row in reader:

        total_rows += 1

        try:

            message = row["Message"]

            if message is None:
                message = ""

            event_template = generate_template(message)

            row["EventTemplate"] = event_template

            writer.writerow(row)

            processed_rows += 1

        except Exception as e:

            failed_rows += 1

            print(
                f"Error processing row {total_rows}: {e}"
            )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("========================================")
print("HDFS LOG TEMPLATE PARSING")
print("========================================")

print("Input file:", input_file)
print("Output file:", output_file)

print("Total rows:", total_rows)
print("Successfully processed:", processed_rows)
print("Failed rows:", failed_rows)

print("========================================")