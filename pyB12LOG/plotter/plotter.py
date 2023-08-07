import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime

class plotter:
    def __init__(self, log):
        self.logDir = log
        self.header = None
        self.items = None
        self.hashDict = None
        self.f = None
        
        self.logRead()
    
    def logRead(self):
        self.f = open(self.log, 'r')
        self.items = self.f.readline().strip('\n').split(',')
        self.hashDict ={x.strip(): [] for x in self.items}
        
        for info in csv.reader(self.f, delimiter = ','): # O(1)
            self.hashDict = self.hashDict_append(info, self.hashDict) # O(n)

    def hashDict_append(self, info, hashDict):
        for index, key in enumerate(hashDict.keys()):
            if key == 'Date':
                val = info[index]
            elif key == 'Time':
                val = info[index].strip() # not necessary to convert string to time in plotting
            else:
                val = float(info[index])
            
            hashDict[key].append(val)
        return hashDict
    
    def plot(self, items, duration):
        # take care of pnts to plot
        delta = datetime.datetime.strptime(self.hashDict['Time'][-1], '%H:%M:%S') - datetime.datetime.strptime(self.hashDict['Time'][-5], '%H:%M:%S')
        pnts = int(duration//delta.total_seconds() * 5)
        
        # init common x-axis
        x_label = [self.hashDict['Time'][-pnts:][i] if i in [0,pnts/2, pnts-1] else '' for i in range(pnts)]
        x = [i for i in range(1, pnts + 1)]
        
        # init figure
        fig = plt.figure(1)
        ax = fig.add_subplot(1,1,1)
        update_require = 1

        # init y-axis
        ys = [self.hashDict[item][-pnts:] for item in items]
        color_lists = ['#F37021', '#46812B', '#4D4D4F', '#A7A9AC']

        while(plt.fignum_exists(1)):

            # where = f.tell() # (option) f current position of pointer
            line = self.f.readline().strip('\n')
            if line: # if there is non-empty new line
                self.hashDict_append(line.strip('\n').split(','), self.hashDict)
                x_label = [self.hashDict['Time'][-pnts:][i] if i in [0,pnts/2,pnts-1] else '' for i in range(pnts)]
                ys = [self.hashDict[item][-pnts:] for item in items]
                update_require = 1

            else: # if there is no line
                if update_require:
                    # f.seek(where) # (option) find current pointer
                    ax.clear()
                    # ax.locator_params(nbins = 5)
                    ax.set_xticks(x, x_label)
                    # ax.grid(ls = ':')
                    for index, (y, color) in enumerate(zip(ys, color_lists)):
                        ax.plot(x, y, color, label = items[index])

                    ax.legend()
                    update_require = 0
        

            plt.pause(0.01) # showing new plot
    
        plt.show()