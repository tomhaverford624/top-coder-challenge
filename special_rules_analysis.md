# Special Rules Analysis for Receipts Ending in .33 and .99

## Summary of Findings

### 1. Receipts ending in .49 (Already Known)
- **Rule**: Return 50% of allowance
- **Formula**: `0.5 × (days × $55 + miles × $0.655)`

### 2. Receipts ending in .33
- **Complex rule based on allowance range**
- If allowance is between ~$570 and ~$1120:
  - The output is approximately 2× allowance, but with variations
  - Not exactly 2× - ranges from 1.82x to 2.18x
  - Needs more investigation for exact formula
- If allowance is outside this range:
  - Different ratios apply (0.90x to 1.66x)
  - No clear pattern yet identified

### 3. Receipts ending in .99
- **Rule based on receipts amount**
- If receipts < $900:
  - Return approximately the allowance (ratio 0.96x to 1.03x)
  - Small variations of ±$26
- If receipts ≥ $900:
  - Different rules apply, often returning less than allowance
  - Ratios vary from 0.67x to 0.88x
  - One case (receipts $1645.99) returns exactly 2/3 of allowance

## Test Cases Analysis

For the specific error cases mentioned:
- **Case 149**: Not in public data (likely private case)
- **Case 513**: Not in public data (likely private case)
- **Case 370**: Not in public data (likely private case)
- **Case 684**: Not in public data (likely private case)

However, similar cases in public data:
- **Case 148**: 7 days, 1006 miles, $1181.33 → Expected $2279.82
  - Allowance: $1043.93
  - Falls in the $570-$1120 range
  - Gets ~2.18× allowance
  
- **Case 512**: 8 days, 1025 miles, $1031.33 → Expected $2214.64
  - Allowance: $1111.38
  - Falls in the $570-$1120 range
  - Gets ~1.99× allowance

## Implementation Recommendation

```python
def calculate_reimbursement(days, miles, receipts):
    per_diem = 55
    mileage_rate = 0.655
    allowance = days * per_diem + miles * mileage_rate
    
    receipts_str = f"{receipts:.2f}"
    
    # Special ending rules
    if receipts_str.endswith('.49'):
        return allowance * 0.5
    
    elif receipts_str.endswith('.33'):
        if 570 <= allowance <= 1120:
            # Approximate with 2x allowance
            # Note: This is not exact and may need refinement
            return allowance * 2.0
        else:
            # For now, use standard calculation
            return allowance + receipts
    
    elif receipts_str.endswith('.99'):
        if receipts < 900:
            return allowance
        else:
            # High receipts cases - needs more investigation
            # For now, use standard calculation
            return allowance + receipts
    
    else:
        # Standard rule
        return allowance + receipts
```

## Notes
- The .33 rule with allowance in $570-$1120 range needs more investigation for the exact formula
- The .99 rule for high receipts (≥$900) needs more data to determine the exact pattern
- There may be additional edge cases or refinements needed based on private test data