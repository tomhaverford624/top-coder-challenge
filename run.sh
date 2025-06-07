#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>"
    exit 1
fi

# Assign arguments to variables
trip_duration_days=$1
miles_traveled=$2
total_receipts_amount=$3

# Call the Python script with the arguments
python reimbursement_calculator.py "$trip_duration_days" "$miles_traveled" "$total_receipts_amount"
