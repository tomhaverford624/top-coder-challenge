#!/bin/bash

# Input parameters
trip_duration_days=$1
miles_traveled=$2
total_receipts_amount=$3

# Python script to calculate reimbursement using decision tree
python3 << EOF
trip_duration_days = $trip_duration_days
miles_traveled = $miles_traveled
total_receipts_amount = $total_receipts_amount

# Calculate derived features
miles_per_day = miles_traveled / trip_duration_days if trip_duration_days > 0 else 0
receipts_per_day = total_receipts_amount / trip_duration_days if trip_duration_days > 0 else 0
receipts_per_mile = total_receipts_amount / miles_traveled if miles_traveled > 0 else 0
days_x_miles = trip_duration_days * miles_traveled
days_x_receipts = trip_duration_days * total_receipts_amount
miles_x_receipts = miles_traveled * total_receipts_amount

# Decision tree logic (score: 7778!)
if total_receipts_amount <= 828.10:
    if days_x_miles <= 2070.00:
        if days_x_receipts <= 487.54:
            if days_x_miles <= 566.00:
                if days_x_miles <= 210.50:
                    total = 196.57
                else:  # days_x_miles > 210.50
                    total = 336.31
            else:  # days_x_miles > 566.00
                total = 559.32
        else:  # days_x_receipts > 487.54
            if days_x_receipts <= 4036.29:
                if days_x_miles <= 1310.50:
                    if total_receipts_amount <= 588.27:
                        if trip_duration_days <= 4.50:
                            total = 492.73
                        else:  # trip_duration_days > 4.50
                            total = 619.95
                    else:  # total_receipts_amount > 588.27
                        total = 719.40
                else:  # days_x_miles > 1310.50
                    if days_x_receipts <= 1467.28:
                        total = 700.75
                    else:  # days_x_receipts > 1467.28
                        total = 828.74
            else:  # days_x_receipts > 4036.29
                total = 935.06
    else:  # days_x_miles > 2070.00
        if days_x_miles <= 4945.50:
            if total_receipts_amount <= 570.45:
                if days_x_receipts <= 1790.10:
                    if days_x_miles <= 3963.60:
                        if receipts_per_mile <= 0.41:
                            total = 750.44
                        else:  # receipts_per_mile > 0.41
                            total = 788.25
                    else:  # days_x_miles > 3963.60
                        total = 845.60
                else:  # days_x_receipts > 1790.10
                    if miles_traveled <= 628.50:
                        if receipts_per_mile <= 1.11:
                            total = 925.07
                        else:  # receipts_per_mile > 1.11
                            total = 853.04
                    else:  # miles_traveled > 628.50
                        total = 1000.77
            else:  # total_receipts_amount > 570.45
                if total_receipts_amount <= 691.05:
                    total = 1019.89
                else:  # total_receipts_amount > 691.05
                    total = 1170.65
        else:  # days_x_miles > 4945.50
            if miles_x_receipts <= 529812.36:
                if trip_duration_days <= 10.50:
                    if days_x_receipts <= 2838.70:
                        if receipts_per_mile <= 0.18:
                            total = 1111.45
                        else:  # receipts_per_mile > 0.18
                            total = 1042.71
                    else:  # days_x_receipts > 2838.70
                        total = 1208.17
                else:  # trip_duration_days > 10.50
                    if days_x_miles <= 11460.50:
                        if miles_x_receipts <= 218691.81:
                            total = 1213.97
                        else:  # miles_x_receipts > 218691.81
                            total = 1298.64
                    else:  # days_x_miles > 11460.50
                        total = 1364.90
            else:  # miles_x_receipts > 529812.36
                if days_x_receipts <= 5526.72:
                    total = 1417.53
                else:  # days_x_receipts > 5526.72
                    total = 1611.04
