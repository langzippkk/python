"""
Create a sorted list of results:

>>> result = sum_debt_by_date('indebtedness.csv')
>>> result_list = list(sorted(result.items()))

Show the 10 oldest entries:

>>> for k, v in result_list[:10]:
...     print("{}:    ${:>,.2f}".format(k, v))
...
2011-10-14:    $2,553,610.00
2011-10-21:    $2,326,302.00
2011-10-28:    $2,132,597.00
2011-11-04:    $1,950,591.00
2011-11-11:    $1,810,242.00
2011-11-18:    $1,741,137.00
2011-11-25:    $1,702,319.00
2011-12-02:    $1,671,228.00
2011-12-09:    $1,648,081.00
2011-12-16:    $1,560,820.00

Show the 10 most recent entries:

>>> for k, v in result_list[-10:]:
...     print("{}:    ${:>,.2f}".format(k, v))
...
2018-01-06:    $3,741,679.92
2018-01-13:    $3,733,799.43
2018-01-27:    $3,496,082.28
2018-02-10:    $3,465,350.41
2018-02-17:    $5,546,558.46
2018-02-24:    $5,436,037.23
2018-03-03:    $5,209,381.37
2018-03-10:    $5,012,478.96
2018-03-17:    $4,873,168.65
2018-03-24:    $4,740,987.36
"""

import csv
from datetime import datetime
# convert datetime

def sum_debt_by_date(data_entries):
    with open(data_entries, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        d = {}
        for row in readCSV:
            if len(row[6]) < 1:
                continue
            name = row[0]
            name = datetime.strptime(name, '%M/%d/%Y').strftime('%Y-%M-%d')
            value = round(float(row[6][1:len(row[6])]), 2)
            if name not in d.keys():
                d[name] = value
            else:
                temp = round(float(d[name] + value), 2)
                d[name] = temp
    return d

print(sum_debt_by_date('indebtedness.csv'))
