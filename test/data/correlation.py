import csv
import numpy as np
import scipy.stats

noise_data = []
error_data = []
time_data = []

with open('example_spectre_old.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    start = False
    
    for row in spamreader:
        if not start:
            start = True
        else:
            noise_data.append(float(row[0].split(",")[0]))
            error_data.append(float(row[0].split(",")[1]))
            time_data.append(float(row[0].split(",")[2]))
print("Spectre noise vs error correlation - " + str(np.corrcoef(noise_data, error_data)[0,1]))
print("Spectre noise vs time correlation - " + str(np.corrcoef(noise_data, time_data)[0,1]))



noise_data2 = []
error_data2 = []
time_data2 = []
with open('noise_error_old.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    start = False
    
    for row in spamreader:
        if not start:
            start = True
        else:
            noise_data2.append(float(row[0].split(",")[0]))
            error_data2.append(float(row[0].split(",")[1]))
            time_data2.append(float(row[0].split(",")[2]))

print("P+P noise vs error correlation - " + str(np.corrcoef(noise_data2, error_data2)[0,1]))
print("P+P noise vs time correlation - " + str(np.corrcoef(noise_data2, time_data2)[0,1]))



