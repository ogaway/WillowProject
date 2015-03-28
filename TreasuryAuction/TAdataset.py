# coding: UTF-8
import csv
import random

"""
Create DataSets
---
you should create datasets to compare the results of each auction design.

Before using this program,
you should check that the folder named "data" is empty.
If the "data" folder is not empty,
datasets updated by using this program may be unuseful.

you can change the variables
"plnum": the number of the participants.
"Round": the number of the round

"""

# You can change the variables
plnum = 2
Round = 2

f1 = open('data/data1.csv', 'ab')
f2 = open('data/data2.csv', 'ab')
f3 = open('data/data3.csv', 'ab')

csvWriter1 = csv.writer(f1)
csvWriter2 = csv.writer(f2)
csvWriter3 = csv.writer(f3)

data1 = []
data2 = []
data3 = []

for i in range(Round):
    values = [[], [], []]
    value = random.randint(1000, 5000)
    estimates = []
    for i in range(plnum):
        estimate = random.randint(value-200, value+200)
        estimates.append(estimate)
    for i in range(3):
        random.shuffle(estimates)
        values[i].append(value)
        values[i].extend(estimates)
    data1.append(values[0])
    data2.append(values[1])
    data3.append(values[2])
random.shuffle(data1)
random.shuffle(data2)
random.shuffle(data3)

csvWriter1.writerows(data1)
csvWriter2.writerows(data2)
csvWriter3.writerows(data3)

f1.close()
f2.close()
f3.close()
