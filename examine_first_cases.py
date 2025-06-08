#!/usr/bin/env python3
import json

# Load public cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("Examining first 10 cases in detail...")
print("=" * 80)

for i, case in enumerate(cases[:10]):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    print(f"\nCase {i+1}:")
    print(f"  Days: {days}")
    print(f"  Miles: {miles}")
    print(f"  Receipts: ${receipts:.2f}")
    print(f"  Expected: ${expected:.2f}")
    
    # Try different decompositions
    print(f"  Per day: ${expected/days:.2f}")
    print(f"  Per mile: ${expected/miles:.4f}")
    
    # Test various formulas
    formulas = [
        ("100*d + 0.6*m + r", 100*days + 0.6*miles + receipts),
        ("80*d + 0.55*m + 0.85*r", 80*days + 0.55*miles + 0.85*receipts),
        ("d^2 * 100 + m*0.6 + r", days*days*100 + miles*0.6 + receipts),
        ("d * 100 + m * (1/d) + r", days * 100 + miles * (1/days) + receipts),
        ("(d+m+r) * factor", None),  # Will calculate factor
    ]
    
    print("  Formula tests:")
    for formula_name, result in formulas:
        if result is None:
            # Calculate factor
            total_input = days + miles + receipts
            factor = expected / total_input if total_input > 0 else 0
            result = total_input * factor
            formula_name = f"(d+m+r) * {factor:.4f}"
        
        error = abs(result - expected)
        print(f"    {formula_name} = ${result:.2f} (error: ${error:.2f})")

# Look for patterns in the "factor" approach
print("\n" + "=" * 80)
print("Analyzing multiplication factors...")

factors = []
for case in cases[:50]:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    total_input = days + miles + receipts
    factor = expected / total_input if total_input > 0 else 0
    
    factors.append({
        'days': days,
        'miles': miles,
        'receipts': receipts,
        'total': total_input,
        'expected': expected,
        'factor': factor
    })

# Group by days
days_factors = {}
for f in factors:
    d = f['days']
    if d not in days_factors:
        days_factors[d] = []
    days_factors[d].append(f['factor'])

print("\nAverage factors by trip days:")
for days in sorted(days_factors.keys()):
    avg_factor = sum(days_factors[days]) / len(days_factors[days])
    print(f"{days} days: avg factor = {avg_factor:.4f} (n={len(days_factors[days])})")

# Maybe it's about the ratio of components?
print("\n" + "=" * 80)
print("Analyzing component ratios...")

for i, case in enumerate(cases[:5]):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    print(f"\nCase {i+1}: D={days}, M={miles}, R=${receipts:.2f}, Expected=${expected:.2f}")
    
    # What if the output is based on ratios?
    miles_per_day = miles / days
    receipts_per_day = receipts / days
    receipts_per_mile = receipts / miles if miles > 0 else 0
    
    print(f"  Miles/day: {miles_per_day:.2f}")
    print(f"  Receipts/day: ${receipts_per_day:.2f}")
    print(f"  Receipts/mile: ${receipts_per_mile:.4f}")
    
    # Maybe there's a complex interaction
    # Let's see if we can find a pattern
    remaining = expected
    print(f"  If we subtract receipts: ${remaining - receipts:.2f}")
    remaining = remaining - receipts
    print(f"  If we then subtract miles*0.6: ${remaining - miles*0.6:.2f}")
    remaining = remaining - miles*0.6
    print(f"  Remaining per day: ${remaining/days:.2f}")