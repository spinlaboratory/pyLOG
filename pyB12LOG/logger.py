from logger import pyB12LOG
            
log = pyB12LOG(timeDelay = 1)
while(1):
    try:
        log.log()
    except Exception as err:
        log = pyB12LOG(timeDelay = 1)

