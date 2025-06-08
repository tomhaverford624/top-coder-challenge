#!/usr/bin/env python3
"""
Genetic Algorithm to Evolve Optimal Formula
Goal: Evolve coefficients and rules to minimize prediction error
"""

import json
import numpy as np
import random
from deap import base, creator, tools, algorithms
import warnings
warnings.filterwarnings('ignore')

# Load the data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

# Prepare data
cases = []
for case in data:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    cases.append((days, miles, receipts, expected))

# Define the individual structure
# Gene: [base_per_diem, mile_rate1, mile_rate2, mile_rate3, receipt_rate1, receipt_rate2, 
#        efficiency_bonus, 5day_multiplier, threshold1, threshold2, ...]
GENE_SIZE = 20

# Setup DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Gene initialization
toolbox.register("attr_float", random.uniform, 0, 200)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=GENE_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate_formula(individual):
    """Evaluate a formula encoded in the individual's genes"""
    total_error = 0
    
    # Extract genes
    base_per_diem = individual[0]
    mile_rate1 = individual[1] / 100  # Scale to reasonable range
    mile_rate2 = individual[2] / 100
    mile_rate3 = individual[3] / 100
    receipt_rate1 = individual[4] / 100
    receipt_rate2 = individual[5] / 100
    receipt_rate3 = individual[6] / 100
    efficiency_bonus = individual[7]
    five_day_mult = 1 + individual[8] / 100
    mile_threshold1 = individual[9] * 10
    mile_threshold2 = individual[10] * 10
    receipt_threshold1 = individual[11] * 10
    receipt_threshold2 = individual[12] * 10
    long_trip_threshold = int(individual[13])
    efficiency_low = individual[14] * 10
    efficiency_high = individual[15] * 10
    penalty_mult1 = individual[16] / 100
    penalty_mult2 = individual[17] / 100
    bonus_mult1 = individual[18] / 100
    bonus_mult2 = individual[19] / 100
    
    for days, miles, receipts, expected in cases:
        # Calculate reimbursement using evolved formula
        
        # Base calculation
        total = base_per_diem * days
        
        # 5-day bonus
        if days == 5:
            total *= five_day_mult
        
        # Mileage calculation (tiered)
        if miles <= mile_threshold1:
            mileage = miles * mile_rate1
        elif miles <= mile_threshold2:
            mileage = mile_threshold1 * mile_rate1 + (miles - mile_threshold1) * mile_rate2
        else:
            mileage = (mile_threshold1 * mile_rate1 + 
                      (mile_threshold2 - mile_threshold1) * mile_rate2 +
                      (miles - mile_threshold2) * mile_rate3)
        total += mileage
        
        # Receipt calculation (with thresholds)
        if receipts <= receipt_threshold1:
            receipt_reimb = receipts * receipt_rate1
        elif receipts <= receipt_threshold2:
            receipt_reimb = receipts * receipt_rate2
        else:
            receipt_reimb = receipts * receipt_rate3
        total += receipt_reimb
        
        # Efficiency bonus/penalty
        if days > 0:
            miles_per_day = miles / days
            if efficiency_low <= miles_per_day <= efficiency_high:
                total += efficiency_bonus
        
        # Long trip penalties
        if days >= long_trip_threshold:
            receipts_per_day = receipts / days if days > 0 else receipts
            if receipts_per_day > 150:
                total *= (1 - penalty_mult1)
        
        # Special combinations
        if days * miles > 5000 and receipts < 500:
            total *= (1 + bonus_mult1)
        
        # Calculate error
        error = abs(total - expected)
        total_error += error
    
    return (total_error,)

# Genetic operators
toolbox.register("evaluate", evaluate_formula)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=10, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Run genetic algorithm
print("Running Genetic Algorithm...")
print("=" * 60)

population = toolbox.population(n=100)
halloffame = tools.HallOfFame(1)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("min", np.min)

# Evolution
for gen in range(50):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.7, mutpb=0.3)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    
    population = toolbox.select(offspring, k=len(population))
    halloffame.update(population)
    
    if gen % 10 == 0:
        record = stats.compile(population)
        print(f"Generation {gen}: Min Error = ${record['min']:.0f}, Avg = ${record['avg']:.0f}")

# Get best individual
best_individual = halloffame[0]
best_fitness = best_individual.fitness.values[0]

print("\n" + "=" * 60)
print(f"Best fitness: ${best_fitness:.0f}")
print("\nBest gene values:")
gene_names = [
    "base_per_diem", "mile_rate1", "mile_rate2", "mile_rate3",
    "receipt_rate1", "receipt_rate2", "receipt_rate3", "efficiency_bonus",
    "five_day_mult", "mile_threshold1", "mile_threshold2", 
    "receipt_threshold1", "receipt_threshold2", "long_trip_threshold",
    "efficiency_low", "efficiency_high", "penalty_mult1", "penalty_mult2",
    "bonus_mult1", "bonus_mult2"
]

