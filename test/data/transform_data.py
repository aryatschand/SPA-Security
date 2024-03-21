import csv

headers = []
data = []

with open('example_spectre_old.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    start = False
    
    for row in spamreader:
        if not start:
            for head in row[0].split(","):
                headers.append(head)
            start = True
        else:
            data.append(row[0].split(","))

with open('spectre_data.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["System","run","value","tag"])
    for x in range(0, len(data)):
        for y in range(0, len(headers)):
            point = [1,x+1,data[x][y],headers[y]]
            spamwriter.writerow(point)
