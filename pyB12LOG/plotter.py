import numpy as np
import matplotlib.pyplot as plt
import csv

def hashDict_append(info, hashDict):
    for index, key in enumerate(hashDict.keys()):
        if key == 'Date':
            val = info[index]
        elif key == 'Time':
            val = info[index].strip() # not necessary to convert string to time in plotting
        else:
            val = float(info[index])
        
        hashDict[key].append(val)

f = open('./logs/2023_RIGOL TECHNOLOGIES_DP821A.csv', 'r')
header = f.readline().strip('\n').split(',')
items = f.readline().strip('\n').split(',')
hashDict ={x.strip(): [] for x in items}
current_info = csv.reader(f, delimiter = ',') # O(1)
for info in current_info:
    hashDict_append(info, hashDict) # O(n)

x_label = [hashDict['Time'][-20:][i] if i in [0,10,19] else '' for i in range(20)]
x = [i for i in range(1, 20 + 1)]
y = hashDict['voltage1'][-20:] 
fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
ax.grid(ls = ':')
update_require = 1

while(plt.fignum_exists(1)):
    # where = f.tell() # (option) f current position of pointer
    line = f.readline().strip('\n')
    if line: # if there is non-empty new line
        hashDict_append(line.strip('\n').split(','), hashDict)
        x_label = [hashDict['Time'][-20:][i] if i in [0,10,19] else '' for i in range(20)]
        y = hashDict['voltage1'][-20:]
        update_require = 1

    else: # if there is no line
        if update_require:
            # f.seek(where) # (option) find current pointer
            ax.clear()
            ax.set_xticks(x, x_label)
            ax.grid(ls = ':')
            ax.plot(x, y, '#F37021')
            update_require = 0
        

    plt.pause(0.01) # showing new plot
    
plt.show()