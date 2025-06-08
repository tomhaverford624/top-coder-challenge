#!/usr/bin/env python3
import json
import sys

def calculate_reimbursement(days, miles, receipts):
    """
    Calculate travel reimbursement with caps and different formulas by trip length.
    """
    
    if days == 1:
        # For 1-day trips, there seems to be a cap around $1475
        # And the formula varies based on the inputs
        
        # For low miles/receipts trips
        if miles < 200 and receipts < 200:
            # Use a formula that works for low reimbursements
            result = 100 + 0.4 * miles + 0.6 * receipts
        else:
            # For higher inputs, use a percentage-based approach
            result = (miles + receipts) * 0.7
        
        # Apply cap
        result = min(result, 1475)
        
    elif days == 2:
        # 2-day trips average $523/day = $1046 total
        base = 160 * days  # $160 per day base
        mileage = miles * 0.55
        receipt_amount = receipts * 0.85
        result = base + mileage + receipt_amount
        
    elif days == 3:
        # 3-day trips average $337/day = $1011 total
        # The example: 3 days, 200 miles, $50 receipts = $392
        # Using: 80*days + 0.55*miles + 0.85*receipts gives close to 392
        result = 80 * days + 0.55 * miles + 0.85 * receipts
        
    elif days == 4:
        # 4-day trips
        result = 75 * days + 0.52 * miles + 0.88 * receipts
        
    elif days == 5:
        # 5-day trips with bonus
        result = 70 * days + 0.5 * miles + 0.9 * receipts + 50  # $50 bonus for 5 days
        
    elif days == 6:
        # 6-day trips
        result = 65 * days + 0.48 * miles + 0.92 * receipts
        
    elif days == 7:
        # 7-day trips
        result = 60 * days + 0.46 * miles + 0.94 * receipts
        
    elif days == 8:
        # 8-day trips
        result = 55 * days + 0.44 * miles + 0.95 * receipts
        
    else:
        # Longer trips
        result = 50 * days + 0.42 * miles + 0.96 * receipts
    
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