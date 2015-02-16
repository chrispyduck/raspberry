import sys, logging, traceback, string

def main():
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
    
    if CurrentConfig.args.writeconfig:
        CurrentConfig.save(CurrentConfig.args.writeconfig)
        sys.exit(0)
    
    logger.info('Starting blackberry:')
    logger.info(CurrentConfig.args)
    
    def exceptionHandler(exctype, value, tb):
        logger.fatal(string.join(traceback.format_exception(exctype, value, tb)))
        sys.__excepthook__(exctype, value, tb)
    sys.excepthook = exceptionHandler
    
    from blackberry.Controller import Controller
    instance = Controller()
    
    if CurrentConfig.args.debug:
        instance.run()
    else:
        instance.start()
        
if __name__ == "__main__":
    main()