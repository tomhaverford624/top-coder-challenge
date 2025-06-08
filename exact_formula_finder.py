#!/usr/bin/env python3
"""
Exact Formula Finder - Find the EXACT formula for score 0
"""

import json
import math
from itertools import product

# Load the data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

print("Searching for EXACT formulas...")
print("=" * 60)

# Test hypothesis: Different formulas for different receipt endings
def test_receipt_ending_formulas():
    print("\nTesting receipt-ending based formulas...")
    
    # Group by receipt ending
    endings = {}
    for case in data:
        cents = int(case['input']['total_receipts_amount'] * 100) % 100
        if cents not in endings:
            endings[cents] = []
        endings[cents].append(case)
    
    # For each ending, try to find exact formula
    for cent_ending, cases in sorted(endings.items()):
        if len(cases) < 5:  # Skip rare endings
            continue
            
        print(f"\n.{cent_ending:02d} endings ({len(cases)} cases):")
        
        # Try different formula structures
        best_formula = None
        best_error = float('inf')
        
        # Test ranges of coefficients
        for base in range(80, 120, 5):
            for mile_coef in [0.40, 0.45, 0.50, 0.52, 0.55, 0.58, 0.60, 0.65]:
                for receipt_coef in [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]:
                    total_error = 0
                    
                    for case in cases:
                        days = case['input']['trip_duration_days']
                        miles = case['input']['miles_traveled']
                        receipts = case['input']['total_receipts_amount']
                        expected = case['expected_output']
                        
                        # Try with different multipliers
                        pred = base * days + mile_coef * miles + receipt_coef * receipts
                        
                        # Special multipliers for .49 and .99
                        if cent_ending == 49:
                            pred *= 1.1
                        elif cent_ending == 99:
                            pred *= 1.05
                        
                        error = abs(pred - expected)
                        total_error += error
                    
                    avg_error = total_error / len(cases)
                    if avg_error < best_error:
                        best_error = avg_error
                        best_formula = (base, mile_coef, receipt_coef)
        
        if best_formula:
            print(f"  Best: {best_formula[0]}*days + {best_formula[1]}*miles + {best_formula[2]}*receipts")
            print(f"  Avg error: ${best_error:.2f}")

# Test hypothesis: Lookup tables for specific combinations
def find_lookup_patterns():
    print("\n\nSearching for lookup table patterns...")
    
    # Round inputs to find patterns
    patterns = {}
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        # Try different rounding strategies
        # Round miles to nearest 10
        miles_rounded = round(miles / 10) * 10
        # Round receipts to nearest 50
        receipts_rounded = round(receipts / 50) * 50
        
        key = (days, miles_rounded, receipts_rounded)
        if key not in patterns:
            patterns[key] = []
        patterns[key].append(expected)
    
    # Find consistent patterns
    consistent = 0
    for key, outputs in patterns.items():
        if len(outputs) > 1:
            # Check if outputs are similar
            avg = sum(outputs) / len(outputs)
            variance = sum((x - avg) ** 2 for x in outputs) / len(outputs)
            if variance < 100:  # Low variance
                consistent += 1
    
    print(f"Found {consistent} consistent patterns out of {len(patterns)} groups")

