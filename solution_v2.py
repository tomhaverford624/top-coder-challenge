#!/usr/bin/env python3
import json
import sys

def calculate_reimbursement(days, miles, receipts):
    """
    Calculate travel reimbursement.
    
    Based on the example that worked: 80*days + 0.55*miles + 0.85*receipts = 392.50
    But we need to account for the fact that 1-day trips behave very differently.
    """
    
    # Calculate base amounts using the formula that matched the example
    base_amount = 80 * days + 0.55 * miles + 0.85 * receipts
    
    # But we know from the data that 1-day trips average much higher per day
    # So there must be multipliers or adjustments
    
    if days == 1:
        # 1-day trips average $873, but with base formula they'd be much lower
        # Need a significant multiplier
        multiplier = 6.5
    elif days == 2:
        # 2-day trips average $523/day = $1046 total
        multiplier = 5.0
    elif days == 3:
        # 3-day trips average $337/day = $1011 total
        multiplier = 3.5
    elif days == 4:
        # 4-day trips average $304/day = $1216 total
        multiplier = 3.0
    elif days == 5:
        # 5-day trips average $255/day = $1275 total
        multiplier = 2.5
    elif days == 6:
        # 6-day trips average $228/day = $1368 total
        multiplier = 2.2
    elif days == 7:
        # 7-day trips average $217/day = $1519 total
        multiplier = 2.0
    elif days == 8:
        # 8-day trips average $180/day = $1440 total
        multiplier = 1.8
    else:
        # Longer trips
        multiplier = 1.5
    
    total = base_amount * multiplier
    
    # Round to 2 decimal places
    return round(total, 2)

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