else:  # total_receipts_amount > 828.10
    if days_x_miles <= 3873.00:
        if days_x_receipts <= 5494.43:
            if miles_x_receipts <= 385934.73:
                if total_receipts_amount <= 1082.07:
                    if days_x_receipts <= 3208.57:
                        total = 949.66
                    else:  # days_x_receipts > 3208.57
                        total = 1099.06
                else:  # total_receipts_amount > 1082.07
                    total = 1239.56
            else:  # miles_x_receipts > 385934.73
                if miles_x_receipts <= 1033628.09:
                    if days_x_receipts <= 2736.24:
                        if miles_x_receipts <= 827348.03:
                            total = 1176.45
                        else:  # miles_x_receipts > 827348.03
                            total = 1261.61
                    else:  # days_x_receipts > 2736.24
                        if total_receipts_amount <= 942.36:
                            total = 1288.02
                        else:  # total_receipts_amount > 942.36
                            total = 1376.78
                else:  # miles_x_receipts > 1033628.09
                    if days_x_miles <= 1205.00:
                        if receipts_per_mile <= 1.77:
                            total = 1294.13
                        else:  # receipts_per_mile > 1.77
                            total = 1408.36
                    else:  # days_x_miles > 1205.00
                        if miles_per_day <= 406.00:
                            total = 1495.94
                        else:  # miles_per_day > 406.00
                            total = 1526.97
        else:  # days_x_receipts > 5494.43
            if days_x_receipts <= 11625.58:
                if days_x_miles <= 979.83:
                    if days_x_receipts <= 9327.43:
                        total = 1270.85
                    else:  # days_x_receipts > 9327.43
                        total = 1406.93
                else:  # days_x_miles > 979.83
                    if miles_traveled <= 518.50:
                        if days_x_miles <= 2578.00:
                            total = 1496.66
                        else:  # days_x_miles > 2578.00
                            total = 1336.63
                    else:  # miles_traveled > 518.50
                        if receipts_per_day <= 624.27:
                            total = 1653.03
                        else:  # receipts_per_day > 624.27
                            total = 1498.03
            else:  # days_x_receipts > 11625.58
                if trip_duration_days <= 12.50:
                    if receipts_per_mile <= 6.38:
                        total = 1664.33
                    else:  # receipts_per_mile > 6.38
                        if trip_duration_days <= 8.50:
                            total = 1528.26
                        else:  # trip_duration_days > 8.50
                            total = 1605.61
                else:  # trip_duration_days > 12.50
                    total = 1714.87
    else:  # days_x_miles > 3873.00
        if days_x_miles <= 6939.00:
            if total_receipts_amount <= 1089.04:
                total = 1476.82
            else:  # total_receipts_amount > 1089.04
                if miles_per_day <= 99.75:
                    if trip_duration_days <= 10.50:
                        if miles_x_receipts <= 1229175.00:
                            total = 1636.17
                        else:  # miles_x_receipts > 1229175.00
                            total = 1521.96
                    else:  # trip_duration_days > 10.50
                        if receipts_per_day <= 169.39:
                            total = 1795.96
                        else:  # receipts_per_day > 169.39
                            total = 1702.51
                else:  # miles_per_day > 99.75
                    if trip_duration_days <= 5.50:
                        if miles_traveled <= 1030.50:
                            total = 1736.47
                        else:  # miles_traveled > 1030.50
                            total = 1659.12
                    else:  # trip_duration_days > 5.50
                        if trip_duration_days <= 6.50:
                            total = 1778.50
                        else:  # trip_duration_days > 6.50
                            total = 1860.13
        else:  # days_x_miles > 6939.00
            if days_x_miles <= 11863.00:
                if miles_per_day <= 127.34:
                    if miles_x_receipts <= 877176.88:
                        total = 1742.71
                    else:  # miles_x_receipts > 877176.88
                        if receipts_per_day <= 174.05:
                            total = 1906.01
                        else:  # receipts_per_day > 174.05
                            total = 1800.23
                else:  # miles_per_day > 127.34
                    if days_x_receipts <= 12912.54:
                        total = 2048.61
                    else:  # days_x_receipts > 12912.54
                        total = 1857.20
            else:  # days_x_miles > 11863.00
                if total_receipts_amount <= 1787.72:
                    if miles_traveled <= 1017.50:
                        total = 1988.28
                    else:  # miles_traveled > 1017.50
                        total = 2136.03
                else:  # total_receipts_amount > 1787.72
                    total = 1924.59

print(f"{total:.2f}")
EOF