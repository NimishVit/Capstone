import csv
from collections import Counter


# ========================================
# DATASET CONFIGURATION
# ========================================

datasets = {
    "HDFS": "data/processed/HDFS_2k_template.csv",
    "BGL": "data/processed/BGL_2k_template.csv",
    "OpenStack": "data/processed/OpenStack_2k_template.csv"
}


# ========================================
# ANALYSIS FUNCTION
# ========================================

def analyze_dataset(dataset_name, input_file):

    templates = []
    levels = []

    # ------------------------------------
    # READ CSV
    # ------------------------------------

    with open(
        input_file,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            # Make sure required columns exist
            if "EventTemplate" in row:
                templates.append(row["EventTemplate"])

            if "Level" in row:
                levels.append(row["Level"])


    # ------------------------------------
    # BASIC STATISTICS
    # ------------------------------------

    total_logs = len(templates)

    template_count = Counter(templates)

    unique_templates = len(template_count)

    level_count = Counter(levels)


    # ------------------------------------
    # DISPLAY RESULTS
    # ------------------------------------

    print()
    print("========================================")
    print(dataset_name, "TEMPLATE ANALYSIS")
    print("========================================")

    print("Input file:", input_file)
    print("Total logs:", total_logs)
    print("Unique templates:", unique_templates)

    if total_logs > 0:

        template_ratio = unique_templates / total_logs

        print(
            "Template diversity ratio:",
            f"{template_ratio:.4f}"
        )

    print()


    # ------------------------------------
    # LOG LEVEL DISTRIBUTION
    # ------------------------------------

    print("Log Level Distribution:")
    print("----------------------------------------")

    if level_count:

        for level, count in level_count.most_common():

            percentage = (count / total_logs) * 100

            print(
                level,
                ":",
                count,
                f"({percentage:.2f}%)"
            )

    else:

        print("Level column not available.")

    print()


    # ------------------------------------
    # TOP 10 TEMPLATES
    # ------------------------------------

    print("Top 10 Most Frequent Templates:")
    print("----------------------------------------")

    for template, count in template_count.most_common(10):

        print("Count:", count)
        print("Template:", template)
        print()


    # ------------------------------------
    # RARE TEMPLATES
    # ------------------------------------

    rare_templates = [
        (template, count)
        for template, count in template_count.items()
        if count == 1
    ]

    print("Rare Templates:")
    print("----------------------------------------")

    print(
        "Number of rare templates:",
        len(rare_templates)
    )

    if total_logs > 0:

        rare_ratio = len(rare_templates) / total_logs

        print(
            "Rare template ratio:",
            f"{rare_ratio:.4f}"
        )

    print()

    # Show first 10 rare templates

    for template, count in rare_templates[:10]:

        print("Count:", count)
        print("Template:", template)
        print()


    print("========================================")
    print(dataset_name, "TEMPLATE ANALYSIS COMPLETED")
    print("========================================")


# ========================================
# RUN ANALYSIS FOR ALL DATASETS
# ========================================

for dataset_name, input_file in datasets.items():

    analyze_dataset(
        dataset_name,
        input_file
    )