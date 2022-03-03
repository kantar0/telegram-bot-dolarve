import logging

def start_logging():
    logging.basicConfig(filename='bot.log', format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO) # configuracion del logger
    logging.info('Logger started')
    

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_debug(message):
    logging.debug(message)

def log_warning(message):
    logging.warning(message)