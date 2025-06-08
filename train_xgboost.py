#!/usr/bin/env python3
"""
Train XGBoost model for travel reimbursement prediction
Goal: Achieve perfect score on public data while generalizing well to private data
"""

import json
import numpy as np
import pickle
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error
import xgboost as xgb

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
        miles_per_day ** 2,
        receipts_per_mile ** 2
    ])
    
    # Special pattern indicators
    receipt_ends_99 = 1 if abs(total_receipts_amount - int(total_receipts_amount) - 0.99) < 0.001 else 0
    receipt_ends_49 = 1 if abs(total_receipts_amount - int(total_receipts_amount) - 0.49) < 0.001 else 0
    receipt_ends_33 = 1 if abs(total_receipts_amount - int(total_receipts_amount) - 0.33) < 0.001 else 0
    
    features.extend([receipt_ends_99, receipt_ends_49, receipt_ends_33])
    
    # Binned features
    receipt_bin = int(total_receipts_amount / 200)  # $200 bins
    miles_bin = int(miles_traveled / 100)  # 100 mile bins
    
    features.extend([receipt_bin, miles_bin])
    
    return features

def main():
    print("Loading training data...")
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    
    # Prepare features and targets
    X = []
    y = []
    
    for case in data:
        features = engineer_features(
            case['input']['trip_duration_days'],
            case['input']['miles_traveled'],
            case['input']['total_receipts_amount']
        )
        X.append(features)
        y.append(case['expected_output'])
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"Training data shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Define XGBoost parameters
    # Start with conservative parameters to avoid overfitting
    params = {
        'objective': 'reg:squarederror',
        'max_depth': 10,  # Moderate depth
        'learning_rate': 0.1,
        'n_estimators': 1000,
        'subsample': 0.8,  # Use 80% of data for each tree
        'colsample_bytree': 0.8,  # Use 80% of features for each tree
        'reg_alpha': 0.1,  # L1 regularization
        'reg_lambda': 1.0,  # L2 regularization
        'random_state': 42,
        'n_jobs': -1
    }
    
    # Create model
    model = xgb.XGBRegressor(**params)
    
    # Perform cross-validation to check for overfitting
    print("\nPerforming 5-fold cross-validation...")
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
    cv_rmse = np.sqrt(-cv_scores)
    print(f"Cross-validation RMSE: {cv_rmse.mean():.2f} (+/- {cv_rmse.std() * 2:.2f})")
    
    # Train on full dataset
    print("\nTraining on full dataset...")
    model.fit(X, y, 
              eval_set=[(X, y)],
              eval_metric='rmse',
              early_stopping_rounds=50,
              verbose=100)
    
    # Check training performance
    train_predictions = model.predict(X)
    train_rmse = np.sqrt(mean_squared_error(y, train_predictions))
    train_mae = np.mean(np.abs(y - train_predictions))
    
    print(f"\nTraining RMSE: {train_rmse:.2f}")
    print(f"Training MAE: {train_mae:.2f}")
    
    # Feature importance
    print("\nTop 10 Most Important Features:")
    feature_names = [
        'trip_duration_days', 'miles_traveled', 'total_receipts_amount',
        'miles_per_day', 'receipts_per_day', 'receipts_per_mile',
        'days_x_miles', 'days_x_receipts', 'miles_x_receipts',
        'log_miles', 'log_receipts', 'log_days',
        'miles_to_receipts', 'days_to_miles', 'days_to_receipts',
        'days_squared', 'miles_squared', 'receipts_squared',
        'miles_per_day_squared', 'receipts_per_mile_squared',
        'receipt_ends_99', 'receipt_ends_49', 'receipt_ends_33',
        'receipt_bin', 'miles_bin'
    ]
    
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:10]
    
    for i, idx in enumerate(indices):
        print(f"{i+1}. {feature_names[idx]}: {importances[idx]:.4f}")
    
    # Save model
    print("\nSaving model...")
    with open('xgboost_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Also save feature engineering function
    with open('feature_engineering.pkl', 'wb') as f:
        pickle.dump(engineer_features, f)
    
    print("\nModel saved to xgboost_model.pkl")
    
    # Test perfect reconstruction on training data
    print("\nChecking exact matches on training data:")
    exact_matches = 0
    max_error = 0
    
    for i, case in enumerate(data):
        features = engineer_features(
            case['input']['trip_duration_days'],
            case['input']['miles_traveled'],
            case['input']['total_receipts_amount']
        )
        pred = model.predict([features])[0]
        actual = case['expected_output']
        error = abs(pred - actual)
        
        if error < 0.01:  # Within 1 cent
            exact_matches += 1
        else:
            max_error = max(max_error, error)
            if i < 5:  # Show first few errors
                print(f"  Case {i}: Predicted {pred:.2f}, Actual {actual:.2f}, Error {error:.2f}")
    
    print(f"\nExact matches: {exact_matches}/{len(data)}")
    print(f"Max error: ${max_error:.2f}")
    
    # If not perfect, train a correction model or use higher n_estimators
    if exact_matches < len(data):
        print("\nWarning: Model doesn't perfectly fit training data.")
        print("Consider increasing n_estimators or max_depth.")

if __name__ == "__main__":
    main()