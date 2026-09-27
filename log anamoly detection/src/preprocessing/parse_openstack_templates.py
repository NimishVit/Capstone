import csv
import re

input_file = "data/processed/OpenStack_2k_parsed.csv"
output_file = "data/processed/OpenStack_2k_template.csv"


def generate_template(message):
    template = message

    # Replace IP addresses
    template = re.sub(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "<*>",
        template
    )

    # Replace UUIDs
    template = re.sub(
        r"\b[0-9a-fA-F]{8}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{12}\b",
        "<*>",
        template
    )

    # Replace hexadecimal-like IDs
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

    # Replace quoted strings
    template = re.sub(
        r"'[^']*'",
        "'<*>'",
        template
    )

    template = re.sub(
        r'"[^"]*"',
        '"<*>"',
        template
    )

    # Remove extra spaces
    template = re.sub(r"\s+", " ", template).strip()

    return template


total_rows = 0
processed_rows = 0
failed_rows = 0


with open(
    input_file,
    "r",
    newline="",
    encoding="utf-8"
) as file, open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    reader = csv.DictReader(file)

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

            event_template = generate_template(message)

            row["EventTemplate"] = event_template

            writer.writerow(row)

            processed_rows += 1

        except Exception:
            failed_rows += 1


print("========================================")
print("OPENSTACK LOG TEMPLATE PARSING")
print("========================================")
print("Input file:", input_file)
print("Output file:", output_file)
print("Total rows:", total_rows)
print("Successfully processed:", processed_rows)
print("Failed rows:", failed_rows)

if total_rows > 0:
    success_rate = (processed_rows / total_rows) * 100
    print(f"Parsing success rate: {success_rate:.2f}%")

print("========================================")