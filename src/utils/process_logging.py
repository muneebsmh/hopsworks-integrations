import logging
class process_logging:

    def process_log(self, logger_name, filename):
        logger = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        fileHandler = logging.FileHandler(filename, mode='a')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(fileHandler)
        logger.addHandler(streamHandler)
