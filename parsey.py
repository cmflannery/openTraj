import csv
import os

path = os.path.join(os.getcwd(), 'atmosTable.txt')
path2 = os.path.join(os.getcwd(), 'atmosData.csv')
with open(path) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)
print(d[1])

with open(path2, 'w') as csvfile:
    dataWriter = csv.writer(csvfile, delimiter=',', quotechar='|')
    for i in range(0, len(d[:][1])-1):
        dataWriter.writerow(d[i][:])
