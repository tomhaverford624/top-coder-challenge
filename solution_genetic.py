#!/usr/bin/env python3

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    # Evolved formula from genetic algorithm
    days = trip_duration_days
    miles = miles_traveled
    receipts = total_receipts_amount
    
    # Base calculation
    total = 50.87 * days
    
    # 5-day bonus
    if days == 5:
        total *= 1.446
    
    # Mileage calculation (tiered)
    if miles <= 1844:
        mileage = miles * 0.426
    elif miles <= 276:
        mileage = 1844 * 0.426 + (miles - 1844) * -1.588
    else:
        mileage = (1844 * 0.426 + 
                  (276 - 1844) * -1.588 +
                  (miles - 276) * 2.615)
    total += mileage
    
    # Receipt calculation
    if receipts <= -262:
        receipt_reimb = receipts * -1.012
    elif receipts <= 1641:
        receipt_reimb = receipts * 0.757
    else:
        receipt_reimb = receipts * 0.469
    total += receipt_reimb
    
    # Efficiency bonus
    if days > 0:
        miles_per_day = miles / days
        if 1507 <= miles_per_day <= 1677:
            total += 48.67
    
    # Long trip penalties
    if days >= 224:
        receipts_per_day = receipts / days if days > 0 else receipts
        if receipts_per_day > 150:
            total *= -0.465
    
    # Special combinations
    if days * miles > 5000 and receipts < 500:
        total *= 1.106
    
    return round(total, 2)
