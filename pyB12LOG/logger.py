from logger import pyB12LOG
log = pyB12LOG()
debugLogger = log.initDebugLog()
while(1):
    try:
        log.log()
    except Exception as err:
        debugLogger.info(err)
        log = pyB12LOG()