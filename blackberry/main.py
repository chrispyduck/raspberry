import sys, logging

if __name__ != "__main__":
    print('What are you doing?')
    sys.exit(1)
    
from blackberry.configuration.ConfigData import CurrentConfig
CurrentConfig.parseArgs()

logfile = logging.FileHandler(CurrentConfig.args.log)
logfile.setLevel(logging.DEBUG)
logfile.setFormatter(logging.Formatter('%(asctime)s %(module)s.%(funcName)s:%(levelname)s: %(message)s'))
logging.getLogger('').addHandler(logfile)

if CurrentConfig.args.debug:
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter('%(module)s.%(funcName)s:%(levelname)s: %(message)s'))
    logging.getLogger('').addHandler(console)
    
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

logger.info('Starting blackberry:')
logger.info(CurrentConfig.args)

from blackberry.Controller import Controller
instance = Controller()
instance.StartWithArgs()