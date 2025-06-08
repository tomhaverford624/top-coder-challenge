#!/usr/bin/env python3

import json
import numpy as np
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# Load the data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

# Extract features and targets
X = []
y = []
for case in data:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    
    # Original features
    features = [days, miles, receipts]
    
    # Add engineered features
    features.append(miles / days if days > 0 else 0)  # miles per day
    features.append(receipts / days if days > 0 else 0)  # receipts per day
    features.append(receipts / miles if miles > 0 else 0)  # receipts per mile
    features.append(days * miles)  # interaction term
    features.append(days * receipts)  # interaction term
    features.append(miles * receipts)  # interaction term
    
    X.append(features)
    y.append(case['expected_output'])

X = np.array(X)
y = np.array(y)

feature_names = [
    'trip_duration_days', 
    'miles_traveled', 
    'total_receipts_amount',
    'miles_per_day',
    'receipts_per_day',
    'receipts_per_mile',
    'days_x_miles',
    'days_x_receipts',
    'miles_x_receipts'
]

print(f"Dataset size: {len(X)} samples")
print(f"Number of features: {X.shape[1]}")
print(f"Target range: {y.min():.2f} to {y.max():.2f}")

# Try different configurations
configs = [
    {'max_depth': 4, 'min_samples_leaf': 30},
    {'max_depth': 5, 'min_samples_leaf': 20},
    {'max_depth': 6, 'min_samples_leaf': 15},
    {'max_depth': 7, 'min_samples_leaf': 10},
]

best_mae = float('inf')
best_model = None
best_config = None

for config in configs:
    print(f"\n{'='*50}")
    print(f"Testing DecisionTreeRegressor with {config}")
    
    model = DecisionTreeRegressor(
        max_depth=config['max_depth'],
        min_samples_leaf=config['min_samples_leaf'],
        min_samples_split=config['min_samples_leaf'] * 2,
        random_state=42
    )
    
    model.fit(X, y)
    y_pred = model.predict(X)
    
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    print(f"MAE: {mae:.2f}")
    print(f"R² Score: {r2:.4f}")
    print(f"Number of leaves: {model.get_n_leaves()}")
    
    # Check feature importances
    importances = model.feature_importances_
    print("\nFeature Importances:")
    for i, imp in enumerate(importances):
        if imp > 0.01:  # Only show features with > 1% importance
            print(f"  {feature_names[i]}: {imp:.4f}")
    
    if mae < best_mae:
        best_mae = mae
        best_model = model
        best_config = config

print(f"\n{'='*50}")
print(f"BEST MODEL: {best_config}")
print(f"Best MAE: {best_mae:.2f}")

# Export the best model's rules
print("\nBest Model Decision Rules:")
tree_rules = export_text(best_model, feature_names=feature_names, max_depth=3)
print(tree_rules)

# Generate Python code for the best model
print("\nGenerating optimized Python implementation...")

def generate_python_code(model, feature_names):
    tree = model.tree_
    
    code_lines = []
    code_lines.append("def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):")
    code_lines.append("    # Calculate derived features")
    code_lines.append("    miles_per_day = miles_traveled / trip_duration_days if trip_duration_days > 0 else 0")
    code_lines.append("    receipts_per_day = total_receipts_amount / trip_duration_days if trip_duration_days > 0 else 0")
    code_lines.append("    receipts_per_mile = total_receipts_amount / miles_traveled if miles_traveled > 0 else 0")
    code_lines.append("    days_x_miles = trip_duration_days * miles_traveled")
    code_lines.append("    days_x_receipts = trip_duration_days * total_receipts_amount")
    code_lines.append("    miles_x_receipts = miles_traveled * total_receipts_amount")
    code_lines.append("    ")
    code_lines.append("    # Decision tree logic")
    
    def add_node(node=0, depth=1):
        indent = "    " * depth
        
        if tree.feature[node] != -2:  # Not a leaf
            feature = feature_names[tree.feature[node]]
            threshold = tree.threshold[node]
            code_lines.append(f"{indent}if {feature} <= {threshold:.2f}:")
            add_node(tree.children_left[node], depth + 1)
            code_lines.append(f"{indent}else:  # {feature} > {threshold:.2f}")
            add_node(tree.children_right[node], depth + 1)
        else:  # Leaf node
            value = tree.value[node][0][0]
            code_lines.append(f"{indent}return {value:.2f}")
    
    add_node()
    
    return "\n".join(code_lines)

python_code = generate_python_code(best_model, feature_names)
print(python_code)

# Save the optimized solution
with open('solution_optimized.py', 'w') as f:
    f.write("#!/usr/bin/env python3\n\n")
    f.write(python_code)
    f.write("\n")

print("\nOptimized solution saved to solution_optimized.py")