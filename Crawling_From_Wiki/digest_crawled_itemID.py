import csv

with open(input("File : "), "r") as f:
    reader = csv.reader(f)
    rows = [*reader]

print(rows)

with open("code.txt", "w") as f:
    for row in rows:
        try:
            f.write(f"    {row[-1]} = {int(row[0])}\n")
        except ValueError:
            pass