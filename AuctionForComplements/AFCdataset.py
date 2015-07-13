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
plnum =  5
Round =  3

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
    if plnum % 3 == 0:
        for i in range(plnum/3):
            values[0].append(random.randint(0, 100))
        for i in range(plnum/3, 2*plnum/3):
            values[1].append(random.randint(0, 100))
        for i in range(2*plnum/3, plnum):
            values[2].append(random.randint(0, 200))
    elif plnum % 3 == 1:
        for i in range((plnum-1)/3 + 1):
            values[0].append(random.randint(0, 100))
        for i in range((plnum-1)/3 + 1, 2*(plnum-1)/3 + 1):
            values[1].append(random.randint(0, 100))
        for i in range(2*(plnum-1)/3 + 1, plnum):
            values[2].append(random.randint(0, 200))
    else:
        for i in range((plnum-2)/3 + 1):
            values[0].append(random.randint(0, 100))
        for i in range((plnum-2)/3 + 1, 2*(plnum-2)/3 + 2):
            values[1].append(random.randint(0, 100))
        for i in range(2*(plnum-2)/3 + 2, plnum):
            values[2].append(random.randint(0, 200))
    data1.append(values[0])
    data2.append(values[1])
    data3.append(values[2])

csvWriter1.writerows(data1)
csvWriter2.writerows(data2)
csvWriter3.writerows(data3)

f1.close()
f2.close()
f3.close()
