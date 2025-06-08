#!/usr/bin/env python3
"""
Integer-based Formula Search
Legacy systems often used integer arithmetic to avoid floating point issues
"""

import json
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

# Load the data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

print("Searching for INTEGER-BASED formulas (legacy system approach)...")
print("=" * 60)

def test_integer_formulas():
    """Test formulas using integer arithmetic with cents"""
    print("\nTesting integer-based calculations...")
    
    exact_matches = 0
    
    for case in data[:100]:  # Test on subset first
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        # Convert to cents to avoid floating point
        receipts_cents = int(receipts * 100)
        expected_cents = int(expected * 100)
        
        # Test various integer-based formulas
        # Base per diem in cents
        base_per_diem_cents = 10000  # $100.00
        
        # Mileage in cents per mile
        mileage_cents_per_mile = 58  # $0.58
        
        # Receipt reimbursement percentage
        receipt_percentage = 80  # 80%
        
        # Calculate in cents
        per_diem_total = base_per_diem_cents * days
        mileage_total = int(mileage_cents_per_mile * miles)
        receipt_reimbursement = (receipts_cents * receipt_percentage) // 100
        
        total_cents = per_diem_total + mileage_total + receipt_reimbursement
        
        # Special rules
        if days == 5:
            total_cents = (total_cents * 110) // 100  # 10% bonus
        
        # Check if exact match
        if total_cents == expected_cents:
            exact_matches += 1
            print(f"EXACT MATCH: {days}d, {miles}mi, ${receipts:.2f} → ${expected:.2f}")
    
    print(f"\nExact matches: {exact_matches}/100")

def test_decimal_calculations():
    """Test using Decimal for exact decimal arithmetic"""
    print("\n\nTesting Decimal-based calculations...")
    
    # Common rates in legacy systems
    rates_to_test = [
        (Decimal('100'), Decimal('0.58'), Decimal('0.80')),
        (Decimal('95'), Decimal('0.55'), Decimal('0.85')),
        (Decimal('105'), Decimal('0.60'), Decimal('0.75')),
        (Decimal('98'), Decimal('0.575'), Decimal('0.82')),
    ]
    
    best_rate = None
    best_matches = 0
    
    for base, mile_rate, receipt_rate in rates_to_test:
        exact_matches = 0
        
        for case in data:
            days = Decimal(str(case['input']['trip_duration_days']))
            miles = Decimal(str(case['input']['miles_traveled']))
            receipts = Decimal(str(case['input']['total_receipts_amount']))
            expected = Decimal(str(case['expected_output']))
            
            # Calculate
            total = base * days + mile_rate * miles + receipt_rate * receipts
            
            # Round to 2 decimal places (cents)
            total = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            if total == expected:
                exact_matches += 1
        
        if exact_matches > best_matches:
            best_matches = exact_matches
            best_rate = (base, mile_rate, receipt_rate)
        
        print(f"Rate {base}, {mile_rate}, {receipt_rate}: {exact_matches} exact matches")
    
    print(f"\nBest rate: {best_rate} with {best_matches} matches")

def analyze_rounding_patterns():
    """Check if specific rounding rules are applied"""
    print("\n\nAnalyzing rounding patterns...")
    
    rounding_patterns = {
        'up': 0,
        'down': 0,
        'nearest': 0,
        'bankers': 0
    }
    
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        # Calculate with more precision
        base_calc = 100.0 * days + 0.58 * miles + 0.80 * receipts
        
        # Test different rounding methods
        rounded_up = math.ceil(base_calc * 100) / 100
        rounded_down = math.floor(base_calc * 100) / 100
        rounded_nearest = round(base_calc, 2)
        
        # Check which rounding matches
        if abs(rounded_up - expected) < 0.01:
            rounding_patterns['up'] += 1
        elif abs(rounded_down - expected) < 0.01:
            rounding_patterns['down'] += 1
        elif abs(rounded_nearest - expected) < 0.01:
            rounding_patterns['nearest'] += 1
    
    print("Rounding pattern matches:")
    for pattern, count in rounding_patterns.items():
        print(f"  {pattern}: {count} matches ({count/len(data)*100:.1f}%)")

def find_magic_formulas():
    """Look for 'magic' formulas that work for specific cases"""
    print("\n\nSearching for magic formulas...")
    
    # Group by output ranges
    output_ranges = {
        'small': [],      # < $500
        'medium': [],     # $500-1000
        'large': [],      # $1000-1500
        'xlarge': []      # > $1500
    }
    
    for case in data:
        output = case['expected_output']
        if output < 500:
            output_ranges['small'].append(case)
        elif output < 1000:
            output_ranges['medium'].append(case)
        elif output < 1500:
            output_ranges['large'].append(case)
        else:
            output_ranges['xlarge'].append(case)
    
    # For each range, find the best formula
    for range_name, cases in output_ranges.items():
        print(f"\n{range_name} outputs ({len(cases)} cases):")
        
        # Test simple formulas
        best_formula = None
        min_total_error = float('inf')
        
        # Test integer coefficients
        for base in range(80, 120, 5):
            for mile_cents in range(45, 65, 2):
                for receipt_pct in range(70, 95, 5):
                    total_error = 0
                    exact_matches = 0
                    
                    for case in cases:
                        days = case['input']['trip_duration_days']
                        miles = case['input']['miles_traveled']
                        receipts = case['input']['total_receipts_amount']
                        expected = case['expected_output']
                        
                        # Calculate
                        pred = base * days + (mile_cents / 100) * miles + (receipt_pct / 100) * receipts
                        
                        error = abs(pred - expected)
                        if error < 0.01:
                            exact_matches += 1
                        total_error += error
                    
                    if total_error < min_total_error:
                        min_total_error = total_error
                        best_formula = (base, mile_cents/100, receipt_pct/100, exact_matches)
        
        if best_formula:
            print(f"  Best: ${best_formula[0]}/day + ${best_formula[1]:.2f}/mile + {best_formula[2]*100:.0f}% receipts")
            print(f"  Exact matches: {best_formula[3]}/{len(cases)}")

# Run all tests
test_integer_formulas()
test_decimal_calculations()
analyze_rounding_patterns()
find_magic_formulas()

print("\n" + "="*60)
print("KEY INSIGHT: Legacy systems often used integer arithmetic!")
print("Try formulas with:")
print("- Integer cents for all calculations")
print("- Specific rounding rules (ROUND_HALF_UP)")
print("- Different formulas for different ranges")