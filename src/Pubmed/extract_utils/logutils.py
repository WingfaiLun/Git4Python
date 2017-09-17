'''
Created on 2017-09-10

@author: lockon
'''
import logging
from datetime import datetime

# define the script global logger
def strd_logger (loggerName, logFileName = "basic_logger.log"):
    log = logging.getLogger (loggerName)
    log.setLevel (logging.INFO)
    formatter = logging.Formatter('[%(asctime)s.%(msecs)d %(levelname)s] %(message)s','%Y-%m-%d,%H:%M:%S')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)    
    log.addHandler(streamHandler)
    fileHandler = logging.FileHandler(logFileName)
    fileHandler.setFormatter(formatter)
    log.addHandler(fileHandler)
    return log

# Define the script global logger
def ext_print (name):
    tnow = datetime.now()
    name = '[' + str(tnow) + '] ' + name
    return name