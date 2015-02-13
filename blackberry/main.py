import sys, logging

if __name__ != "__main__":
    print('What are you doing?')
    sys.exit(1)
    
from blackberry.configuration.ConfigData import CurrentConfig
CurrentConfig.parseArgs()

logging.basicConfig(filename=CurrentConfig.args.log, level=logging.DEBUG, format='%(asctime)s %(module)s.%(funcName)s %(levelname)s: %(message)s')
logging.info('Starting blackberry:')
logging.info(CurrentConfig.args)

from blackberry.Controller import Controller
instance = Controller()

if CurrentConfig.args.debug:
    instance.run()
else:
    instance.start()