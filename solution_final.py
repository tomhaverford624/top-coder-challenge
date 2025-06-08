#!/usr/bin/env python3
import json
import sys

def calculate_reimbursement(days, miles, receipts):
    """
    Calculate travel reimbursement with caps and penalties for high receipts.
    """
    
    # Apply receipt caps/adjustments first
    # Based on the data, very high receipts get heavily penalized
    if receipts > 1000:
        # For very high receipts, only a small portion is reimbursed
        effective_receipts = 100 + (receipts - 1000) * 0.05
    elif receipts > 500:
        # Medium-high receipts get partial reimbursement
        effective_receipts = 50 + (receipts - 500) * 0.1 + 500 * 0.2
    elif receipts > 200:
        # Moderate receipts
        effective_receipts = receipts * 0.4
    else:
        # Low receipts get better treatment
        effective_receipts = receipts * 0.85
    
    if days == 1:
        # For 1-day trips
        if miles < 200 and receipts < 200:
            # Low miles/receipts formula
            result = 100 + 0.4 * miles + 0.6 * receipts
        else:
            # Higher inputs - but use effective receipts
            base = 100
            mileage = miles * 0.5
            result = base + mileage + effective_receipts
        
        # Apply cap for 1-day trips
        result = min(result, 1475)
        
    elif days == 2:
        # 2-day trips
        base = 160 * days
        mileage = miles * 0.45
        result = base + mileage + effective_receipts
        
    elif days == 3:
        # 3-day trips - we know the example works
        # But need to handle high receipts differently
        base = 80 * days
        mileage = miles * 0.55
        
        # Use original receipts for low amounts, effective for high
        if receipts < 100:
            receipt_component = receipts * 0.85
        else:
            receipt_component = effective_receipts
        
        result = base + mileage + receipt_component
        
    elif days == 4:
        # 4-day trips
        base = 75 * days
        mileage = miles * 0.48
        result = base + mileage + effective_receipts
        
    elif days == 5:
        # 5-day trips with bonus
        base = 70 * days + 50  # $50 bonus
        mileage = miles * 0.45
        result = base + mileage + effective_receipts
        
    elif days == 6:
        # 6-day trips
        base = 65 * days
        mileage = miles * 0.42
        result = base + mileage + effective_receipts
        
    elif days == 7:
        # 7-day trips
        base = 60 * days
        mileage = miles * 0.40
        result = base + mileage + effective_receipts
        
    elif days == 8:
        # 8-day trips
        base = 55 * days
        mileage = miles * 0.38
        result = base + mileage + effective_receipts
        
    else:
        # Longer trips
        base = 50 * days
        mileage = miles * 0.35
        result = base + mileage + effective_receipts
    
    # Apply overall caps based on trip length
    max_per_day = 500 - (days * 20)  # Decreasing cap per day
    max_total = days * max_per_day
    result = min(result, max_total)
    
    # Round to 2 decimal places
    return round(result, 2)

def main():
    # Read input
    if len(sys.argv) > 1:
        # Command line arguments
        days = int(sys.argv[1])
        miles = int(sys.argv[2])
        receipts = float(sys.argv[3])
    else:
        # Read from stdin (JSON format expected)
        data = json.loads(sys.stdin.read())
        days = data['trip_duration_days']
        miles = data['miles_traveled']
        receipts = data['total_receipts_amount']
    
    # Calculate reimbursement
    result = calculate_reimbursement(days, miles, receipts)
    
    # Output result
    print(result)

if __name__ == "__main__":
    main()