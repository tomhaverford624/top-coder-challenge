#!/usr/bin/env python3

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    # Evolved formula from genetic algorithm
    days = trip_duration_days
    miles = miles_traveled
    receipts = total_receipts_amount
    
    # Base calculation
    total = 49.59 * days
    
    # 5-day bonus
    if days == 5:
        total *= 1.287
    
    # Mileage calculation (tiered)
    if miles <= 2416:
        mileage = miles * 0.420
    elif miles <= 2248:
        mileage = 2416 * 0.420 + (miles - 2416) * -7.936
    else:
        mileage = (2416 * 0.420 + 
                  (2248 - 2416) * -7.936 +
                  (miles - 2248) * 1.034)
    total += mileage
    
    # Receipt calculation
    if receipts <= 1627:
        receipt_reimb = receipts * 0.763
    elif receipts <= 1932:
        receipt_reimb = receipts * 0.524
    else:
        receipt_reimb = receipts * 0.466
    total += receipt_reimb
    
    # Efficiency bonus
    if days > 0:
        miles_per_day = miles / days
        if 1965 <= miles_per_day <= 316:
            total += 58.11
    
    # Long trip penalties
    if days >= 134:
        receipts_per_day = receipts / days if days > 0 else receipts
        if receipts_per_day > 150:
            total *= 23.463
    
    # Special combinations
    if days * miles > 5000 and receipts < 500:
        total *= 1.040
    
    return round(total, 2)
