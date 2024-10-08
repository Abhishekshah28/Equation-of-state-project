import numpy as np
import csv

T = 373  # Kelvin
v = 0.0005  # m3
mole = 0.5
R = 8.314  # J/mol.k
Vm = v / mole
yi = np.array([0.05, 0.1, 0.05, 0.05, 0.1, 0.1, 0.1, 0.05, 0.15, 0.1, 0.1, 0.05])
Tci = np.array([190.6, 305.4, 370, 408.1, 425.1, 460.8, 469.6, 507.4, 540.6, 568.8, 595, 645])  # Corrected typo
Pci = np.array([4.6, 4.88, 4.3, 3.65, 3.8, 3.29, 3.37, 3.3, 2.74, 2.49, 2.3, 2.39])
w = np.array([0.0115, 0.099, 0.153, 0.183, 0.199, 0.227, 0.251, 0.299, 0.349, 0.398, 0.443])
Tr = T / Tci
betai = 0.25989 - 0.0217 * w + 0.00375 * w * w
eitai = 1 / (3 * (1 + (betai * w)))
print(eitai)
bi = betai * eitai * R * T / Pci
alpha = pow(1 + (0.48 + 1.574 * w - 0.176 * w * w) * (1 - pow(Tr, 0.5)), 2)

ai = pow((1 - eitai * (1 - betai)), 3) * R * R * Tci * Tci * alpha / (Pci)
b = sum(yi * bi)

k_data_file = open(r"k_data.csv", "r")
csv_reader = csv.reader(k_data_file)
k_data = []

for i in csv_reader:
    k_data.append([float(x) for x in i[1:]])  # Convert strings to float

k_data = k_data[1:]

a = 0
for i in range(0, 12):  # Corrected index starting from 0
    for j in range(i, 12):  # Corrected index starting from i
        tmp = yi[i] * yi[j] * ((ai[i] * ai[j]) ** 0.5) * (1 - float(k_data[i][j]))
        a += tmp

wa = sum(yi * w * pow(bi, 0.7))
wb = sum(yi * pow(bi, 0.7))

wab = wa / wb

# Corrected Peng-Robinson equation
P = (R * T / (Vm - b)) - (a / (Vm * Vm + (1 + 2 * wab) * b * Vm - (b * b * (1 - wab))))

print(P, "Pa")
