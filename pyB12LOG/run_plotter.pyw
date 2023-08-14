'''
This is the python program to run plotter only 
'''

import os
import sys
from collections import Counter
import argparse
from .plotter import *

def main_func():
    parser = argparse.ArgumentParser(prog='pyB12plotter')
    parser.add_argument('number_of_file', type=int, nargs='?', default = 100, 
                        help='To select number of files to plot in real-time')
    args = parser.parse_args()
    current_exe = os.popen('wmic process get description').read().strip().replace(' ', '').split('\n\n')
    hashDict = Counter(current_exe) 
    if 'pyB12plotter.exe' in hashDict and hashDict['pyB12plotter.exe'] > 1:
        exit()
    else:
        fig = plotter(number_of_file = args.number_of_file)

if __name__ == "__main__":
    main_func()