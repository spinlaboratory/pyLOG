"""
pyB12LOG: The logging program for instrumentations

pyB12LOG: read configurations, get available devices, send command and save return.

Author: Yen-Chun Huang

Company: Bridge 12 Technologies, Inc
"""

from .device import *
import time
import os
from .loggerConfig import *
from .debugLog import *

class pyB12LOG:
    def __init__(self, config_file: str = None):
        
        config = loggerConfig(config_file)
        settings = config.settings 
        commands = config.commands # dictionary {model: {variable: {command, alias, min, max, static}}}
        device_config = config.devices
        
        self.log_dir = settings['log_folder_location'] + '/B12TLOG/'
        self.delay = int(settings['log_interval'])
        self.max_size = int(settings['save_file_size_kb'])
        
        self._checkDirectory()
        self.last_query_time = None
        self.devices = DEVICE(device_config) # establish communication 
        self.data_by_variable = self._getDataDictByVariable(commands) # initial empty dictionary for storing data
        
        self.header = self._makeLogHeader()
        self._createNewLog()
        while (1):
            self.log(commands, device_config)
    
    def log(self, commands, device_config):
        now = time.time()

        if not self.last_query_time or now - self.last_query_time > self.delay:

            devices_info = self.devices.devices_info # dictionary: {model: {status, config_status, device, id_command}}
            for name, info in commands.items():
                delimiter = device_config[name]['delimiter']
                index = device_config[name]['index']
                device = devices_info[name]['device']
                for variable in info.keys():
                    if self.devices.checkDeviceStatus(name): # check the connection of a device
                        command = info[variable]['command']
                        data_string = device.query(command)
                        data = self._returnStringConverter(data_string, delimiter, index)
                    
                    else:
                        data = 'nan' # write nan to not available data

                    self.data_by_variable[variable] = data
            
            self.last_query_time = now
            
            if self._checkFileSize(): # exceed the maximum file size
                self._createNewLog() # create log with header

            self._saveData()

    def _checkDirectory(self):
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
            return False
        return True
    
    def _createNewLog(self):
        '''
        Create new log file in log directory
        '''
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #YYYYMMDDHMS
        self.current_log_file = self.log_dir + '/log_' + now + '.csv'
        with open(self.current_log_file, 'w') as f:
            f.write(self.header)

        return True

    def _makeLogHeader(self):
        '''
        Make a log header base on the data by variable dictionary

        Return:
            header (str) format: 'Date, Time, variable 1, variable 2.....'
        '''   
        list_of_items = list(self.data_by_variable.keys())
        header = ', '.join(list_of_items) + '\n'

        return header
    
    def _saveData(self):
        '''
        Save current data to current log file

        '''

        list_of_data = list(self.data_by_variable.values())
        data_string = ', '.join(list_of_data) + '\n'
        
        with open(self.current_log_file, 'a') as f:
            f.write(data_string)

        return True
    
    def _checkFileSize(self):
        '''
        Check the size of file

        Return:
            bool: True if file is oversize
        '''      
        if os.path.getsize(self.current_log_file) > self.max_size * 1024:
            return True
        else:
            return False


    def _getDataDictByVariable(self, command_dict: dict):
        '''
        Get the variable list based on the model and it's command dictionary 
        Args:
            command_dict (dict): the command list for a device, {variable: {command, alias, min, max, static}}

        Returns:
            data_dict (dict): the data dictionary in format {variable: reading}

        '''
        today = str(datetime.date.today())
        now = str(datetime.datetime.now().strftime("%H:%M:%S"))
        data_dict = {'Date': today, 'Time': now}
        for info in command_dict.values():
           temp_dict = {key : None for key in info}
           data_dict = {**data_dict, **temp_dict}

        return data_dict
    
    def _returnStringConverter(self, string: str, delimiter: str, index: int):
        '''
        Convert returned string and acquire data from it
        Args:
            delimiter (str): the delimiter for string analysis
            index (int): the data index

        Returns:
            data (string): return data in str
        '''
        string.replace(' ', '') # remove white space
        string.replace('\n', '') # remove cr
        string.replace('\t', '') # remove fl
        data = string.split(delimiter)[index]

        return data

    
        # while(1):
            # print(self.devices.devices_status['437B']['device'].query('*IDN?'))
        
        # if time.time() - self.lastCheckTime > self.timeDelay:
        #     self.logStartTime = time.time()
        #     self.device.log()
        #     self.lastCheckTime = time.time()
        #     self.logDeltaTime = self.lastCheckTime - self.logStartTime
            
        #     if self.firstLog:
        #         self.debugLogger.info('Log interval of %0.1f s. Logging takes %0.1f s to complete.' %(self.timeDelay, self.logDeltaTime))
        #         self.firstLog = False
        #     if self.logDeltaTime > self.timeDelay:
        #         self.debugLogger.info('Log interval of %0.1f s is too short. Logging takes %0.1f s to complete. Log interval is set to %0.1f s.' %(self.timeDelay, self.logDeltaTime, self.logDeltaTime + 0.1))
        #         self.timeDelay = self.logDeltaTime + 0.1

if __name__ == '__main__':
    pyB12LOG()