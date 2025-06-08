#!/usr/bin/env python3
import json
from solution_v3 import calculate_reimbursement

# Load public cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("Debugging specific error patterns...")
print("=" * 80)

# Test the first few cases to see patterns
print("First 10 cases:")
for i, case in enumerate(cases[:10]):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    predicted = calculate_reimbursement(days, miles, receipts)
    error = abs(predicted - expected)
    
    print(f"\nCase {i+1}: D={days}, M={miles}, R=${receipts:.2f}")
    print(f"  Expected: ${expected:.2f}")
    print(f"  Predicted: ${predicted:.2f}")
    print(f"  Error: ${error:.2f}")
    
    # Try to understand what's happening
    if days == 1:
        if miles < 200 and receipts < 200:
            print(f"  Formula used: 100 + 0.4*{miles} + 0.6*{receipts:.2f}")
            print(f"  Calculation: 100 + {0.4*miles:.2f} + {0.6*receipts:.2f} = {100 + 0.4*miles + 0.6*receipts:.2f}")
        else:
            print(f"  Formula used: ({miles} + {receipts:.2f}) * 0.7")
            print(f"  Calculation: {miles + receipts:.2f} * 0.7 = {(miles + receipts) * 0.7:.2f}")
    elif days == 3:
        print(f"  Formula used: 80*{days} + 0.55*{miles} + 0.85*{receipts:.2f}")
        print(f"  Calculation: {80*days} + {0.55*miles:.2f} + {0.85*receipts:.2f} = {80*days + 0.55*miles + 0.85*receipts:.2f}")

# Look for patterns in large errors
print("\n" + "=" * 80)
print("Analyzing large errors...")

large_errors = []
for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    predicted = calculate_reimbursement(days, miles, receipts)
    error = abs(predicted - expected)
    
    if error > 500:  # Large error
        large_errors.append({
            'days': days,
            'miles': miles,
            'receipts': receipts,
            'expected': expected,
            'predicted': predicted,
            'error': error
        })

large_errors.sort(key=lambda x: x['error'], reverse=True)
print(f"\nFound {len(large_errors)} cases with error > $500")
print("Top 10 largest errors:")
for err in large_errors[:10]:
    print(f"  D={err['days']}, M={err['miles']}, R=${err['receipts']:.2f}: "
          f"Expected ${err['expected']:.2f}, Got ${err['predicted']:.2f}, Error=${err['error']:.2f}")

# Check if there's a pattern in receipts
print("\n" + "=" * 80)
print("Checking receipt patterns...")

# Group errors by receipt ranges
receipt_ranges = [(0, 50), (50, 100), (100, 500), (500, 1000), (1000, 3000)]
range_errors = {r: [] for r in receipt_ranges}

for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    predicted = calculate_reimbursement(days, miles, receipts)
    error = abs(predicted - expected)
    
    for r in receipt_ranges:
        if r[0] <= receipts < r[1]:
            range_errors[r].append(error)
            break

print("\nAverage error by receipt range:")
for r, errors in range_errors.items():
    if errors:
        avg_error = sum(errors) / len(errors)
        print(f"  ${r[0]}-${r[1]}: avg error = ${avg_error:.2f} (n={len(errors)})")