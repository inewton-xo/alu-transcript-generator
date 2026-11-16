import csv
import math
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Validates the data, calculates the final grade and GPA,
    decides PASSED/FAILED and lists resubmission options.
    """
    print("\n--- Processing Grades ---")

    if not data:
        print("Error: no assignment records found in the file.")
        sys.exit(1)

    # a) Grade validation: every score must be between 0 and 100
    invalid = [a for a in data if not (0 <= a['score'] <= 100)]
    if invalid:
        for a in invalid:
            print(f"Error: score for '{a['assignment']}' is {a['score']:g}, "
                  f"which is outside the 0-100 range.")
        sys.exit(1)

    # Weights must be positive numbers
    bad_weights = [a for a in data if not (a['weight'] > 0)]
    if bad_weights:
        for a in bad_weights:
            print(f"Error: weight for '{a['assignment']}' is {a['weight']:g}, "
                  f"it must be greater than 0.")
        sys.exit(1)

    # b) Weight validation: total=100, Formative=60, Summative=40
    formative = [a for a in data if a['group'].strip().lower() == 'formative']
    summative = [a for a in data if a['group'].strip().lower() == 'summative']

    total_weight = sum(a['weight'] for a in data)
    formative_weight = sum(a['weight'] for a in formative)
    summative_weight = sum(a['weight'] for a in summative)

    weight_errors = []
    if not math.isclose(total_weight, 100):
        weight_errors.append(f"Total weight is {total_weight:g}, expected 100.")
    if not math.isclose(formative_weight, 60):
        weight_errors.append(f"Formative weight is {formative_weight:g}, expected 60.")
    if not math.isclose(summative_weight, 40):
        weight_errors.append(f"Summative weight is {summative_weight:g}, expected 40.")
    if weight_errors:
        for err in weight_errors:
            print(f"Error: {err}")
        sys.exit(1)

    # c) Final grade and GPA
    formative_earned = sum(a['score'] * a['weight'] / 100 for a in formative)
    summative_earned = sum(a['score'] * a['weight'] / 100 for a in summative)
    total_grade = formative_earned + summative_earned
    gpa = (total_grade / 100) * 5.0

    # d) Pass/Fail: at least 50% in BOTH categories
    formative_pct = formative_earned / formative_weight * 100
    summative_pct = summative_earned / summative_weight * 100
    passed = formative_pct >= 50 and summative_pct >= 50

    print(f"Formative: {formative_earned:.2f}/{formative_weight:g} ({formative_pct:.2f}%)")
    print(f"Summative: {summative_earned:.2f}/{summative_weight:g} ({summative_pct:.2f}%)")
    print(f"Total Grade: {total_grade:.2f}/100")
    print(f"GPA: {gpa:.2f}")
    print(f"Final Status: {'PASSED' if passed else 'FAILED'}")

    # e) Resubmission: failed formatives (< 50) with the highest weight
    failed = [a for a in formative if a['score'] < 50]
    if failed:
        max_weight = max(a['weight'] for a in failed)
        resubmit = [a for a in failed if a['weight'] == max_weight]
        print("\nEligible for resubmission:")
        for a in resubmit:
            print(f"  - {a['assignment']} (score: {a['score']:g}, weight: {a['weight']:g})")
    else:
        print("\nNo failed formative assignments. No resubmission needed.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)