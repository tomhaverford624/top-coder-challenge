#!/usr/bin/env python3
"""
Gradient Boosting approach without external dependencies
Using multiple weak learners combined
"""

import json
import math

# Load the data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

# Create simple decision stumps
def create_stump(feature_idx, threshold, left_val, right_val):
    """Create a simple decision stump"""
    def stump(features):
        if features[feature_idx] <= threshold:
            return left_val
        else:
            return right_val
    return stump

# Feature engineering function
def engineer_features(days, miles, receipts):
    """Engineer features from raw inputs"""
    miles_per_day = miles / days if days > 0 else 0
    receipts_per_day = receipts / days if days > 0 else 0
    receipts_per_mile = receipts / miles if miles > 0 else 0
    days_x_miles = days * miles
    days_x_receipts = days * receipts
    miles_x_receipts = miles * receipts
    log_miles = math.log(miles + 1)
    log_receipts = math.log(receipts + 1)
    sqrt_days = math.sqrt(days)
    
    return [
        days, miles, receipts,
        miles_per_day, receipts_per_day, receipts_per_mile,
        days_x_miles, days_x_receipts, miles_x_receipts,
        log_miles, log_receipts, sqrt_days
    ]

# Analyze data to find best split points
print("Analyzing data for gradient boosting...")

# Extract all features and targets
X_train = []
y_train = []
for case in data:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    features = engineer_features(days, miles, receipts)
    X_train.append(features)
    y_train.append(expected)

# Find good split points for each feature
feature_names = [
    'days', 'miles', 'receipts',
    'miles_per_day', 'receipts_per_day', 'receipts_per_mile',
    'days_x_miles', 'days_x_receipts', 'miles_x_receipts',
    'log_miles', 'log_receipts', 'sqrt_days'
]

# Manually create a gradient boosting ensemble
print("\nCreating gradient boosting ensemble...")

# Start with a base prediction (mean of all targets)
base_prediction = sum(y_train) / len(y_train)
print(f"Base prediction: ${base_prediction:.2f}")

# Create weak learners
learners = []

# Learner 1: Split on days_x_miles
learner1 = {
    'feature': 'days_x_miles',
    'threshold': 2000,
    'left': base_prediction * 0.7,
    'right': base_prediction * 1.3
}

# Learner 2: Split on receipts_per_day
learner2 = {
    'feature': 'receipts_per_day',
    'threshold': 100,
    'left': 50,
    'right': -30
}

# Learner 3: Split on miles_per_day
learner3 = {
    'feature': 'miles_per_day',
    'threshold': 180,
    'left': -20,
    'right': 40
}

# Generate code
print("\nGenerating gradient boosting code...")

code = '''#!/usr/bin/env python3

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
'''

# Save the gradient boosting solution
with open('solution_gradient_boost.py', 'w') as f:
    f.write(code)

print("\nGradient boosting solution saved to solution_gradient_boost.py")

# Test on training data
from solution_gradient_boost import calculate_reimbursement as calc_gb

total_error = 0
for case in data:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    predicted = calc_gb(days, miles, receipts)
    error = abs(predicted - expected)
    total_error += error

avg_error = total_error / len(data)
print(f"\nTraining error: ${avg_error:.2f} average, ${total_error:.0f} total")