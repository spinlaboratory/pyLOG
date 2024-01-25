'''
This is debug log class for logger

Author: Yen-Chun Huang

Company: Bridge 12 Technologies. Inc
'''

import logging

class debugLog:
    def __init__(self, log_dir: str):

        logpath = log_dir + '/debug_log.txt'
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler(str(logpath))
        ch.setLevel(logging.INFO)
        ch2 = logging.StreamHandler()
        ch2.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        ch2.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(ch2)

        return logger