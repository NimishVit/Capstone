import csv
import os
import re
from datetime import datetime


# ============================================================
# FILE PATHS
# ============================================================

PARSED_FILE = "data/processed/OpenStack_2k_parsed.csv"
TEMPLATE_FILE = "data/processed/OpenStack_2k_template.csv"

EXPECTED_ROWS = 2000


# ============================================================
# EXPECTED COLUMNS
# ============================================================

PARSED_COLUMNS = [
    "LogFile",
    "Date",
    "Time",
    "PID",
    "Level",
    "Component",
    "Message"
]

TEMPLATE_COLUMNS = [
    "LogFile",
    "Date",
    "Time",
    "PID",
    "Level",
    "Component",
    "Message",
    "EventTemplate"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def print_section(title):
    print()
    print("=" * 55)
    print(title)
    print("=" * 55)


def check_file_exists(file_path):
    if os.path.exists(file_path):
        print("PASS - File exists:", file_path)
        return True
    else:
        print("FAIL - File not found:", file_path)
        return False


def check_columns(actual_columns, expected_columns):
    if actual_columns == expected_columns:
        print("PASS - Column structure is correct")
        print("Columns:", actual_columns)
        return True

    print("FAIL - Column structure mismatch")
    print("Expected:", expected_columns)
    print("Found   :", actual_columns)

    return False


# ============================================================
# VALIDATE PARSED CSV
# ============================================================

def validate_parsed_file():

    print_section("OPENSTACK PARSED DATA VALIDATION")

    if not check_file_exists(PARSED_FILE):
        return False

    total_rows = 0
    missing_rows = 0
    invalid_pid_rows = 0
    invalid_date_rows = 0
    invalid_time_rows = 0
    empty_message_rows = 0
    empty_level_rows = 0
    empty_component_rows = 0

    levels = {}
    unique_logs = set()

    try:

        with open(
            PARSED_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            # ------------------------------------------------
            # COLUMN CHECK
            # ------------------------------------------------

            if not check_columns(
                reader.fieldnames,
                PARSED_COLUMNS
            ):
                return False

            # ------------------------------------------------
            # ROW VALIDATION
            # ------------------------------------------------

            for row in reader:

                total_rows += 1

                # ============================================
                # MISSING VALUE CHECK
                # ============================================

                required_values = [
                    row.get("LogFile", ""),
                    row.get("Date", ""),
                    row.get("Time", ""),
                    row.get("PID", ""),
                    row.get("Level", ""),
                    row.get("Component", ""),
                    row.get("Message", "")
                ]

                if any(value.strip() == "" for value in required_values):
                    missing_rows += 1

                # ============================================
                # DATE CHECK
                # ============================================

                date_value = row.get("Date", "").strip()

                try:
                    datetime.strptime(
                        date_value,
                        "%Y-%m-%d"
                    )
                except ValueError:
                    invalid_date_rows += 1

                # ============================================
                # TIME CHECK
                # ============================================

                time_value = row.get("Time", "").strip()

                time_valid = re.match(
                    r"^\d{2}:\d{2}:\d{2}\.\d{3}$",
                    time_value
                )

                if not time_valid:
                    invalid_time_rows += 1

                # ============================================
                # PID CHECK
                # ============================================

                pid_value = row.get("PID", "").strip()

                try:
                    int(pid_value)
                except ValueError:
                    invalid_pid_rows += 1

                # ============================================
                # LEVEL CHECK
                # ============================================

                level = row.get("Level", "").strip()

                if level == "":
                    empty_level_rows += 1

                levels[level] = levels.get(level, 0) + 1

                # ============================================
                # COMPONENT CHECK
                # ============================================

                component = row.get("Component", "").strip()

                if component == "":
                    empty_component_rows += 1

                # ============================================
                # MESSAGE CHECK
                # ============================================

                message = row.get("Message", "").strip()

                if message == "":
                    empty_message_rows += 1

                # ============================================
                # DUPLICATE CHECK
                # ============================================

                unique_logs.add(
                    (
                        row.get("LogFile", ""),
                        row.get("Date", ""),
                        row.get("Time", ""),
                        row.get("PID", ""),
                        row.get("Level", ""),
                        row.get("Component", ""),
                        row.get("Message", "")
                    )
                )

        # ====================================================
        # DISPLAY BASIC RESULTS
        # ====================================================

        print()
        print("Total rows:", total_rows)
        print("Expected rows:", EXPECTED_ROWS)

        if total_rows == EXPECTED_ROWS:
            print("PASS - Row count is correct")
        else:
            print("FAIL - Row count mismatch")

        # ====================================================
        # MISSING VALUES
        # ====================================================

        print()
        print("Missing/incomplete rows:", missing_rows)

        if missing_rows == 0:
            print("PASS - No missing values")
        else:
            print("FAIL - Missing values found")

        # ====================================================
        # DATE VALIDATION
        # ====================================================

        print()
        print("Invalid dates:", invalid_date_rows)

        if invalid_date_rows == 0:
            print("PASS - Date format is valid")
        else:
            print("FAIL - Invalid dates found")

        # ====================================================
        # TIME VALIDATION
        # ====================================================

        print()
        print("Invalid times:", invalid_time_rows)

        if invalid_time_rows == 0:
            print("PASS - Time format is valid")
        else:
            print("FAIL - Invalid times found")

        # ====================================================
        # PID VALIDATION
        # ====================================================

        print()
        print("Invalid PID values:", invalid_pid_rows)

        if invalid_pid_rows == 0:
            print("PASS - PID values are valid")
        else:
            print("FAIL - Invalid PID values found")

        # ====================================================
        # LEVEL VALIDATION
        # ====================================================

        print()
        print("Empty Level values:", empty_level_rows)

        if empty_level_rows == 0:
            print("PASS - Level values are present")
        else:
            print("FAIL - Empty Level values found")

        # ====================================================
        # COMPONENT VALIDATION
        # ====================================================

        print()
        print("Empty Component values:", empty_component_rows)

        if empty_component_rows == 0:
            print("PASS - Component values are present")
        else:
            print("FAIL - Empty Component values found")

        # ====================================================
        # MESSAGE VALIDATION
        # ====================================================

        print()
        print("Empty Message values:", empty_message_rows)

        if empty_message_rows == 0:
            print("PASS - Message values are present")
        else:
            print("FAIL - Empty Message values found")

        # ====================================================
        # DUPLICATE CHECK
        # ====================================================

        duplicate_rows = total_rows - len(unique_logs)

        print()
        print("Duplicate rows:", duplicate_rows)

        if duplicate_rows == 0:
            print("PASS - No duplicate rows")
        else:
            print(
                "INFO - Duplicate rows found:",
                duplicate_rows
            )

        # ====================================================
        # LEVEL DISTRIBUTION
        # ====================================================

        print()
        print("Log Level Distribution:")
        print("-" * 40)

        for level, count in sorted(
            levels.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            print(level, ":", count)

        # ====================================================
        # FINAL PARSED VALIDATION
        # ====================================================

        parsed_pass = (
            total_rows == EXPECTED_ROWS
            and missing_rows == 0
            and invalid_date_rows == 0
            and invalid_time_rows == 0
            and invalid_pid_rows == 0
            and empty_level_rows == 0
            and empty_component_rows == 0
            and empty_message_rows == 0
        )

        print()

        if parsed_pass:
            print("PARSED DATA VALIDATION: PASSED")
        else:
            print("PARSED DATA VALIDATION: FAILED")

        return parsed_pass

    except Exception as error:

        print()
        print("ERROR while validating parsed file:")
        print(error)

        return False


# ============================================================
# VALIDATE TEMPLATE CSV
# ============================================================

def validate_template_file():

    print_section("OPENSTACK TEMPLATE DATA VALIDATION")

    if not check_file_exists(TEMPLATE_FILE):
        return False

    total_rows = 0
    empty_template_rows = 0
    placeholder_rows = 0

    templates = set()

    try:

        with open(
            TEMPLATE_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            # ------------------------------------------------
            # COLUMN CHECK
            # ------------------------------------------------

            if not check_columns(
                reader.fieldnames,
                TEMPLATE_COLUMNS
            ):
                return False

            # ------------------------------------------------
            # TEMPLATE VALIDATION
            # ------------------------------------------------

            for row in reader:

                total_rows += 1

                event_template = row.get(
                    "EventTemplate",
                    ""
                ).strip()

                # ============================================
                # EMPTY TEMPLATE CHECK
                # ============================================

                if event_template == "":
                    empty_template_rows += 1
                    continue

                # ============================================
                # STORE UNIQUE TEMPLATE
                # ============================================

                templates.add(event_template)

                # ============================================
                # PLACEHOLDER CHECK
                # ============================================

                if "<*>" in event_template:
                    placeholder_rows += 1

        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        print()
        print("Total template rows:", total_rows)
        print("Expected rows:", EXPECTED_ROWS)

        if total_rows == EXPECTED_ROWS:
            print("PASS - Template row count is correct")
        else:
            print("FAIL - Template row count mismatch")

        # ====================================================
        # EMPTY TEMPLATE CHECK
        # ====================================================

        print()
        print("Empty EventTemplate rows:", empty_template_rows)

        if empty_template_rows == 0:
            print("PASS - No empty templates")
        else:
            print("FAIL - Empty templates found")

        # ====================================================
        # UNIQUE TEMPLATE COUNT
        # ====================================================

        print()
        print("Unique EventTemplates:", len(templates))

        # ====================================================
        # PLACEHOLDER INFORMATION
        # ====================================================

        print()
        print(
            "Rows containing <*>:",
            placeholder_rows
        )

        # ====================================================
        # FINAL TEMPLATE VALIDATION
        # ====================================================

        template_pass = (
            total_rows == EXPECTED_ROWS
            and empty_template_rows == 0
        )

        print()

        if template_pass:
            print("TEMPLATE DATA VALIDATION: PASSED")
        else:
            print("TEMPLATE DATA VALIDATION: FAILED")

        return template_pass

    except Exception as error:

        print()
        print("ERROR while validating template file:")
        print(error)

        return False


# ============================================================
# COMPARE PARSED AND TEMPLATE FILES
# ============================================================

def compare_files():

    print_section("PARSED VS TEMPLATE FILE COMPARISON")

    if not os.path.exists(PARSED_FILE):
        print("FAIL - Parsed file does not exist")
        return False

    if not os.path.exists(TEMPLATE_FILE):
        print("FAIL - Template file does not exist")
        return False

    try:

        # ----------------------------------------------------
        # COUNT PARSED ROWS
        # ----------------------------------------------------

        with open(
            PARSED_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            parsed_reader = csv.DictReader(file)
            parsed_rows = list(parsed_reader)

        # ----------------------------------------------------
        # COUNT TEMPLATE ROWS
        # ----------------------------------------------------

        with open(
            TEMPLATE_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            template_reader = csv.DictReader(file)
            template_rows = list(template_reader)

        # ----------------------------------------------------
        # ROW COUNT COMPARISON
        # ----------------------------------------------------

        print("Parsed rows:", len(parsed_rows))
        print("Template rows:", len(template_rows))

        if len(parsed_rows) == len(template_rows):
            print("PASS - Parsed and template row counts match")
        else:
            print("FAIL - Row counts do not match")
            return False

        # ----------------------------------------------------
        # MESSAGE VS TEMPLATE ALIGNMENT
        # ----------------------------------------------------

        mismatch_count = 0

        for parsed_row, template_row in zip(
            parsed_rows,
            template_rows
        ):

            parsed_message = parsed_row.get(
                "Message",
                ""
            )

            template_message = template_row.get(
                "Message",
                ""
            )

            if parsed_message != template_message:
                mismatch_count += 1

        print()
        print(
            "Message alignment mismatches:",
            mismatch_count
        )

        if mismatch_count == 0:
            print("PASS - Parsed and template rows are aligned")
        else:
            print("FAIL - Message alignment mismatch")

        # ----------------------------------------------------
        # FINAL COMPARISON
        # ----------------------------------------------------

        comparison_pass = (
            len(parsed_rows) == len(template_rows)
            and mismatch_count == 0
        )

        print()

        if comparison_pass:
            print("FILE COMPARISON: PASSED")
        else:
            print("FILE COMPARISON: FAILED")

        return comparison_pass

    except Exception as error:

        print()
        print("ERROR while comparing files:")
        print(error)

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 55)
    print("OPENSTACK DATA VALIDATION")
    print("=" * 55)

    print()
    print("Parsed file:")
    print(PARSED_FILE)

    print()
    print("Template file:")
    print(TEMPLATE_FILE)

    # --------------------------------------------------------
    # STEP 1: PARSED DATA
    # --------------------------------------------------------

    parsed_result = validate_parsed_file()

    # --------------------------------------------------------
    # STEP 2: TEMPLATE DATA
    # --------------------------------------------------------

    template_result = validate_template_file()

    # --------------------------------------------------------
    # STEP 3: COMPARE BOTH FILES
    # --------------------------------------------------------

    comparison_result = compare_files()

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print()
    print("=" * 55)
    print("FINAL OPENSTACK VALIDATION RESULT")
    print("=" * 55)

    print(
        "Parsed data   :",
        "PASSED" if parsed_result else "FAILED"
    )

    print(
        "Template data :",
        "PASSED" if template_result else "FAILED"
    )

    print(
        "Comparison    :",
        "PASSED" if comparison_result else "FAILED"
    )

    print()

    if (
        parsed_result
        and template_result
        and comparison_result
    ):
        print("OPENSTACK DATA VALIDATION: PASSED")
        print("OpenStack preprocessing is ready.")
    else:
        print("OPENSTACK DATA VALIDATION: FAILED")
        print("Please check the errors above.")

    print("=" * 55)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()