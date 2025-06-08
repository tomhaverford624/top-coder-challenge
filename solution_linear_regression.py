#!/usr/bin/env python3

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Calculate reimbursement using linear regression formula.
    
    This formula was derived using linear regression on the public test cases.
    The coefficients were optimized to minimize the average absolute error.
    
    Formula: output = 50.05 * days + 0.45 * miles + 0.38 * receipts + 266.71
    
    The receipts coefficient (0.38) is naturally between 0 and 1, which makes
    sense as receipts shouldn't be multiplied by values greater than 1.
    
    Average error on public cases: $175.49
    """
    return (50.050486 * trip_duration_days + 
            0.445645 * miles_traveled + 
            0.382861 * total_receipts_amount + 
            266.707681)

# Test with a few examples
if __name__ == "__main__":
    # Test case 1: 3 days, 93 miles, $1.42 receipts
    result = calculate_reimbursement(3, 93, 1.42)
    print(f"Example 1: 3 days, 93 miles, $1.42 receipts = ${result:.2f}")
    
    # Test case 2: 1 day, 55 miles, $3.6 receipts  
    result = calculate_reimbursement(1, 55, 3.6)
    print(f"Example 2: 1 day, 55 miles, $3.6 receipts = ${result:.2f}")
    
    # Test case 3: 2 days, 202 miles, $21.24 receipts
    result = calculate_reimbursement(2, 202, 21.24)
    print(f"Example 3: 2 days, 202 miles, $21.24 receipts = ${result:.2f}")