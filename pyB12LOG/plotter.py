import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

f = open('./logs/2023_RIGOL TECHNOLOGIES_DP821A.csv', 'r')
header = f.readline().strip('\n').split(',')
items = f.readline().strip('\n').split(',')
info = f.readline().strip('\n').split(',')[1]
t = datetime.datetime.strptime(info.strip(), "%H:%M:%S").strftime("%H:%M:%S")
x = []
y = []
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

while(1):
    where = f.tell()
    line = f.readline().strip('\n')
    if not line:
        # time.sleep(1)
        f.seek(where)
        ax.clear()
        ax.plot(x, y, '#F37021')
        
    else:
        info = line.strip('\n').split(',')
        x.append(datetime.datetime.strptime(info[1].strip(), "%H:%M:%S").strftime("%H:%M:%S"))
        y.append(float(info[2].strip()))
        x = x[-20:]
        y = y[-20:]
        # plt.scatter(x, y, marker = '', color = '#F37021')   
    plt.pause(0.01)
    
plt.show()
        