for i, (name, value) in enumerate(zip(gene_names, best_individual)):
    print(f"  {name}: {value:.2f}")

# Generate Python code from best individual
def generate_genetic_code(individual):
    """Generate Python code from the evolved formula"""
    
    # Extract and scale genes
    base_per_diem = individual[0]
    mile_rate1 = individual[1] / 100
    mile_rate2 = individual[2] / 100
    mile_rate3 = individual[3] / 100
    receipt_rate1 = individual[4] / 100
    receipt_rate2 = individual[5] / 100
    receipt_rate3 = individual[6] / 100
    efficiency_bonus = individual[7]
    five_day_mult = 1 + individual[8] / 100
    mile_threshold1 = individual[9] * 10
    mile_threshold2 = individual[10] * 10
    receipt_threshold1 = individual[11] * 10
    receipt_threshold2 = individual[12] * 10
    long_trip_threshold = int(individual[13])
    efficiency_low = individual[14] * 10
    efficiency_high = individual[15] * 10
    penalty_mult1 = individual[16] / 100
    penalty_mult2 = individual[17] / 100
    bonus_mult1 = individual[18] / 100
    bonus_mult2 = individual[19] / 100
    
    code = f"""def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    # Evolved formula from genetic algorithm
    days = trip_duration_days
    miles = miles_traveled
    receipts = total_receipts_amount
    
    # Base calculation
    total = {base_per_diem:.2f} * days
    
    # 5-day bonus
    if days == 5:
        total *= {five_day_mult:.3f}
    
    # Mileage calculation (tiered)
    if miles <= {mile_threshold1:.0f}:
        mileage = miles * {mile_rate1:.3f}
    elif miles <= {mile_threshold2:.0f}:
        mileage = {mile_threshold1:.0f} * {mile_rate1:.3f} + (miles - {mile_threshold1:.0f}) * {mile_rate2:.3f}
    else:
        mileage = ({mile_threshold1:.0f} * {mile_rate1:.3f} + 
                  ({mile_threshold2:.0f} - {mile_threshold1:.0f}) * {mile_rate2:.3f} +
                  (miles - {mile_threshold2:.0f}) * {mile_rate3:.3f})
    total += mileage
    
    # Receipt calculation
    if receipts <= {receipt_threshold1:.0f}:
        receipt_reimb = receipts * {receipt_rate1:.3f}
    elif receipts <= {receipt_threshold2:.0f}:
        receipt_reimb = receipts * {receipt_rate2:.3f}
    else:
        receipt_reimb = receipts * {receipt_rate3:.3f}
    total += receipt_reimb
    
    # Efficiency bonus
    if days > 0:
        miles_per_day = miles / days
        if {efficiency_low:.0f} <= miles_per_day <= {efficiency_high:.0f}:
            total += {efficiency_bonus:.2f}
    
    # Long trip penalties
    if days >= {long_trip_threshold}:
        receipts_per_day = receipts / days if days > 0 else receipts
        if receipts_per_day > 150:
            total *= {1 - penalty_mult1:.3f}
    
    # Special combinations
    if days * miles > 5000 and receipts < 500:
        total *= {1 + bonus_mult1:.3f}
    
    return round(total, 2)
"""
    
    return code

# Save the genetic algorithm solution
genetic_code = generate_genetic_code(best_individual)

with open('solution_genetic.py', 'w') as f:
    f.write("#!/usr/bin/env python3\n\n")
    f.write(genetic_code)

print("\nGenetic algorithm solution saved to solution_genetic.py")

# Also run a more aggressive genetic algorithm with larger population
print("\n" + "=" * 60)
print("Running aggressive genetic algorithm with larger population...")

# Increase population and generations
large_population = toolbox.population(n=500)
halloffame_large = tools.HallOfFame(5)  # Keep top 5

# Run for more generations
for gen in range(100):
    offspring = algorithms.varAnd(large_population, toolbox, cxpb=0.8, mutpb=0.4)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    
    large_population = toolbox.select(offspring, k=len(large_population))
    halloffame_large.update(large_population)
    
    if gen % 20 == 0:
        record = stats.compile(large_population)
        print(f"Generation {gen}: Min Error = ${record['min']:.0f}, Avg = ${record['avg']:.0f}")

# Check if we found a better solution
best_large = halloffame_large[0]
if best_large.fitness.values[0] < best_fitness:
    print(f"\nFound better solution! New best: ${best_large.fitness.values[0]:.0f}")
    
    # Save the better solution
    genetic_code_v2 = generate_genetic_code(best_large)
    with open('solution_genetic_v2.py', 'w') as f:
        f.write("#!/usr/bin/env python3\n\n")
        f.write(genetic_code_v2)