#!/usr/bin/env python3
"""
Lookup Table Analysis - Legacy systems often used lookup tables!
"""

import json
import math
from collections import defaultdict

# Load the data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

print("Searching for Lookup Table Patterns...")
print("=" * 60)

# Group by exact input combinations
exact_matches = defaultdict(list)
for case in data:
    key = (
        case['input']['trip_duration_days'],
        case['input']['miles_traveled'],
        case['input']['total_receipts_amount']
    )
    exact_matches[key].append(case['expected_output'])

# Find any exact duplicates
print(f"Total unique input combinations: {len(exact_matches)}")
duplicates = {k: v for k, v in exact_matches.items() if len(v) > 1}
print(f"Duplicate inputs with different outputs: {len(duplicates)}")

# Look for patterns in receipt endings
receipt_patterns = defaultdict(list)
for case in data:
    receipts = case['input']['total_receipts_amount']
    cents = int(receipts * 100) % 100
    receipt_patterns[cents].append(case)

print("\nReceipt Ending Patterns:")
special_endings = [49, 99, 33, 0, 50]
for ending in special_endings:
    cases = receipt_patterns[ending]
    if cases:
        print(f"\n.{ending:02d} endings: {len(cases)} cases")
        # Analyze if these follow specific formulas
        errors = []
        for c in cases:
            days = c['input']['trip_duration_days']
            miles = c['input']['miles_traveled']
            receipts = c['input']['total_receipts_amount']
            expected = c['expected_output']
            
            # Test various formulas
            formula1 = 100 * days + 0.58 * miles + 0.8 * receipts
            formula2 = 95 * days + 0.5 * miles + 0.85 * receipts
            formula3 = 105 * days + 0.55 * miles + 0.75 * receipts
            
            errors.append(min(
                abs(formula1 - expected),
                abs(formula2 - expected),
                abs(formula3 - expected)
            ))
        
        avg_error = sum(errors) / len(errors) if errors else 0
        print(f"  Best formula avg error: ${avg_error:.2f}")

# Look for "magic numbers" in outputs
output_counts = defaultdict(int)
for case in data:
    output_counts[case['expected_output']] += 1

print("\nMost common output values:")
common_outputs = sorted(output_counts.items(), key=lambda x: x[1], reverse=True)[:20]
for output, count in common_outputs:
    if count > 1:
        print(f"  ${output:.2f}: {count} times")

# Analyze specific value patterns
print("\nSearching for calculation patterns...")

# Check if outputs are multiples of specific values
base_values = [10, 25, 50, 100]
for base in base_values:
    multiples = 0
    for case in data:
        if abs(case['expected_output'] % base) < 0.01:
            multiples += 1
    print(f"  Outputs that are multiples of ${base}: {multiples} ({multiples/len(data)*100:.1f}%)")

# Look for tiered calculations
print("\nAnalyzing tiered structures...")

# Group by trip duration
duration_groups = defaultdict(list)
for case in data:
    duration_groups[case['input']['trip_duration_days']].append(case)

for days in sorted(duration_groups.keys())[:10]:
    cases = duration_groups[days]
    outputs = [c['expected_output'] for c in cases]
    if len(outputs) > 5:
        min_out = min(outputs)
        max_out = max(outputs)
        avg_out = sum(outputs) / len(outputs)
        print(f"\n{days}-day trips: {len(cases)} cases")
        print(f"  Output range: ${min_out:.2f} - ${max_out:.2f}")
        print(f"  Average: ${avg_out:.2f}")
        
        # Check if there's a base amount
        base_estimate = min_out / days if days > 0 else 0
        print(f"  Estimated base per day: ${base_estimate:.2f}")

# Kevin mentioned specific combinations
print("\nTesting Kevin's insights...")

# 5-day trips with 180+ miles/day and <$100/day receipts
kevin_cases = []
for case in data:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    
    if days == 5:
        miles_per_day = miles / days
        receipts_per_day = receipts / days
        
        if miles_per_day >= 180 and receipts_per_day < 100:
            kevin_cases.append(case)

if kevin_cases:
    print(f"\nKevin's 'sweet spot' cases: {len(kevin_cases)}")
    for i, case in enumerate(kevin_cases[:5]):
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        print(f"  {i+1}. {days}d, {miles}mi, ${receipts:.2f} → ${expected:.2f}")

# Department simulation - different base rates
print("\nTesting department-based calculations...")

# Try different base rates
base_rates = [90, 95, 100, 105, 110]
mileage_rates = [0.50, 0.55, 0.58, 0.60, 0.65]
receipt_rates = [0.70, 0.75, 0.80, 0.85, 0.90]

best_combo = None
best_error = float('inf')

for base in base_rates:
    for mile_rate in mileage_rates:
        for receipt_rate in receipt_rates:
            total_error = 0
            for case in data[:100]:  # Test on subset first
                days = case['input']['trip_duration_days']
                miles = case['input']['miles_traveled']
                receipts = case['input']['total_receipts_amount']
                expected = case['expected_output']
                
                predicted = base * days + mile_rate * miles + receipt_rate * receipts
                total_error += abs(predicted - expected)
            
            if total_error < best_error:
                best_error = total_error
                best_combo = (base, mile_rate, receipt_rate)

print(f"\nBest simple formula combination:")
print(f"  Base: ${best_combo[0]}/day")
print(f"  Mileage: ${best_combo[1]}/mile")
print(f"  Receipts: {best_combo[2]*100:.0f}% reimbursement")
print(f"  Error on first 100 cases: ${best_error:.2f}")