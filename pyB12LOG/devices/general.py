import os
import pyvisa
from pyvisa.constants import Parity, StopBits
import datetime
from config.config import CONFIG
from configparser import ConfigParser

rm = pyvisa.ResourceManager()

class DEVICE:
    def __init__(self, debugLogger):
        deviceConfigDirHome = CONFIG['CONFIG']['log_folder_location'][1:-1]
        self.file_size = int(CONFIG['CONFIG']['save_file_size_kb']) * 1024
        self.deviceConfigDirFile = deviceConfigDirHome +'/B12TLOG_Config/device_config.cfg'
        self.deviceConfig = ConfigParser()

        self.commandConfigFile = deviceConfigDirHome +'/B12TLOG_Config/command.cfg'
        self.commandConfig = ConfigParser()

        self.logDir = deviceConfigDirHome + '/B12TLOG'

        self.debugLogger= debugLogger
        self.active_devices = []
        self.active_addresses = []
        self.query_items = []
        self.new_file = 1
        self.update_connect()
        self.log(new_file = 1)

    def update_connect(self):
        self.deviceConfig.read(self.deviceConfigDirFile)
        for address in rm.list_resources():
            if self.deviceConfig[address]['device_status'] == 'True' and address not in self.active_addresses:
                for item, val in self.deviceConfig[address].items():
                    exec("%s = %s" %(item, val), globals())
                try:
                    inst = rm.open_resource(device_address)
                    inst.baud_rate=baud_rate
                    inst.data_bits=data_bits
                    inst.flow_control=flow_control 
                    inst.parity=parity
                    inst.stop_bits=stop_bits
                    inst.read_termination = termination
                    inst.write_termination = termination
  
                    device_id = inst.query(id_command).strip('\r').strip('\n').strip()
                    
                    if not device_manufacturer or not model_number or not serial_number:
                        add_device_manufacturer = device_id.split(split_sign)[0]
                        add_model_number = device_id.split(split_sign)[1]
                        add_serial_number = device_id.split(split_sign)[2]
                        self.deviceConfig[address]['device_manufacturer'] = "'%s'" %add_device_manufacturer
                        self.deviceConfig[address]['model_number'] = "'%s'" %add_model_number
                        self.deviceConfig[address]['serial_number'] = "'%s'" %add_serial_number
                    
                    if address not in self.active_addresses:
                        self.new_file = 1
                        self.active_devices.append(inst)  
                        self.active_addresses.append(address)         
                
                except Exception as err:
                    self.deviceConfig[address]['device_status'] = 'False'
                    
                    if address in self.active_addresses:
                        self.new_file = 1
                        self.active_devices.remove(inst)
                        self.active_addresses.remove(address) 

                with open(self.deviceConfigDirFile, 'w') as conf:
                    self.deviceConfig.write(conf)

    def log(self, new_file = 0):
        self.update_connect()
        self.commandConfig.read(self.commandConfigFile)
        if new_file:
            for address in self.active_addresses:
                model_number = self.deviceConfig[address]['model_number'].replace("'", '')
                if model_number in self.commandConfig.keys():
                    for key in self.commandConfig[model_number]:
                        if key not in self.query_items:
                            self.query_items.append(key) 
            
            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #YYYYMMDDHMS
            self.logFile = self.logDir + '/' + 'log_' + now + '.csv'
            if self.query_items:
                with open(self.logFile, 'w') as f:
                    f.write('Date, Time, %s' %', '.join(self.query_items) + '\n')
                self.new_file = 0
        
        today = datetime.date.today()
        data = [str(today), str(datetime.datetime.now().strftime("%H:%M:%S"))]
        for index, (inst, address) in enumerate(zip(self.active_devices, self.active_addresses)):
            model = self.deviceConfig[address]['model_number'].replace("'", '')
            split_sign = self.deviceConfig[address]['split_sign'].replace("'", '')
            data_index = int(self.deviceConfig[address]['data_index'])
            if model in self.commandConfig.keys():
                # print(self.commandConfig[model]['voltage1'])
                for item, command in self.commandConfig[model].items():
                    try: 
                        data.append(inst.query(command).strip('\n').strip('\r').split(split_sign)[data_index])
                    except:
                        data.append(0)
                        self.new_file = 1
        with open(self.logFile, 'a') as f:
            f.write('%s' %', '.join(data) + '\n')
        
        if os.path.getsize(self.logFile) > self.file_size:
            self.new_file = 1             
            
            
    #     self.deviceRegDictStatus = False
    #     self.logDir = logDir
    #     self.deviceRegFile = self.logDir + '/device_reg.txt'
    #     self.debugLogger = debugLogger
    #     self.device_id = None

    #     if device_address in deviceRegDict: # check if device address is saved in device registration dictionary. The device address is the key.
    #         self.deviceRegDictStatus = True # because the device found, this value is set to True
    #         deviceInfo = deviceRegDict[device_address] # skip the 'Address' in the value
    #         index = 0
    #         for key in SEIRAL_CONFIG:
    #             for item, val in SEIRAL_CONFIG[key].items():
    #                 # print(item, deviceInfo[index])
    #                 try:
    #                     exec("self." + "%s = %s" %(item, deviceInfo[index]))
    #                 except:
    #                     exec("self." + "%s = '%s'" %(item, deviceInfo[index]))
    #                 index += 1
    #     else:
    #         # some default settings. They can be overwritten by 'deviceRegFile' if information exists.
    #         for key in SEIRAL_CONFIG:
    #             for item, val in SEIRAL_CONFIG[key].items():
    #                 exec("self." + "%s = %s" %(item, val)) # execute lines defined in config
            
    #     self.queryLogDict = {} # The log dictionary
    #     self.logDictStatus = False
        
    #     # splitter to split return strings
    #     self.splitter = ',' if self.split_sign.strip() == 'default' else self.split_sign.strip()

    #     self.connect(rm)
    #     self.categorize(COMMAND)

    #     self.fileSize = fileSize # the maximum saved file size.  
    #     self.log(init = 1) # only check when init
        
    # def connect(self, rm): 
    #     if self.deviceRegDictStatus and not self.device_status: # the device info is in device registration , and device is set to invalid (disable)
    #         return
    #     else:
    #         self.device = rm.open_resource(self.device_address) # open rm for valid device or unknown device
    #         self.setSerial()

    #     try:
    #         self.device_id = self.device.query(self.id_command).strip('\n').strip('\r') # try to check communication again
    #         self.device_status = True # device connected and device is valid
    #         print(self.device_address, 'Connected!')
    #         print(self.id_command, ': ', self.device_id)

    #     except Exception as err:
    #         self.debugLogger.info(err)
    #         self.debugLogger.warn('%s is not a valid device or need to change serial configuration' %self.device_address,)
        
    #     if not self.deviceRegDictStatus: # if device info is not in device registration, then save the new device info to registration
    #         if self.device_status and self.device_id:
    #             try:
    #                 self.device_manufacturer = self.device_id.split(self.splitter)[0]
    #                 self.model_number = self.device_id.split(self.splitter)[1]
    #                 self.serial_number = self.device_id.split(self.splitter)[2]
    #             except:
    #                 self.device_status, self.device_manufacturer, self.model_number, self.serial_number = False, None, None, None
    #                 self.debugLogger.warn('%s does not have a valid ID. Please update in device_reg.txt' %self.device_address)
            
    #         f = open(self.deviceRegFile, 'a')
    #         index = 0
    #         string = ''
    #         for key in SEIRAL_CONFIG:
    #             for item, val in SEIRAL_CONFIG[key].items():
    #                 if index == 0:
    #                     string += '{:^50}'.format(str(eval('self.' + item))) + ','
    #                 else:
    #                     string += '{:^25}'.format(str(eval('self.' + item))) + ','  
    #                 index += 1
    #         print(string[:-1], file = f)
    #         f.close()
                
    # def reconnect(self, rm):
    #     self.device = rm.open_resource(self.device_address)
    #     self.device.baud_rate = self.baud_rate
    #     self.setSerial()

    #     if self.device.query(self.id_command):
    #         self.device_status = True
    #         print(self.model_number, 'Reconnected!')
    #     else:
    #         self.device_status = False
    #         print(self.model_number, 'Reconnection Fails!')
    
    # def disconnect(self):
    #     self.device_status = False
    #     print(self.model_number, 'Disconnected!')


    # def categorize(self, COMMAND):
    #     if self.device_id:            
    #         try:
    #             for key, val in COMMAND[self.model_number].items():
    #                 self.queryLogDict[key.strip()] = val.strip()
    #             self.logDictStatus = True
    #         except Exception as err:
    #             self.debugLogger.warn(err)
    #             self.debugLogger.info('%s does not have config file.' %self.model_number)
    
    # def setSerial(self):
    #     self.setTermination()
    #     self.setParity()
    #     self.setStopBits()

    #     # other configurations
    #     self.device.flow_control = self.flow_control
    #     self.device.data_bits = self.data_bits
            
    # def setTermination(self):
    #     self.endSign = self.termination.replace('fl', '\n')
    #     self.endSign = self.endSign.replace('cr', '\r')
    #     self.device.write_termination = self.endSign
    #     self.device.read_termination = self.endSign
        
    # def setParity(self):
    #     '''
    #     even = 2
    #     mark = 3
    #     none = 0
    #     odd = 1
    #     space = 4
    #     '''

    #     if self.parity == 2:
    #         self.device.parity = Parity.even

    #     elif self.parity == 3:
    #         self.devive.parity = Parity.mark
        
    #     elif self.parity == 1:
    #         self.device.parity = Parity.odd

    #     elif self.parity == 4:
    #         self.device.parity = Parity.space

    #     elif self.parity == 0:
    #         self.device.parity = Parity.none

    #     else:
    #         self.debugLogger.info('Parity Incorrect')
    #         raise TypeError('Parity Incorrect')
    
    # def setStopBits(self):
    #     '''
    #     one = 10
    #     one_and_a_half = 15
    #     two = 20
    #     '''

    #     if self.stop_bits == 10:
    #         self.device.stop_bits = StopBits.one
    #     elif self.stop_bits == 15:
    #         self.device.stop_bits = StopBits.one_and_a_half
    #     elif self.stop_bits == 20:
    #         self.device.stop_bits = StopBits.two
    #     else:
    #         self.debugLogger.info('Stop bits Incorrect')
    #         raise TypeError('Stop bits Incorrect')

    # def log(self , init = 0):
    #     if self.device_id and self.logDictStatus and self.device_status:
    #         today = datetime.date.today()
    #         if init or self.createFile:
    #             now = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #YYYYMMDDHMS
    #             self.fileName = self.logDir + '/' + str(self.device_manufacturer) + '_' + str(self.model_number) + '_' + now + '.csv'
    #             f = open(self.fileName, 'a')
    #             print('Date, Time, ' + ', '.join(self.queryLogDict.keys()), file = f)
    #             f.close()
    #             self.createFile = False
            
    #         else:
    #             string = str(today) + ', ' + str(datetime.datetime.now().strftime("%H:%M:%S"))+ ', '
    #             f = open(self.fileName, 'a')
    #             try:
    #                 for command in self.queryLogDict.values():
    #                     string += (self.device.query(command).strip('\n').strip('\r').split(self.splitter)[self.data_index] + ', ')
    #                 string = string[:-2] # remove last commas
    #                 print(string, file = f)
    #             except Exception as err:
    #                 self.debugLogger.warn(err)
                
    #             f.close()

    #             if os.path.getsize(self.fileName) > self.fileSize:
    #                 self.createFile = True