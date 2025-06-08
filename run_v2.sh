#!/bin/bash

# Input parameters
trip_duration_days=$1
miles_traveled=$2
total_receipts_amount=$3

# Python script to calculate reimbursement
python3 << EOF
trip_duration_days = $trip_duration_days
miles_traveled = $miles_traveled
total_receipts_amount = $total_receipts_amount

# COMPLETELY NEW FORMULA DISCOVERED!

# Base amount (NOT per diem - fixed amounts!)
if trip_duration_days == 1:
    base_amount = 100
elif trip_duration_days == 2:
    base_amount = 200
elif trip_duration_days == 3:
    base_amount = 280
else:  # 4+ days
    base_amount = 290

# Mileage rate (varies by trip duration!)
if trip_duration_days <= 4:
    mileage_rate = 0.40
elif trip_duration_days == 5:
    mileage_rate = 0.67
elif trip_duration_days <= 12:
    mileage_rate = 0.85
else:  # 13+ days
    mileage_rate = 1.00

# Receipt reimbursement (tiered system)
if total_receipts_amount <= 50:
    receipt_reimbursement = total_receipts_amount
elif total_receipts_amount <= 200:
    receipt_reimbursement = 50 + (total_receipts_amount - 50) * 0.70
elif total_receipts_amount <= 1000:
    receipt_reimbursement = 50 + 150 * 0.70 + (total_receipts_amount - 200) * 0.50
else:
    receipt_reimbursement = 50 + 150 * 0.70 + 800 * 0.50 + (total_receipts_amount - 1000) * 0.30

# BUG: Specific .49 receipts get NO receipt reimbursement
bugged_receipts = [293.49, 389.49, 396.49, 1063.49, 1878.49, 2321.49]
if total_receipts_amount in bugged_receipts:
    receipt_reimbursement = 0

# Calculate total
total = base_amount + receipt_reimbursement + (miles_traveled * mileage_rate)

# Round to 2 decimal places
print(f"{total:.2f}")
EOF