# Test hypothesis: Complex piecewise functions
def test_piecewise_functions():
    print("\n\nTesting piecewise functions...")
    
    # Group by characteristics
    groups = {
        'short_low': [],     # <=3 days, <$500 receipts
        'short_high': [],    # <=3 days, >=$500 receipts
        'medium_low': [],    # 4-7 days, <$800 receipts
        'medium_high': [],   # 4-7 days, >=$800 receipts
        'long_low': [],      # 8+ days, <$1000 receipts
        'long_high': []      # 8+ days, >=$1000 receipts
    }
    
    for case in data:
        days = case['input']['trip_duration_days']
        receipts = case['input']['total_receipts_amount']
        
        if days <= 3:
            if receipts < 500:
                groups['short_low'].append(case)
            else:
                groups['short_high'].append(case)
        elif days <= 7:
            if receipts < 800:
                groups['medium_low'].append(case)
            else:
                groups['medium_high'].append(case)
        else:
            if receipts < 1000:
                groups['long_low'].append(case)
            else:
                groups['long_high'].append(case)
    
    # Find formula for each group
    for group_name, cases in groups.items():
        if not cases:
            continue
            
        print(f"\n{group_name}: {len(cases)} cases")
        
        # Find best formula for this group
        best_error = float('inf')
        best_params = None
        
        for base in range(70, 130, 10):
            for mile_rate in [0.3, 0.4, 0.5, 0.6, 0.7]:
                for receipt_rate in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
                    total_error = 0
                    
                    for case in cases:
                        days = case['input']['trip_duration_days']
                        miles = case['input']['miles_traveled']
                        receipts = case['input']['total_receipts_amount']
                        expected = case['expected_output']
                        
                        pred = base * days + mile_rate * miles + receipt_rate * receipts
                        total_error += abs(pred - expected)
                    
                    avg_error = total_error / len(cases)
                    if avg_error < best_error:
                        best_error = avg_error
                        best_params = (base, mile_rate, receipt_rate)
        
        print(f"  Best: {best_params[0]}*d + {best_params[1]}*m + {best_params[2]}*r")
        print(f"  Avg error: ${best_error:.2f}")

# Test hypothesis: Exact matches in simple cases
def find_exact_patterns():
    print("\n\nLooking for exact pattern matches...")
    
    exact_matches = 0
    near_matches = 0
    
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        # Test various exact formulas
        formulas = [
            100 * days + 0.58 * miles + 0.80 * receipts,
            95 * days + 0.55 * miles + 0.85 * receipts,
            105 * days + 0.60 * miles + 0.75 * receipts,
            98 * days + 0.56 * miles + 0.82 * receipts,
            days * 100 + miles * 0.575 + receipts * 0.8,
            # Tiered mileage
            days * 100 + min(miles, 100) * 0.58 + max(0, miles - 100) * 0.50 + receipts * 0.80,
            # With 5-day bonus
            (110 if days == 5 else 100) * days + 0.58 * miles + 0.80 * receipts,
        ]
        
        for formula in formulas:
            if abs(formula - expected) < 0.01:
                exact_matches += 1
                break
            elif abs(formula - expected) < 1.00:
                near_matches += 1
    
    print(f"Exact matches: {exact_matches}")
    print(f"Near matches (within $1): {near_matches}")

# Test employee-mentioned patterns
def test_employee_insights():
    print("\n\nTesting specific employee insights...")
    
    # Lisa mentioned $847 as a "lucky number"
    lucky_outputs = [case for case in data if abs(case['expected_output'] - 847.00) < 1]
    print(f"\nOutputs near $847: {len(lucky_outputs)}")
    
    # Kevin's Tuesday effect - but we need submission date
    # Marcus's quarterly patterns - need dates
    
    # Test for "remembers history" effect
    sorted_data = sorted(data, key=lambda x: (
        x['input']['trip_duration_days'],
        x['input']['miles_traveled'],
        x['input']['total_receipts_amount']
    ))
    
    # Look for sequential effects
    for i in range(1, len(sorted_data)):
        prev = sorted_data[i-1]
        curr = sorted_data[i]
        
        # Similar inputs?
        if (abs(prev['input']['trip_duration_days'] - curr['input']['trip_duration_days']) <= 1 and
            abs(prev['input']['miles_traveled'] - curr['input']['miles_traveled']) <= 50 and
            abs(prev['input']['total_receipts_amount'] - curr['input']['total_receipts_amount']) <= 100):
            
            # Check if outputs show a pattern
            diff = curr['expected_output'] - prev['expected_output']
            if abs(diff) < 10:
                print(f"\nSimilar inputs with small output difference: ${diff:.2f}")

# Run all tests
test_receipt_ending_formulas()
find_lookup_patterns()
test_piecewise_functions()
find_exact_patterns()
test_employee_insights()

print("\n" + "="*60)
print("RECOMMENDATION: Focus on receipt endings and piecewise functions!")