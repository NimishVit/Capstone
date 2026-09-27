import csv

input_file = "data/processed/BGL_2k_parsed.csv"

total_rows = 0
missing_values = 0

expected_columns = [
    "Label",
    "Timestamp",
    "Date",
    "Node",
    "Time",
    "NodeRepeat",
    "Type",
    "Component",
    "Level",
    "Message"
]

with open(input_file, "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    print("Columns:")
    print(reader.fieldnames)

    # Check columns
    if reader.fieldnames == expected_columns:
        print("\nColumn structure: OK")
    else:
        print("\nColumn structure: ERROR")

    for row in reader:

        total_rows += 1

        # Check missing values
        for column in expected_columns:
            if not row[column].strip():
                missing_values += 1

print("\n========================================")
print("BGL DATA VALIDATION")
print("========================================")
print("Total rows:", total_rows)
print("Missing values:", missing_values)
print("========================================")