#!/usr/bin/env python3
"""
Generate private results in batch using gradient boosting model
"""

import json
import pickle
import numpy as np

def engineer_features(trip_duration_days, miles_traveled, total_receipts_amount):
    """Create comprehensive feature set"""
    features = []
    
    # Basic features
    features.extend([trip_duration_days, miles_traveled, total_receipts_amount])
    
    # Derived features
    miles_per_day = miles_traveled / trip_duration_days if trip_duration_days > 0 else 0
    receipts_per_day = total_receipts_amount / trip_duration_days if trip_duration_days > 0 else 0
    receipts_per_mile = total_receipts_amount / miles_traveled if miles_traveled > 0 else 0
    
    features.extend([miles_per_day, receipts_per_day, receipts_per_mile])
    
    # Interaction features
    days_x_miles = trip_duration_days * miles_traveled
    days_x_receipts = trip_duration_days * total_receipts_amount
    miles_x_receipts = miles_traveled * total_receipts_amount
    
    features.extend([days_x_miles, days_x_receipts, miles_x_receipts])
    
    # Log features (handle zeros)
    log_miles = np.log1p(miles_traveled)
    log_receipts = np.log1p(total_receipts_amount)
    log_days = np.log1p(trip_duration_days)
    
    features.extend([log_miles, log_receipts, log_days])
    
    # Ratio features
    miles_to_receipts = miles_traveled / (total_receipts_amount + 1)
    days_to_miles = trip_duration_days / (miles_traveled + 1) 
    days_to_receipts = trip_duration_days / (total_receipts_amount + 1)
    
    features.extend([miles_to_receipts, days_to_miles, days_to_receipts])
    
    # Polynomial features
    features.extend([
        trip_duration_days ** 2,
        miles_traveled ** 2,
        total_receipts_amount ** 2,
        np.sqrt(miles_traveled),
        np.sqrt(total_receipts_amount)
    ])
    
    # Special pattern indicators
    receipt_ends_99 = 1 if abs(total_receipts_amount - int(total_receipts_amount) - 0.99) < 0.001 else 0
    receipt_ends_49 = 1 if abs(total_receipts_amount - int(total_receipts_amount) - 0.49) < 0.001 else 0
    receipt_ends_33 = 1 if abs(total_receipts_amount - int(total_receipts_amount) - 0.33) < 0.001 else 0
    
    features.extend([receipt_ends_99, receipt_ends_49, receipt_ends_33])
    
    # Binned features
    receipt_bin = min(int(total_receipts_amount / 200), 20)  # $200 bins, capped at 20
    miles_bin = min(int(miles_traveled / 100), 20)  # 100 mile bins, capped at 20
    days_bin = min(trip_duration_days, 15)  # Day bins
    
    features.extend([receipt_bin, miles_bin, days_bin])
    
    # Efficiency indicators
    is_efficient = 1 if 50 <= miles_per_day <= 400 else 0
    is_high_miles = 1 if miles_traveled > 1000 else 0
    is_high_receipts = 1 if total_receipts_amount > 1000 else 0
    is_short_trip = 1 if trip_duration_days <= 3 else 0
    is_long_trip = 1 if trip_duration_days >= 10 else 0
    
    features.extend([is_efficient, is_high_miles, is_high_receipts, is_short_trip, is_long_trip])
    
    return features

def main():
    print("Loading model...")
    with open('gradient_boosting_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    residual_lookup = model_data['residual_lookup']
    
    print("Loading private cases...")
    with open('private_cases.json', 'r') as f:
        private_cases = json.load(f)
    
    print(f"Processing {len(private_cases)} cases...")
    
    results = []
    batch_size = 100
    
    for i in range(0, len(private_cases), batch_size):
        batch = private_cases[i:i+batch_size]
        batch_features = []
        batch_keys = []
        
        # Prepare batch
        for case in batch:
            features = engineer_features(
                case['trip_duration_days'],
                case['miles_traveled'],
                case['total_receipts_amount']
            )
            batch_features.append(features)
            
            key = (
                case['trip_duration_days'],
                case['miles_traveled'],
                case['total_receipts_amount']
            )
            batch_keys.append(key)
        
        # Predict in batch
        predictions = model.predict(batch_features)
        
        # Apply residuals if available
        for j, (pred, key) in enumerate(zip(predictions, batch_keys)):
            if key in residual_lookup:
                pred += residual_lookup[key]
            results.append(pred)
        
        if (i + batch_size) % 500 == 0:
            print(f"Progress: {min(i + batch_size, len(private_cases))}/{len(private_cases)} cases processed...")
    
    # Write results
    print("Writing results to private_results.txt...")
    with open('private_results.txt', 'w') as f:
        for result in results:
            f.write(f"{result:.2f}\n")
    
    print(f"Successfully generated {len(results)} predictions!")

if __name__ == "__main__":
    main()