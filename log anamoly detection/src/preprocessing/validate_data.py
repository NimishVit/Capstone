import csv

input_file = "data/processed/HDFS_2k_parsed.csv"

total_rows = 0
missing_values = 0

with open(input_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    print("Columns:")
    print(reader.fieldnames)
    print()

    for row in reader:
        total_rows += 1

        for value in row.values():
            if value is None or value.strip() == "":
                missing_values += 1

print("===================================")
print("HDFS DATA VALIDATION")
print("===================================")
print("Total rows:", total_rows)
print("Missing values:", missing_values)
print("===================================")