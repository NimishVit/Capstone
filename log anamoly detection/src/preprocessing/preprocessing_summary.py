import csv
from collections import Counter

input_file = "data/processed/HDFS_2k_template.csv"

total_rows = 0
levels = Counter()
components = Counter()
templates = Counter()

with open(input_file, "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    print("Columns:")
    print(reader.fieldnames)

    for row in reader:
        total_rows += 1

        levels[row["Level"]] += 1
        components[row["Component"]] += 1
        templates[row["EventTemplate"]] += 1


print("\n========================================")
print("FINAL PREPROCESSING SUMMARY")
print("========================================")

print("Total logs:", total_rows)
print("Unique log levels:", len(levels))
print("Unique components:", len(components))
print("Unique templates:", len(templates))

print("\nLog Level Distribution:")
for level, count in levels.items():
    print(level, ":", count)

print("\nTop 10 Components:")
for component, count in components.most_common(10):
    print(component, ":", count)

print("\nTop 10 Templates:")
for template, count in templates.most_common(10):
    print(count, ":", template)

print("\n========================================")
print("PREPROCESSING READY FOR FEATURE ENGINEERING")
print("========================================")