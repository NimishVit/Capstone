import csv
import re


# ============================================================
# FILE CONFIGURATION
# ============================================================

input_file = "data/processed/BGL_2k_parsed.csv"
output_file = "data/processed/BGL_2k_template.csv"


# ============================================================
# BGL TEMPLATE GENERATION
# ============================================================

def generate_template(message):

    template = message

    # Replace IP addresses
    template = re.sub(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "<*>",
        template
    )

    # Replace hexadecimal values / IDs
    template = re.sub(
        r"\b[0-9a-fA-F]{8,}\b",
        "<*>",
        template
    )

    # Replace numbers
    template = re.sub(
        r"\b\d+\b",
        "<*>",
        template
    )

    # Replace values containing numbers
    # Example: node123 -> node<*>
    template = re.sub(
        r"\b[A-Za-z_-]*\d+[A-Za-z0-9_-]*\b",
        "<*>",
        template
    )

    return template


# ============================================================
# PROCESS BGL CSV
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

    # Check Message column
    if "Message" not in reader.fieldnames:
        raise ValueError(
            "ERROR: 'Message' column not found."
        )

    # Add EventTemplate column
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
# FINAL OUTPUT
# ============================================================

print("========================================")
print("BGL LOG TEMPLATE PARSING")
print("========================================")

print("Input file:", input_file)
print("Output file:", output_file)

print("Total rows:", total_rows)
print("Successfully processed:", processed_rows)
print("Failed rows:", failed_rows)

print("========================================")