import joblib
import numpy as np
import sys

# Load the pre-trained decision tree model
try:
    tree = joblib.load("public_cases_tree.joblib")
except FileNotFoundError:
    print("Error: Model file 'public_cases_tree.joblib' not found.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error loading model: {e}", file=sys.stderr)
    sys.exit(1)

def legacy_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Calculates the legacy reimbursement amount using the pre-trained decision tree model.
    """
    try:
        features = np.array([[float(trip_duration_days), float(miles_traveled), float(total_receipts_amount)]])
        prediction = tree.predict(features)[0]
        return float(prediction)
    except Exception as e:
        print(f"Error during prediction: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python reimbursement_calculator.py <trip_duration_days> <miles_traveled> <total_receipts_amount>", file=sys.stderr)
        sys.exit(1)

    try:
        trip_duration_days_arg = sys.argv[1]
        miles_traveled_arg = sys.argv[2]
        total_receipts_amount_arg = sys.argv[3]

        reimbursement = legacy_reimbursement(trip_duration_days_arg, miles_traveled_arg, total_receipts_amount_arg)
        print(f"{reimbursement:.2f}")  # Output rounded to 2 decimal places
    except ValueError as e:
        print(f"Error: Invalid input. All inputs must be numbers. Details: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
