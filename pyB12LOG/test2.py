from config.config import CONFIG
import os
if 'USER' in CONFIG:
    configKey = 'USER'

else:
    configKey = 'Default'

logDirHome = CONFIG[configKey]['log_folder_loc'][1:-1]
timeDelay = float(CONFIG[configKey]['acquire_interval'])

listDir = os.listdir(logDirHome)
logDir= logDirHome +'/logs/'
if 'logs' not in listDir:
    os.mkdir(logDir)


