#!/usr/bin/env python3
"""
Decision Tree Optimizer - Fine-tune the decision tree for score 0
"""

import json
from solution import calculate_reimbursement as current_best

# Load the data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

print("Analyzing current decision tree performance...")
print("=" * 60)

# Analyze all errors
errors = []
for case in data:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    predicted = current_best(days, miles, receipts)
    error = predicted - expected  # Signed error
    
    errors.append({
        'days': days,
        'miles': miles,
        'receipts': receipts,
        'expected': expected,
        'predicted': predicted,
        'error': error,
        'abs_error': abs(error)
    })

# Sort by absolute error
errors.sort(key=lambda x: x['abs_error'], reverse=True)

print(f"Total cases: {len(errors)}")
print(f"Average absolute error: ${sum(e['abs_error'] for e in errors) / len(errors):.2f}")

# Analyze systematic biases
overestimates = [e for e in errors if e['error'] > 1]
underestimates = [e for e in errors if e['error'] < -1]

print(f"\nOverestimates (>$1): {len(overestimates)}")
print(f"Underestimates (<-$1): {len(underestimates)}")

# Find patterns in errors
print("\nTop 20 errors with patterns:")
for i, e in enumerate(errors[:20]):
    print(f"\n{i+1}. Error: ${e['error']:.2f} (predicted ${e['predicted']:.2f}, expected ${e['expected']:.2f})")
    print(f"   Input: {e['days']}d, {e['miles']}mi, ${e['receipts']:.2f}")
    
    # Calculate features
    miles_per_day = e['miles'] / e['days'] if e['days'] > 0 else 0
    receipts_per_day = e['receipts'] / e['days'] if e['days'] > 0 else 0
    days_x_miles = e['days'] * e['miles']
    
    print(f"   Features: {miles_per_day:.1f} mi/day, ${receipts_per_day:.2f}/day, days×miles={days_x_miles}")
    
    # Find correction factor
    if e['predicted'] > 0:
        correction = e['expected'] / e['predicted']
        print(f"   Correction needed: {correction:.3f}x")

# Look for patterns by features
print("\n" + "="*60)
print("PATTERN ANALYSIS:")

# Group by receipt ranges
receipt_ranges = [
    (0, 500, 'low'),
    (500, 1000, 'medium'),
    (1000, 1500, 'high'),
    (1500, 3000, 'very_high')
]

for min_r, max_r, label in receipt_ranges:
    range_errors = [e for e in errors if min_r <= e['receipts'] < max_r]
    if range_errors:
        avg_error = sum(e['error'] for e in range_errors) / len(range_errors)
        avg_abs_error = sum(e['abs_error'] for e in range_errors) / len(range_errors)
        print(f"\nReceipts {label} (${min_r}-${max_r}): {len(range_errors)} cases")
        print(f"  Average error: ${avg_error:.2f} (abs: ${avg_abs_error:.2f})")
        
        # Find systematic bias
        if abs(avg_error) > 10:
            if avg_error > 0:
                print(f"  → Systematically OVER-estimating by ${avg_error:.2f}")
            else:
                print(f"  → Systematically UNDER-estimating by ${-avg_error:.2f}")

# Generate correction code
print("\n" + "="*60)
print("GENERATING OPTIMIZED SOLUTION...")

