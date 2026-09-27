import csv
import os

input_file = "data/raw/HDFS_2k.log"
output_file = "data/processed/HDFS_2k_parsed.csv"

# Make sure processed folder exists
os.makedirs("data/processed", exist_ok=True)

total_lines = 0
parsed_lines = 0
malformed_lines = 0

with open(input_file, "r", encoding="utf-8") as file, \
     open(output_file, "w", newline="", encoding="utf-8") as csv_file:

    writer = csv.writer(csv_file)

    # Write column names
    writer.writerow([
        "Date",
        "Time",
        "Number",
        "Level",
        "Component",
        "Message"
    ])

    for line in file:

        total_lines += 1

        # Remove extra spaces/newline
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        parts = line.split()

        # A valid HDFS log should have at least:
        # Date, Time, Number, Level, Component
        if len(parts) < 5:
            malformed_lines += 1
            continue

        date = parts[0]
        time = parts[1]
        number = parts[2]
        level = parts[3]
        component = parts[4].rstrip(":")
        message = " ".join(parts[5:])

        # Basic validation
        if not date or not time or not number or not level or not component:
            malformed_lines += 1
            continue

        writer.writerow([
            date,
            time,
            number,
            level,
            component,
            message
        ])

        parsed_lines += 1


print("===================================")
print("HDFS LOG PREPROCESSING COMPLETED")
print("===================================")
print("Total lines read:", total_lines)
print("Successfully parsed:", parsed_lines)
print("Malformed lines:", malformed_lines)
print("CSV created:", output_file)
print("===================================")