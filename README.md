# ALU Transcript Generator

Introduction to Python Programming and Databases, BSE Year 1 Trimester 2.

## Files

- `grade-evaluator.py`: reads a CSV of grades, validates scores and weights, calculates the final grade and GPA, prints PASSED/FAILED and lists the formative assignment(s) eligible for resubmission.
- `organizer.sh`: archives `grades.csv` into `archive/` with a timestamp, creates a fresh empty `grades.csv`, and appends the action to `organizer.log`.
- `grades.csv`: sample grade data.

## Usage

```bash
python3 grade-evaluator.py
# Enter the name of the CSV file to process: grades.csv

chmod +x organizer.sh
./organizer.sh
```

Run the Python script before the organizer, because the organizer empties `grades.csv`.

## Rules implemented

- Every score must be between 0 and 100.
- Total weight = 100, Formative = 60, Summative = 40.
- GPA = (Total Grade / 100) * 5.0.
- PASSED only with at least 50% in both Formative and Summative.
- Resubmission: failed formative assignment(s) (< 50) with the highest weight; ties are all listed.
