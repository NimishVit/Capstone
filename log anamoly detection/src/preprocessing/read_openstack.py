import csv
import re


# ============================================================
# FILE PATHS
# ============================================================

input_file = "data/raw/OpenStack_2k.log"
output_file = "data/processed/OpenStack_2k_parsed.csv"


# ============================================================
# OPENSTACK LOG PARSER
# ============================================================

def parse_openstack_line(line):
    """
    Parse one OpenStack log line.

    Expected format:

    nova-api.log.1.2017-05-16_13:53:08
    2017-05-16
    00:00:00.008
    25746
    INFO
    nova.osapi_compute...
    [message]
    """

    line = line.strip()

    if not line:
        return None

    # Split only first 6 parts.
    # Message may contain spaces, so we keep the remaining
    # portion as Message.
    parts = line.split(maxsplit=6)

    if len(parts) < 7:
        return None

    log_file = parts[0]
    date = parts[1]
    time = parts[2]
    pid = parts[3]
    level = parts[4]
    component = parts[5]
    message = parts[6]

    return {
        "LogFile": log_file,
        "Date": date,
        "Time": time,
        "PID": pid,
        "Level": level,
        "Component": component,
        "Message": message
    }


# ============================================================
# PROCESS LOG FILE
# ============================================================

total_lines = 0
successful_lines = 0
malformed_lines = 0

rows = []


with open(input_file, "r", encoding="utf-8", errors="replace") as file:

    for line in file:

        total_lines += 1

        parsed = parse_openstack_line(line)

        if parsed is not None:
            rows.append(parsed)
            successful_lines += 1
        else:
            malformed_lines += 1


# ============================================================
# WRITE CSV
# ============================================================

fieldnames = [
    "LogFile",
    "Date",
    "Time",
    "PID",
    "Level",
    "Component",
    "Message"
]


with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    writer = csv.DictWriter(
        csv_file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(rows)


# ============================================================
# SUMMARY
# ============================================================

print("========================================")
print("OPENSTACK LOG PREPROCESSING COMPLETED")
print("========================================")

print("Input file:", input_file)
print("Output file:", output_file)

print("Total lines:", total_lines)
print("Successfully parsed:", successful_lines)
print("Malformed lines:", malformed_lines)

if total_lines > 0:
    success_rate = (successful_lines / total_lines) * 100
    print("Parsing success rate: {:.2f}%".format(success_rate))

print("========================================")