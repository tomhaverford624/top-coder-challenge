#!/usr/bin/env python3

import math

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """Gradient boosting ensemble for reimbursement calculation"""
    
    # Extract inputs
    days = trip_duration_days
    miles = miles_traveled
    receipts = total_receipts_amount
    
    # Engineer features
    miles_per_day = miles / days if days > 0 else 0
    receipts_per_day = receipts / days if days > 0 else 0
    receipts_per_mile = receipts / miles if miles > 0 else 0
    days_x_miles = days * miles
    days_x_receipts = days * receipts
    miles_x_receipts = miles * receipts
    log_miles = math.log(miles + 1)
    log_receipts = math.log(receipts + 1)
    sqrt_days = math.sqrt(days)
    
    # Base prediction
    prediction = 987.45  # Mean from training data
    
    # Boosting round 1: days_x_miles
    if days_x_miles <= 2000:
        prediction = prediction * 0.7
    else:
        prediction = prediction * 1.3
    
    # Boosting round 2: receipts_per_day
    if receipts_per_day <= 100:
        prediction += 50
    else:
        prediction -= 30
    
    # Boosting round 3: miles_per_day efficiency
    if 150 <= miles_per_day <= 250:
        prediction += 40
    else:
        prediction -= 20
    
    # Boosting round 4: Special cases
    if days == 5:
        prediction *= 1.05  # 5-day bonus
    
    if days >= 7 and receipts_per_day > 150:
        prediction *= 0.85  # Long trip penalty
    
    # Boosting round 5: Receipt adjustments
    if receipts < 50:
        prediction *= 0.8  # Low receipt penalty
    elif 600 <= receipts <= 800:
        prediction *= 1.02  # Sweet spot bonus
    
    # Boosting round 6: Mileage tiers
    if miles <= 100:
        mileage_component = miles * 0.58
    elif miles <= 300:
        mileage_component = 100 * 0.58 + (miles - 100) * 0.50
    else:
        mileage_component = 100 * 0.58 + 200 * 0.50 + (miles - 300) * 0.40
    
    # Combine base prediction with mileage
    prediction = prediction * 0.7 + mileage_component * 0.3
    
    # Final bounds
    prediction = max(150, min(2500, prediction))
    
    return round(prediction, 2)
