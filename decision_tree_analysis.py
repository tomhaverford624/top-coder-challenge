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
    X.append([
        case['input']['trip_duration_days'],
        case['input']['miles_traveled'],
        case['input']['total_receipts_amount']
    ])
    y.append(case['expected_output'])

X = np.array(X)
y = np.array(y)

print(f"Dataset size: {len(X)} samples")
print(f"Features: trip_duration_days, miles_traveled, total_receipts_amount")
print(f"Target range: {y.min():.2f} to {y.max():.2f}")

# Try different max_depth values
for max_depth in [2, 3, 4, 5]:
    print(f"\n{'='*50}")
    print(f"Testing DecisionTreeRegressor with max_depth={max_depth}")
    
    # Create and train the model with aggressive pruning
    model = DecisionTreeRegressor(
        max_depth=max_depth,
        min_samples_leaf=50,  # Require at least 50 samples in each leaf
        min_samples_split=100,  # Require at least 100 samples to split
        random_state=42
    )
    
    model.fit(X, y)
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate metrics
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    print(f"MAE: {mae:.2f}")
    print(f"R² Score: {r2:.4f}")
    print(f"Number of leaves: {model.get_n_leaves()}")
    
    # Export the decision tree rules
    feature_names = ['trip_duration_days', 'miles_traveled', 'total_receipts_amount']
    tree_rules = export_text(model, feature_names=feature_names)
    print("\nDecision Tree Rules:")
    print(tree_rules)
    
    # Create a visualization
    plt.figure(figsize=(15, 10))
    plot_tree(model, 
              feature_names=feature_names,
              filled=True,
              rounded=True,
              fontsize=10)
    plt.title(f'Decision Tree (max_depth={max_depth})')
    plt.tight_layout()
    plt.savefig(f'decision_tree_depth_{max_depth}.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Extract the tree structure for manual implementation
    print("\nTree structure for manual implementation:")
    tree = model.tree_
    
    def print_tree_structure(node=0, depth=0):
        indent = "  " * depth
        
        if tree.feature[node] != -2:  # Not a leaf
            feature = feature_names[tree.feature[node]]
            threshold = tree.threshold[node]
            print(f"{indent}if {feature} <= {threshold:.2f}:")
            print_tree_structure(tree.children_left[node], depth + 1)
            print(f"{indent}else:  # {feature} > {threshold:.2f}")
            print_tree_structure(tree.children_right[node], depth + 1)
        else:  # Leaf node
            value = tree.value[node][0][0]
            n_samples = tree.n_node_samples[node]
            print(f"{indent}return {value:.2f}  # ({n_samples} samples)")
    
    print_tree_structure()

# Select the best model based on the analysis
print("\n" + "="*50)
print("RECOMMENDATION:")
print("Based on the analysis, choose the model with the best balance of:")
print("1. Low MAE (good accuracy)")
print("2. Simple structure (few leaves)")
print("3. Good generalization (not overfitting)")