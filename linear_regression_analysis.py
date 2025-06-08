#!/usr/bin/env python3

import json
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize
import pandas as pd

# Load the data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

# Prepare data for linear regression
X = []
y = []

for case in data:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    
    # X matrix: [days, miles, receipts, 1] for formula: a*days + b*miles + c*receipts + d
    X.append([days, miles, receipts, 1])
    y.append(case['expected_output'])

X = np.array(X)
y = np.array(y)

print(f"Dataset size: {len(y)} cases")
print(f"\nData statistics:")
print(f"Days: min={X[:, 0].min()}, max={X[:, 0].max()}, mean={X[:, 0].mean():.2f}")
print(f"Miles: min={X[:, 1].min()}, max={X[:, 1].max()}, mean={X[:, 1].mean():.2f}")
print(f"Receipts: min={X[:, 2].min():.2f}, max={X[:, 2].max():.2f}, mean={X[:, 2].mean():.2f}")
print(f"Output: min={y.min():.2f}, max={y.max():.2f}, mean={y.mean():.2f}")

# Method 1: Standard Linear Regression (no constraints)
print("\n" + "="*60)
print("METHOD 1: Standard Linear Regression (no constraints)")
print("="*60)

lr = LinearRegression(fit_intercept=False)  # We include intercept in X
lr.fit(X, y)

coefficients = lr.coef_
a, b, c, d = coefficients

print(f"\nCoefficients:")
print(f"a (days coefficient): {a:.6f}")
print(f"b (miles coefficient): {b:.6f}")
print(f"c (receipts coefficient): {c:.6f}")
print(f"d (intercept): {d:.6f}")

# Test the formula
predictions = X @ coefficients
errors = np.abs(predictions - y)
avg_error = np.mean(errors)
max_error = np.max(errors)
rmse = np.sqrt(np.mean((predictions - y)**2))

print(f"\nPerformance:")
print(f"Average absolute error: ${avg_error:.2f}")
print(f"Maximum absolute error: ${max_error:.2f}")
print(f"RMSE: ${rmse:.2f}")
print(f"R² score: {lr.score(X, y):.6f}")

# Show some example predictions
print("\nSample predictions (first 10 cases):")
for i in range(min(10, len(y))):
    print(f"Case {i+1}: Actual=${y[i]:.2f}, Predicted=${predictions[i]:.2f}, Error=${errors[i]:.2f}")

# Method 2: Constrained optimization (c between 0 and 1)
print("\n" + "="*60)
print("METHOD 2: Constrained Optimization (0 ≤ c ≤ 1)")
print("="*60)

def objective(params):
    """Minimize sum of squared errors"""
    predictions = X @ params
    return np.sum((predictions - y)**2)

# Initial guess (from unconstrained solution)
initial_guess = coefficients.copy()
initial_guess[2] = np.clip(initial_guess[2], 0, 1)  # Clip c to [0, 1]

# Define bounds: no bounds for a, b, d; c in [0, 1]
bounds = [
    (None, None),  # a (days)
    (None, None),  # b (miles)
    (0, 1),        # c (receipts)
    (None, None)   # d (intercept)
]

# Optimize
result = minimize(objective, initial_guess, bounds=bounds, method='L-BFGS-B')

if result.success:
    a_const, b_const, c_const, d_const = result.x
    
    print(f"\nConstrained Coefficients:")
    print(f"a (days coefficient): {a_const:.6f}")
    print(f"b (miles coefficient): {b_const:.6f}")
    print(f"c (receipts coefficient): {c_const:.6f}")
    print(f"d (intercept): {d_const:.6f}")
    
    # Test the constrained formula
    predictions_const = X @ result.x
    errors_const = np.abs(predictions_const - y)
    avg_error_const = np.mean(errors_const)
    max_error_const = np.max(errors_const)
    rmse_const = np.sqrt(np.mean((predictions_const - y)**2))
    
    print(f"\nPerformance:")
    print(f"Average absolute error: ${avg_error_const:.2f}")
    print(f"Maximum absolute error: ${max_error_const:.2f}")
    print(f"RMSE: ${rmse_const:.2f}")
    
    # Calculate R²
    ss_res = np.sum((y - predictions_const)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2_const = 1 - (ss_res / ss_tot)
    print(f"R² score: {r2_const:.6f}")
    
    print("\nSample predictions (first 10 cases):")
    for i in range(min(10, len(y))):
        print(f"Case {i+1}: Actual=${y[i]:.2f}, Predicted=${predictions_const[i]:.2f}, Error=${errors_const[i]:.2f}")

# Method 3: Try other constraint combinations
print("\n" + "="*60)
print("METHOD 3: Additional Constraints (all coefficients ≥ 0)")
print("="*60)

# All coefficients non-negative
bounds_positive = [
    (0, None),     # a (days) ≥ 0
    (0, None),     # b (miles) ≥ 0
    (0, None),     # c (receipts) ≥ 0
    (0, None)      # d (intercept) ≥ 0
]

result_pos = minimize(objective, np.abs(coefficients), bounds=bounds_positive, method='L-BFGS-B')

if result_pos.success:
    a_pos, b_pos, c_pos, d_pos = result_pos.x
    
    print(f"\nPositive Coefficients:")
    print(f"a (days coefficient): {a_pos:.6f}")
    print(f"b (miles coefficient): {b_pos:.6f}")
    print(f"c (receipts coefficient): {c_pos:.6f}")
    print(f"d (intercept): {d_pos:.6f}")
    
    predictions_pos = X @ result_pos.x
    errors_pos = np.abs(predictions_pos - y)
    avg_error_pos = np.mean(errors_pos)
    
    print(f"\nPerformance:")
    print(f"Average absolute error: ${avg_error_pos:.2f}")

# Summary comparison
print("\n" + "="*60)
print("SUMMARY COMPARISON")
print("="*60)
print(f"\nUnconstrained Linear Regression:")
print(f"  Formula: {a:.6f} * days + {b:.6f} * miles + {c:.6f} * receipts + {d:.6f}")
print(f"  Average Error: ${avg_error:.2f}")

if result.success:
    print(f"\nConstrained (0 ≤ c ≤ 1):")
    print(f"  Formula: {a_const:.6f} * days + {b_const:.6f} * miles + {c_const:.6f} * receipts + {d_const:.6f}")
    print(f"  Average Error: ${avg_error_const:.2f}")

if result_pos.success:
    print(f"\nAll Positive Coefficients:")
    print(f"  Formula: {a_pos:.6f} * days + {b_pos:.6f} * miles + {c_pos:.6f} * receipts + {d_pos:.6f}")
    print(f"  Average Error: ${avg_error_pos:.2f}")

# Save the best formula
best_method = "unconstrained"
best_coeffs = coefficients
best_error = avg_error

if result.success and avg_error_const < best_error:
    best_method = "constrained"
    best_coeffs = result.x
    best_error = avg_error_const

if result_pos.success and avg_error_pos < best_error:
    best_method = "positive"
    best_coeffs = result_pos.x
    best_error = avg_error_pos

print(f"\n{'='*60}")
print(f"BEST METHOD: {best_method}")
print(f"Best Formula: {best_coeffs[0]:.6f} * days + {best_coeffs[1]:.6f} * miles + {best_coeffs[2]:.6f} * receipts + {best_coeffs[3]:.6f}")
print(f"Average Error: ${best_error:.2f}")
print(f"{'='*60}")