import csv

input_file = "data/raw/BGL_2k.log"
output_file = "data/processed/BGL_2k_parsed.csv"

total_lines = 0
parsed_lines = 0
malformed_lines = 0

with open(input_file, "r", encoding="utf-8") as file, \
     open(output_file, "w", newline="", encoding="utf-8") as csv_file:

    writer = csv.writer(csv_file)

    # Column names
    writer.writerow([
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
    ])

    for line in file:

        total_lines += 1

        line = line.strip()

        if not line:
            continue

        # BGL has 9 fixed fields before message
        parts = line.split(maxsplit=9)

        if len(parts) < 10:
            malformed_lines += 1
            continue

        label = parts[0]
        timestamp = parts[1]
        date = parts[2]
        node = parts[3]
        time = parts[4]
        node_repeat = parts[5]
        event_type = parts[6]
        component = parts[7]
        level = parts[8]
        message = parts[9]

        writer.writerow([
            label,
            timestamp,
            date,
            node,
            time,
            node_repeat,
            event_type,
            component,
            level,
            message
        ])

        parsed_lines += 1


print("========================================")
print("BGL LOG PREPROCESSING COMPLETED")
print("========================================")
print("Total lines read:", total_lines)
print("Successfully parsed:", parsed_lines)
print("Malformed lines:", malformed_lines)
print("CSV created:", output_file)
print("========================================")