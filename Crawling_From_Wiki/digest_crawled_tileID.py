import csv

with open(input("File : "), "r") as f:
    reader = csv.reader(f)
    rows = [*reader]

print(rows)

with open("code.txt", "w") as f:
    for row in rows:
        if row[-1]:
            f.write(f"    {row[-1]} = {int(row[0])}\n")

#Somehow Pearlstone is assigned as both number 117 and 118.