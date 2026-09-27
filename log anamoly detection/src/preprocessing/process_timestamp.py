import csv
from datetime import datetime

input_file = "data/processed/HDFS_2k_parsed.csv"
output_file = "data/processed/HDFS_2k_timestamp.csv"

total_rows = 0
successful_rows = 0
failed_rows = 0

with open(input_file, "r", newline="", encoding="utf-8") as file, \
     open(output_file, "w", newline="", encoding="utf-8") as output:

    reader = csv.DictReader(file)

    fieldnames = [
        "Date",
        "Time",
        "Timestamp",
        "Number",
        "Level",
        "Component",
        "Message"
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        total_rows += 1

        try:
            timestamp = datetime.strptime(
                row["Date"] + row["Time"],
                "%y%m%d%H%M%S"
            )

            row["Timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow({
                "Date": row["Date"],
                "Time": row["Time"],
                "Timestamp": row["Timestamp"],
                "Number": row["Number"],
                "Level": row["Level"],
                "Component": row["Component"],
                "Message": row["Message"]
            })

            successful_rows += 1

        except ValueError:
            failed_rows += 1

print("===================================")
print("HDFS TIMESTAMP PROCESSING")
print("===================================")
print("Total rows:", total_rows)
print("Successful:", successful_rows)
print("Failed:", failed_rows)
print("CSV created:", output_file)
print("===================================")