code = '''#!/usr/bin/env python3

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    # Calculate derived features (same as decision tree)
    miles_per_day = miles_traveled / trip_duration_days if trip_duration_days > 0 else 0
    receipts_per_day = total_receipts_amount / trip_duration_days if trip_duration_days > 0 else 0
    receipts_per_mile = total_receipts_amount / miles_traveled if miles_traveled > 0 else 0
    days_x_miles = trip_duration_days * miles_traveled
    days_x_receipts = trip_duration_days * total_receipts_amount
    miles_x_receipts = miles_traveled * total_receipts_amount
    
    # Use the same decision tree logic
    if total_receipts_amount <= 828.10:
        if days_x_miles <= 2070.00:
            if days_x_receipts <= 487.54:
                if days_x_miles <= 566.00:
                    if days_x_miles <= 210.50:
                        total = 196.57
                    else:
                        total = 336.31
                else:
                    total = 559.32
            else:
                if days_x_receipts <= 4036.29:
                    if days_x_miles <= 1310.50:
                        if total_receipts_amount <= 588.27:
                            if trip_duration_days <= 4.50:
                                total = 492.73
                            else:
                                total = 619.95
                        else:
                            total = 719.40
                    else:
                        if days_x_receipts <= 1467.28:
                            total = 700.75
                        else:
                            total = 828.74
                else:
                    total = 935.06
        else:
            if days_x_miles <= 4945.50:
                if total_receipts_amount <= 570.45:
                    if days_x_receipts <= 1790.10:
                        if days_x_miles <= 3963.60:
                            if receipts_per_mile <= 0.41:
                                total = 750.44
                            else:
                                total = 788.25
                        else:
                            total = 845.60
                    else:
                        if miles_traveled <= 628.50:
                            if receipts_per_mile <= 1.11:
                                total = 925.07
                            else:
                                total = 853.04
                        else:
                            total = 1000.77
                else:
                    if total_receipts_amount <= 691.05:
                        total = 1019.89
                    else:
                        total = 1170.65
            else:
                if miles_x_receipts <= 529812.36:
                    if trip_duration_days <= 10.50:
                        if days_x_receipts <= 2838.70:
                            if receipts_per_mile <= 0.18:
                                total = 1111.45
                            else:
                                total = 1042.71
                        else:
                            total = 1208.17
                    else:
                        if days_x_miles <= 11460.50:
                            if miles_x_receipts <= 218691.81:
                                total = 1213.97
                            else:
                                total = 1298.64
                        else:
                            total = 1364.90
                else:
                    if days_x_receipts <= 5526.72:
                        total = 1417.53
                    else:
                        total = 1611.04
    else:
        if days_x_miles <= 3873.00:
            if days_x_receipts <= 5494.43:
                if miles_x_receipts <= 385934.73:
                    if total_receipts_amount <= 1082.07:
                        if days_x_receipts <= 3208.57:
                            total = 949.66
                        else:
                            total = 1099.06
                    else:
                        total = 1239.56
                else:
                    if miles_x_receipts <= 1033628.09:
                        if days_x_receipts <= 2736.24:
                            if miles_x_receipts <= 827348.03:
                                total = 1176.45
                            else:
                                total = 1261.61
                        else:
                            if total_receipts_amount <= 942.36:
                                total = 1288.02
                            else:
                                total = 1376.78
                    else:
                        if days_x_miles <= 1205.00:
                            if receipts_per_mile <= 1.77:
                                total = 1294.13
                            else:
                                total = 1408.36
                        else:
                            if miles_per_day <= 406.00:
                                total = 1495.94
                            else:
                                total = 1526.97
            else:
                if days_x_receipts <= 11625.58:
                    if days_x_miles <= 979.83:
                        if days_x_receipts <= 9327.43:
                            total = 1270.85
                        else:
                            total = 1406.93
                    else:
                        if miles_traveled <= 518.50:
                            if days_x_miles <= 2578.00:
                                total = 1496.66
                            else:
                                total = 1336.63
                        else:
                            if receipts_per_day <= 624.27:
                                total = 1653.03
                            else:
                                total = 1498.03
                else:
                    if trip_duration_days <= 12.50:
                        if receipts_per_mile <= 6.38:
                            total = 1664.33
                        else:
                            if trip_duration_days <= 8.50:
                                total = 1528.26
                            else:
                                total = 1605.61
                    else:
                        total = 1714.87
        else:
            if days_x_miles <= 6939.00:
                if total_receipts_amount <= 1089.04:
                    total = 1476.82
                else:
                    if miles_per_day <= 99.75:
                        if trip_duration_days <= 10.50:
                            if miles_x_receipts <= 1229175.00:
                                total = 1636.17
                            else:
                                total = 1521.96
                        else:
                            if receipts_per_day <= 169.39:
                                total = 1795.96
                            else:
                                total = 1702.51
                    else:
                        if trip_duration_days <= 5.50:
                            if miles_traveled <= 1030.50:
                                total = 1736.47
                            else:
                                total = 1659.12
                        else:
                            if trip_duration_days <= 6.50:
                                total = 1778.50
                            else:
                                total = 1860.13
            else:
                if days_x_miles <= 11863.00:
                    if miles_per_day <= 127.34:
                        if miles_x_receipts <= 877176.88:
                            total = 1742.71
                        else:
                            if receipts_per_day <= 174.05:
                                total = 1906.01
                            else:
                                total = 1800.23
                    else:
                        if days_x_receipts <= 12912.54:
                            total = 2048.61
                        else:
                            total = 1857.20
                else:
                    if total_receipts_amount <= 1787.72:
                        if miles_traveled <= 1017.50:
                            total = 1988.28
                        else:
                            total = 2136.03
                    else:
                        total = 1924.59
    
    return round(total, 2)
'''

# Save optimized version
with open('solution_optimized_final.py', 'w') as f:
    f.write(code)

print("\nOptimized solution saved to solution_optimized_final.py")
print("\nNOTE: The decision tree is already highly optimized.")
print("A score of 0 likely requires:")
print("1. Additional data (dates, departments, employee types)")
print("2. Access to the exact business rules")
print("3. Or discovering a hidden pattern we haven't found yet")