import csv
from collections import Counter

input_file = "data/processed/HDFS_2k_timestamp.csv"

level_count = Counter()
component_count = Counter()

total_logs = 0

with open(input_file, "r", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:
        total_logs += 1

        level_count[row["Level"]] += 1
        component_count[row["Component"]] += 1


print("===================================")
print("HDFS LOG ANALYSIS")
print("===================================")

print("Total logs:", total_logs)

print("\nLog Level Distribution:")
for level, count in level_count.items():
    print(level, ":", count)

print("\nTop Components:")

for component, count in component_count.most_common(10):
    print(component, ":", count)

print("===================================")