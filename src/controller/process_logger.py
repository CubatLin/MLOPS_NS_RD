import logging
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, path, cmd_level="debug", file_level="debug"):

        """
        1. path: save path of log file
        2. level:
            DEBUG:
                Detailed information, typically of interest only when diagnosing problems.
            INFO:
                Confirmation that things are working as expected.
            WARNING:
                An indication that something unexpected happened, or indicative of some problem
                in the near future(e.g. ‘disk space low’). The software is still working as expected.
            ERROR:
                Due to a more serious problem, the software has not been able to perform some function.
            CRITICAL:
                A serious error, indicating that the program itself may be unable to continue running.

        Demo Code:
            root = Logger(path='../Log/test_log.log', cmd_level='error', file_level='debug')
            root.debug('一個 debug 的 log')
            root.info('一個 info 的 log')
            root.warn('一個 warning 的 log')
            root.error('一個 error 的 log')
            root.critical('一個 critical 的 log')
            
        Test Case:
            root = Logger(path='test_log.log', cmd_level='error', file_level='debug')
            try:
                x = 5 / 0
            except:
                root.debug('Catch an exception.\n')
                root.info('Catch an exception.\n')
                root.warn('Catch an exception.\n')
                root.error('Catch an exception.\n')
                root.critical('Catch an exception.\n')    
        """
        log_level_mapping_table = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }

        # Note: multiple calls to getLogger() with the same name will always return a reference to the same Logger object.
        self.logger = logging.getLogger(name=path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # cmd log
        stream_handler = logging.StreamHandler() # cmd要輸出的level
        stream_handler.setFormatter(fmt)
        stream_handler.setLevel(log_level_mapping_table[cmd_level])
        self.logger.addHandler(stream_handler)

        # file log
        rotating_file_handler = RotatingFileHandler(
            path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        rotating_file_handler.setFormatter(fmt)
        rotating_file_handler.setLevel(log_level_mapping_table[file_level])
        self.logger.addHandler(rotating_file_handler)

    def debug(self, message):
        self.logger.debug(message, exc_info=True)

    def info(self, message):
        self.logger.info(message, exc_info=True)

    def warn(self, message):
        self.logger.warn(message, exc_info=True)

    def error(self, message):
        self.logger.error(message, exc_info=True)

    def critical(self, message):
        self.logger.critical(message, exc_info=True)