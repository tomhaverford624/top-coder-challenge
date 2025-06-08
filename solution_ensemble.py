#!/usr/bin/env python3

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    import math
    
    # Engineer features
    days = trip_duration_days
    miles = miles_traveled
    receipts = total_receipts_amount
    
    miles_per_day = miles / days if days > 0 else 0
    receipts_per_day = receipts / days if days > 0 else 0
    receipts_per_mile = receipts / miles if miles > 0 else 0
    days_x_miles = days * miles
    days_x_receipts = days * receipts
    miles_x_receipts = miles * receipts
    log_miles = math.log(miles + 1)
    log_receipts = math.log(receipts + 1)
    sqrt_days = math.sqrt(days)
    
    # Ensemble prediction using weighted average of simple rules
    predictions = []
    
    # Rule 1: Based on top features
    if days_x_miles <= 2000:
        pred1 = 100 * days + 0.5 * miles + 0.8 * receipts
    else:
        pred1 = 120 * days + 0.4 * miles + 0.7 * receipts
    predictions.append(pred1)

    # Rule 2: Efficiency-based
    if 150 <= miles_per_day <= 250:
        pred2 = 110 * days + 0.55 * miles + 0.75 * receipts
    else:
        pred2 = 95 * days + 0.45 * miles + 0.65 * receipts
    predictions.append(pred2)

    # Rule 3: Receipt-based
    if receipts_per_day <= 100:
        pred3 = 105 * days + 0.52 * miles + 0.85 * receipts
    else:
        pred3 = 100 * days + 0.48 * miles + 0.6 * receipts
    predictions.append(pred3)

    # Weighted average of predictions
    final_prediction = sum(predictions) / len(predictions)
    
    # Apply bounds
    final_prediction = max(100, min(2500, final_prediction))
    
    return round(final_prediction, 2)
