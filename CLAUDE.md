# Top Coder Reimbursement System Reverse Engineering Strategy

## System Overview & Current Understanding

### Problem Definition
- **Goal**: Reverse-engineer a 60-year-old reimbursement system from 1,000 input/output examples
- **Challenge**: System has undocumented quirks and bugs that must be preserved
- **Warning**: Don't overfit on public data - private cases will determine final score

### Current Model Components
1. **Base**: $105/day with penalties for 5+ day trips (-$75/day on all days)
2. **Mileage**: Tiered ($0.58 first 100 miles, $0.45 after) with efficiency modifiers
3. **Receipts**: Complex tiers with $1000 cap
4. **Special Rules**: .49, .33, .99 endings have unique calculations

### Current Performance
- Average Error: ~$150
- Score: ~15,000
- Key Issue: Still missing critical patterns

## Strategic Analysis Framework

### 1. Root Cause Decomposition
**Why are we still having high errors?**
- First Why: Our formula doesn't match expected outputs
- Second Why: We're missing some calculation rules
- Third Why: The system has hidden patterns we haven't discovered
- Fourth Why: We haven't fully leveraged all available clues
- Fifth Why: We may be thinking too linearly about the problem

### 2. Kaizen Protocol for Pattern Discovery

#### Micro-Improvements to Make:
1. **Interview Deep Dive**: Re-read INTERVIEWS.md focusing on:
   - Exact phrases about calculations
   - Contradictions between employees (might indicate conditional rules)
   - Temporal patterns mentioned but disputed
   
2. **Error Pattern Analysis**: Group errors by:
   - Trip duration
   - Efficiency ranges
   - Receipt amount ranges
   - Day of week/month patterns (if derivable)

3. **Edge Case Catalog**: Document every case with error > $500

#### Measurement Framework:
- Track error reduction after each rule discovery
- Note which employee hints correlate with actual patterns
- Monitor overfitting risk by testing generalizations

### 3. Systems Thinking Model

```
┌─────────────────────────────────────────────────┐
│                 Input Variables                  │
│  - Trip Duration                                 │
│  - Miles Traveled                                │
│  - Receipt Amount                                │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│             Hidden State Variables               │
│  - Day of Week?                                  │
│  - Seasonal Factors?                             │
│  - Receipt Patterns (beyond .49/.33/.99)?        │
│  - Cumulative Trip History?                      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│            Processing Rules                      │
│  - Base Calculation                              │
│  - Mileage Tiers                                 │
│  - Receipt Processing                            │
│  - Special Ending Rules                          │
│  - [UNKNOWN RULES]                               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│               Output                             │
│         Reimbursement Amount                     │
└─────────────────────────────────────────────────┘
```

### 4. Hypothesis Testing Framework

#### Current Hypotheses to Test:
1. **Temporal Patterns**: Despite disputes, there might be weekly/monthly patterns
2. **Receipt Threshold Rules**: Additional special amounts beyond endings
3. **Compound Conditions**: Rules that only apply when multiple conditions are met
4. **Historical Bugs**: Calculation errors that became "features"

#### Testing Approach:
- Group cases by suspected pattern
- Calculate expected vs actual for each group
- Look for consistent deviations

### 5. Pattern Recognition Blind Spots

#### Areas We Haven't Explored:
1. **Interaction Effects**: 
   - Does 5-day bonus interact differently with certain receipt amounts?
   - Are efficiency bonuses modified by trip duration?

2. **Non-Linear Relationships**:
   - Quadratic or logarithmic components?
   - Step functions at specific thresholds?

3. **Legacy System Artifacts**:
   - Rounding errors from old decimal systems
   - Integer overflow patterns
   - Floating point precision issues

## Implementation Roadmap

### Phase 1: Immediate Actions (Next 30 minutes)
1. Re-analyze INTERVIEWS.md for missed clues
2. Create error clustering visualization
3. Test for day-of-week patterns using case numbers as proxy

### Phase 2: Pattern Mining (Next 2 hours)
1. Examine all cases with error > $400
2. Look for receipt amounts that consistently produce errors
3. Test interaction effects between variables

### Phase 3: Model Refinement (Next 1 hour)
1. Implement discovered patterns
2. Test against public cases
3. Ensure we're not overfitting

## Key Principles to Remember

1. **The bugs are features**: Don't try to "fix" illogical patterns
2. **Employees know partial truths**: Each interview contains real insights
3. **Simple patterns hide in complex data**: Look for elegant explanations
4. **Overfitting is the enemy**: Patterns must generalize to private cases

## Next Analysis Questions

1. What did Marcus mean by "Wednesday thing"?
2. Why do some .33 cases return 2x allowance while others don't?
3. Are there more "magic numbers" like .49/.33/.99?
4. What causes the $1000 receipt cap to sometimes not apply?
5. Is there a pattern to which cases get exact matches vs close matches?

## Success Metrics

- Reduce average error below $100
- Achieve at least 10% exact matches
- Find patterns that explain 90%+ of cases
- Maintain generalization to private cases