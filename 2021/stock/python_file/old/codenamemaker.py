import csv
from pprint import pprint


result = {}

f = open("code_and_name.csv", "r", encoding="utf-8")
rdr = csv.reader(f)
for line in rdr:

    result[line[0][1:]] = line[1]
f.close()

print(len(result))


print(len(a))
