#!/usr/bin/env python3
import json

# Load public cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

def optimize_step_function():
    """Find optimal parameters for step function approach"""
    print("Optimizing Step Function Parameters")
    print("="*80)
    
    # Split cases by trip length
    short_trips = []  # 1-3 days
    long_trips = []   # 4+ days
    
    for case in cases[:500]:  # Use more cases for better optimization
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        if days <= 3:
            short_trips.append((days, miles, receipts, expected))
        else:
            long_trips.append((days, miles, receipts, expected))
    
    print(f"\nData split: {len(short_trips)} short trips, {len(long_trips)} long trips")
    
    # Optimize parameters for short trips
    print("\nOptimizing SHORT trips (1-3 days):")
    best_short_error = float('inf')
    best_short_params = None
    
    for base in range(70, 100, 2):
        for receipt_mult in [0.8, 0.9, 1.0, 1.1, 1.2]:
            for mile_rate in [0.60, 0.65, 0.67, 0.70, 0.75]:
                errors = []
                for days, miles, receipts, expected in short_trips:
                    pred = base * days + receipts * receipt_mult + miles * mile_rate
                    error = abs(pred - expected) / expected * 100
                    errors.append(error)
                
                avg_error = sum(errors) / len(errors)
                if avg_error < best_short_error:
                    best_short_error = avg_error
                    best_short_params = (base, receipt_mult, mile_rate)
    
    print(f"  Best parameters: base=${best_short_params[0]}/day, "
          f"receipts*{best_short_params[1]}, miles*${best_short_params[2]}")
    print(f"  Average error: {best_short_error:.2f}%")
    
    # Optimize parameters for long trips
    print("\nOptimizing LONG trips (4+ days):")
    best_long_error = float('inf')
    best_long_params = None
    
    for base in range(20, 50, 2):
        for receipt_mult in [0.8, 0.9, 1.0, 1.1, 1.2]:
            for mile_rate in [0.60, 0.65, 0.67, 0.70, 0.75]:
                errors = []
                for days, miles, receipts, expected in long_trips:
                    pred = base * days + receipts * receipt_mult + miles * mile_rate
                    error = abs(pred - expected) / expected * 100
                    errors.append(error)
                
                avg_error = sum(errors) / len(errors)
                if avg_error < best_long_error:
                    best_long_error = avg_error
                    best_long_params = (base, receipt_mult, mile_rate)
    
    print(f"  Best parameters: base=${best_long_params[0]}/day, "
          f"receipts*{best_long_params[1]}, miles*${best_long_params[2]}")
    print(f"  Average error: {best_long_error:.2f}%")
    
    # Test combined approach
    print("\n\nTesting Combined Approach on All Cases:")
    all_errors = []
    
    for case in cases[:100]:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        if days <= 3:
            base, receipt_mult, mile_rate = best_short_params
        else:
            base, receipt_mult, mile_rate = best_long_params
        
        pred = base * days + receipts * receipt_mult + miles * mile_rate
        error = abs(pred - expected) / expected * 100
        all_errors.append(error)
    
    print(f"  Average error on first 100 cases: {sum(all_errors)/len(all_errors):.2f}%")
    print(f"  Max error: {max(all_errors):.2f}%")
    print(f"  Cases with <5% error: {sum(1 for e in all_errors if e < 5)}/{len(all_errors)}")
    print(f"  Cases with <10% error: {sum(1 for e in all_errors if e < 10)}/{len(all_errors)}")
    
    # Print the final formula
    print("\n\nFINAL FORMULA:")
    print("="*50)
    print("if trip_duration_days <= 3:")
    print(f"    reimbursement = {best_short_params[0]} * trip_duration_days + "
          f"{best_short_params[1]} * total_receipts_amount + "
          f"{best_short_params[2]} * miles_traveled")
    print("else:")
    print(f"    reimbursement = {best_long_params[0]} * trip_duration_days + "
          f"{best_long_params[1]} * total_receipts_amount + "
          f"{best_long_params[2]} * miles_traveled")
    
    return best_short_params, best_long_params

def test_edge_cases(short_params, long_params):
    """Test on specific edge cases"""
    print("\n\nTesting Edge Cases:")
    print("="*50)
    
    # Test on the transition point (3 vs 4 days)
    print("\nTransition from 3 to 4 days:")
    for case in cases[:50]:
        days = case['input']['trip_duration_days']
        if days == 3 or days == 4:
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            expected = case['expected_output']
            
            if days == 3:
                base, receipt_mult, mile_rate = short_params
            else:
                base, receipt_mult, mile_rate = long_params
            
            pred = base * days + receipts * receipt_mult + miles * mile_rate
            error = abs(pred - expected) / expected * 100
            
            print(f"\n{days} days, {miles} miles, ${receipts:.2f} receipts:")
            print(f"  Expected: ${expected:.2f}")
            print(f"  Predicted: ${pred:.2f}")
            print(f"  Error: {error:.1f}%")

if __name__ == "__main__":
    params = optimize_step_function()
    test_edge_cases(*params)