import csv

mas = []
with open('locations.list', 'r', encoding='ISO-8859-1') as file:
    cnt = 1
    for line in file.readlines():
        cnt += 1
        if cnt % 20:
            continue
        if len(line.split(',')) < 4 or '}' in line:
            continue
        year = line.split('(')[1][:4]
        name = line.split('(')[0].strip()
        sth = line.split(',')[:-1]
        sth[0] = sth[0].split(')')[-1]
        if not year.isnumeric():
            continue
        address = ""
        for i in sth:
            if '"' in i or '(' in i or ',' in i:
                continue
            address += i.strip() + " "
        mas.append((year, name, address))

f = open("loc10000.csv", 'w')
for i in mas:
    f.write(i[0] + ',' + i[1] + ',' + i[2] + '\n')

