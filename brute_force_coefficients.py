#!/usr/bin/env python3
import json

# Load public cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("Brute forcing simple linear coefficients...")
print("=" * 80)

# Let's try a simple linear formula: a*days + b*miles + c*receipts
# and brute force search for the best coefficients

best_accuracy = 0
best_coeffs = None
best_errors = []

# Try different coefficient ranges
for a in range(70, 130, 5):  # Per day coefficient
    for b in [0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]:  # Per mile
        for c in [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1]:  # Receipt multiplier
            correct = 0
            errors = []
            
            for case in cases:
                days = case['input']['trip_duration_days']
                miles = case['input']['miles_traveled']
                receipts = case['input']['total_receipts_amount']
                expected = case['expected_output']
                
                predicted = a * days + b * miles + c * receipts
                
                if abs(predicted - expected) < 0.01:
                    correct += 1
                else:
                    error = abs(predicted - expected)
                    errors.append((days, miles, receipts, expected, predicted, error))
            
            accuracy = (correct / len(cases)) * 100
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_coeffs = (a, b, c)
                best_errors = errors[:5]  # Keep first 5 errors
                print(f"New best: a={a}, b={b}, c={c}, accuracy={accuracy:.1f}%")

print("\n" + "=" * 80)
print(f"Best formula: {best_coeffs[0]}*days + {best_coeffs[1]}*miles + {best_coeffs[2]}*receipts")
print(f"Best accuracy: {best_accuracy:.1f}%")

if best_errors:
    print("\nFirst 5 errors with best formula:")
    for d, m, r, exp, pred, err in best_errors:
        print(f"  D={d}, M={m}, R=${r:.2f}: Expected ${exp:.2f}, Got ${pred:.2f}, Error=${err:.2f}")

# Let's also try some non-linear combinations
print("\n" + "=" * 80)
print("Testing non-linear formulas...")

def test_formula(formula_func, name):
    correct = 0
    errors = []
    
    for case in cases:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        predicted = formula_func(days, miles, receipts)
        
        if abs(predicted - expected) < 0.01:
            correct += 1
        else:
            error = abs(predicted - expected)
            errors.append(error)
    
    accuracy = (correct / len(cases)) * 100
    avg_error = sum(errors) / len(errors) if errors else 0
    
    print(f"{name}: Accuracy={accuracy:.1f}%, Avg Error=${avg_error:.2f}")
    return accuracy

# Test some specific formulas based on patterns
def formula1(d, m, r):
    # Maybe there's a minimum per day
    return max(100 * d, 50) + m * 0.6 + r

def formula2(d, m, r):
    # Maybe it's based on trip type
    if d == 1:
        return 100 + m * 1.2 + r
    else:
        return d * 90 + m * 0.8 + r

def formula3(d, m, r):
    # What if there's a base amount plus variable
    return 50 + d * 70 + m * 0.6 + r

def formula4(d, m, r):
    # Try the coefficient we found
    return best_coeffs[0] * d + best_coeffs[1] * m + best_coeffs[2] * r

formulas = [
    (formula1, "max(100*d, 50) + m*0.6 + r"),
    (formula2, "Variable by trip length"),
    (formula3, "50 + d*70 + m*0.6 + r"),
    (formula4, f"{best_coeffs[0]}*d + {best_coeffs[1]}*m + {best_coeffs[2]}*r")
]

for func, name in formulas:
    test_formula(func, name)