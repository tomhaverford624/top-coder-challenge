#!/usr/bin/env python3

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    
    # Engineer features
    days = trip_duration_days
    miles = miles_traveled
    receipts = total_receipts_amount
    
    # Feature engineering
    miles_per_day = miles / days if days > 0 else 0
    receipts_per_day = receipts / days if days > 0 else 0
    receipts_per_mile = receipts / miles if miles > 0 else 0
    days_x_miles = days * miles
    days_x_receipts = days * receipts
    miles_x_receipts = miles * receipts
    
    # Simplified neural network approximation
    # Using piecewise linear approximations of the trained network
    
    # Layer 1: Feature combinations
    if days <= 3:
        if receipts_per_day <= 50:
            base = 95 * days + 0.58 * miles
        else:
            base = 100 * days + 0.55 * miles + 0.7 * receipts
    elif days <= 6:
        if miles_per_day >= 180 and miles_per_day <= 220:
            base = 110 * days + 0.52 * miles + 0.75 * receipts + 50  # Efficiency bonus
        else:
            base = 105 * days + 0.5 * miles + 0.72 * receipts
    else:
        if receipts_per_day > 150:
            base = 90 * days + 0.45 * miles + 0.5 * receipts  # Penalty
        else:
            base = 100 * days + 0.48 * miles + 0.65 * receipts
    
    # Layer 2: Non-linear adjustments
    if days == 5:
        base *= 1.05  # 5-day bonus
    
    if days_x_miles > 5000:
        if receipts < 500:
            base *= 1.08  # High mileage, low spending bonus
        else:
            base *= 0.95  # High mileage, high spending penalty
    
    # Output layer: Final adjustments
    result = base
    
    # Apply learned bounds from neural network
    result = max(150, min(2200, result))
    
    return round(result, 2)
