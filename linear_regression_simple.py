#!/usr/bin/env python3

import json
import math

# Load the data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

# Prepare data for linear regression
X = []  # Feature matrix
y = []  # Target values

for case in data:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    
    # X matrix: [days, miles, receipts, 1] for formula: a*days + b*miles + c*receipts + d
    X.append([days, miles, receipts, 1])
    y.append(case['expected_output'])

n = len(y)
print(f"Dataset size: {n} cases")

# Convert to manual matrix operations
# Normal equation: (X^T * X)^-1 * X^T * y

# Transpose X
X_T = [[X[j][i] for j in range(n)] for i in range(4)]

# Compute X^T * X (4x4 matrix)
XTX = [[0 for _ in range(4)] for _ in range(4)]
for i in range(4):
    for j in range(4):
        for k in range(n):
            XTX[i][j] += X_T[i][k] * X[k][j]

# Compute X^T * y (4x1 vector)
XTy = [0 for _ in range(4)]
for i in range(4):
    for k in range(n):
        XTy[i] += X_T[i][k] * y[k]

# Helper function to solve 4x4 system using Gaussian elimination
def solve_linear_system(A, b):
    """Solve Ax = b for 4x4 matrix A"""
    # Create augmented matrix
    aug = [A[i][:] + [b[i]] for i in range(4)]
    
    # Forward elimination
    for i in range(4):
        # Find pivot
        max_row = i
        for k in range(i + 1, 4):
            if abs(aug[k][i]) > abs(aug[max_row][i]):
                max_row = k
        aug[i], aug[max_row] = aug[max_row], aug[i]
        
        # Make all rows below this one 0 in current column
        for k in range(i + 1, 4):
            c = aug[k][i] / aug[i][i]
            for j in range(i, 5):
                aug[k][j] -= c * aug[i][j]
    
    # Back substitution
    x = [0 for _ in range(4)]
    for i in range(3, -1, -1):
        x[i] = aug[i][4]
        for j in range(i + 1, 4):
            x[i] -= aug[i][j] * x[j]
        x[i] /= aug[i][i]
    
    return x

# Solve for coefficients
coefficients = solve_linear_system(XTX, XTy)
a, b, c, d = coefficients

print(f"\nLinear Regression Coefficients:")
print(f"a (days coefficient): {a:.6f}")
print(f"b (miles coefficient): {b:.6f}")
print(f"c (receipts coefficient): {c:.6f}")
print(f"d (intercept): {d:.6f}")

print(f"\nFormula: output = {a:.6f} * days + {b:.6f} * miles + {c:.6f} * receipts + {d:.6f}")

# Test the formula
total_error = 0
max_error = 0
errors = []

print("\nSample predictions (first 20 cases):")
for i, case in enumerate(data):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    actual = case['expected_output']
    
    predicted = a * days + b * miles + c * receipts + d
    error = abs(predicted - actual)
    errors.append(error)
    total_error += error
    max_error = max(max_error, error)
    
    if i < 20:
        print(f"Case {i+1}: Actual=${actual:.2f}, Predicted=${predicted:.2f}, Error=${error:.2f}")

avg_error = total_error / n

print(f"\nPerformance Summary:")
print(f"Average absolute error: ${avg_error:.2f}")
print(f"Maximum absolute error: ${max_error:.2f}")

# Calculate RMSE
rmse = math.sqrt(sum((a * X[i][0] + b * X[i][1] + c * X[i][2] + d - y[i])**2 for i in range(n)) / n)
print(f"RMSE: ${rmse:.2f}")

# Calculate R²
y_mean = sum(y) / n
ss_tot = sum((y[i] - y_mean)**2 for i in range(n))
ss_res = sum((y[i] - (a * X[i][0] + b * X[i][1] + c * X[i][2] + d))**2 for i in range(n))
r2 = 1 - (ss_res / ss_tot)
print(f"R² score: {r2:.6f}")

# Now let's try with constraints
print("\n" + "="*60)
print("Trying Constrained Optimization (simple gradient descent)")
print("="*60)

# Simple gradient descent with constraints
def gradient_descent_constrained(X, y, learning_rate=0.0001, iterations=100000):
    # Initialize coefficients
    a, b, c, d = 50, 1, 0.5, 50  # Initial guess
    
    best_error = float('inf')
    best_coeffs = [a, b, c, d]
    
    for iter in range(iterations):
        # Calculate gradients
        grad_a = 0
        grad_b = 0
        grad_c = 0
        grad_d = 0
        
        for i in range(n):
            pred = a * X[i][0] + b * X[i][1] + c * X[i][2] + d
            error = pred - y[i]
            grad_a += 2 * error * X[i][0] / n
            grad_b += 2 * error * X[i][1] / n
            grad_c += 2 * error * X[i][2] / n
            grad_d += 2 * error / n
        
        # Update coefficients
        a -= learning_rate * grad_a
        b -= learning_rate * grad_b
        c -= learning_rate * grad_c
        d -= learning_rate * grad_d
        
        # Apply constraint: c between 0 and 1
        c = max(0, min(1, c))
        
        # Calculate current error
        if iter % 10000 == 0:
            total_err = sum(abs(a * X[i][0] + b * X[i][1] + c * X[i][2] + d - y[i]) for i in range(n)) / n
            if total_err < best_error:
                best_error = total_err
                best_coeffs = [a, b, c, d]
            
            if iter % 50000 == 0:
                print(f"Iteration {iter}: avg_error=${total_err:.2f}, coeffs=[{a:.3f}, {b:.3f}, {c:.3f}, {d:.3f}]")
    
    return best_coeffs

# Run constrained optimization
print("\nRunning gradient descent with constraint 0 ≤ c ≤ 1...")
a_c, b_c, c_c, d_c = gradient_descent_constrained(X, y)

print(f"\nConstrained Coefficients:")
print(f"a (days coefficient): {a_c:.6f}")
print(f"b (miles coefficient): {b_c:.6f}")
print(f"c (receipts coefficient): {c_c:.6f}")
print(f"d (intercept): {d_c:.6f}")

# Test constrained formula
total_error_c = 0
for case in data:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    actual = case['expected_output']
    
    predicted = a_c * days + b_c * miles + c_c * receipts + d_c
    error = abs(predicted - actual)
    total_error_c += error

avg_error_c = total_error_c / n
print(f"\nConstrained formula average error: ${avg_error_c:.2f}")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"\nUnconstrained Linear Regression:")
print(f"  Formula: {a:.6f} * days + {b:.6f} * miles + {c:.6f} * receipts + {d:.6f}")
print(f"  Average Error: ${avg_error:.2f}")
print(f"\nConstrained (0 ≤ c ≤ 1):")
print(f"  Formula: {a_c:.6f} * days + {b_c:.6f} * miles + {c_c:.6f} * receipts + {d_c:.6f}")
print(f"  Average Error: ${avg_error_c:.2f}")

if avg_error < avg_error_c:
    print(f"\nBest: Unconstrained with average error ${avg_error:.2f}")
else:
    print(f"\nBest: Constrained with average error ${avg_error_c:.2f}")