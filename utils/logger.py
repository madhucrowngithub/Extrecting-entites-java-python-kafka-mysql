# -*- coding: utf-8 -*-
#
import sys
import logging.handlers
import platform
from logging import FileHandler, LogRecord
from datetime import datetime
from utils.cfg import Cfg

class HostnameFilter(logging.Filter):
    hostname = platform.node()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True

logger_initialized = False
def init():
    global logger_initialized
    if logger_initialized:
        return
    logger_initialized = True
    
    root_logger= logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
            'logs/trace.log', maxBytes=50 * 1024 * 1024, 
            backupCount=3, encoding='utf-8')
    handler.setFormatter(logging.Formatter(
            '%(levelname)s %(threadName)s %(asctime)s %(filename)s:%(lineno)d %(funcName)s %(message)s'))
    root_logger.addHandler(handler)
    root_logger.addHandler(logging.StreamHandler(sys.stdout))
    logging.info("Logger initialized")
    
def init_stdout():
    root_logger= logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(logging.StreamHandler(sys.stdout))
    logging.info("Logger initialized")

#add new method
#
def init_custom_name():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
            'logs/trace.log', maxBytes=Cfg.LOG_SIZE * 1024 * 1024,
            backupCount=Cfg.BACKUP_COUNT, encoding='utf-8')
    handler.setFormatter(logging.Formatter(
            '%(levelname)s:%(process)d %(threadName)s %(name)s %(asctime)s %(filename)s:%(lineno)d %(message)s'))
    root_logger.addHandler(handler)
    root_logger.addHandler(logging.StreamHandler(sys.stdout))    
    logging.info("Logger initialized")

    
def init_remote():
    root_logger= logging.getLogger()
    root_logger.setLevel(logging.INFO)
    socketHandler = logging.handlers.SocketHandler(Cfg.LOGGER_HOST,
                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    root_logger.addHandler(socketHandler)
    root_logger.addFilter(HostnameFilter())
    root_logger.addHandler(logging.StreamHandler(sys.stdout))    
    logging.info("Logger initialized")


def init_confidence_logger():
    root_logger = logging.getLogger("confidence")
    root_logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
            'logs/confidence.log', maxBytes=100 * 1024 * 1024,
            backupCount=2, encoding='utf-8')
    handler.setFormatter(logging.Formatter(
            '%(asctime)s.%(msecs)03d,%(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    root_logger.addHandler(handler)
    root_logger.addHandler(logging.StreamHandler(sys.stdout))    
    logging.info("Confidence logger initialized")
    
class FileHandlerWithOneFilePerPeriod(FileHandler):
    """A handler which writes formatted logging records to files, one file per period.
    From: https://stackoverflow.com/questions/19074645/need-to-do-a-daily-log-rotation-0utc-using-python
    """
    def __init__(self, filename_pattern, mode='a', encoding=None, delay=False):
        self.filename_pattern = filename_pattern
        filename = datetime.now().strftime(self.filename_pattern)
        super().__init__(filename, mode, encoding, delay)
    
    def emit(self, record: LogRecord):
        new_filename = datetime.fromtimestamp(record.created).strftime(self.filename_pattern)
        if self.stream is None:
            self.set_new_filename(new_filename)
        elif self.differs_from_current_filename(new_filename):
            self.close()
            self.set_new_filename(new_filename)
    
        super().emit(record)
    
    def set_new_filename(self, new_filename):
        self.baseFilename = new_filename
    
    def differs_from_current_filename(self, filename: str) -> bool:
        return filename != self.baseFilename
    
def init_daily_file(file_prefix=Cfg.LOGGING_FILE_PREFIX):
    root_logger= logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = FileHandlerWithOneFilePerPeriod(
            filename_pattern=f'logs/{file_prefix}-%Y%m%d.log', encoding='utf-8')
    handler.setFormatter(logging.Formatter(
            '%(levelname)s:%(process)d %(threadName)s %(name)s %(asctime)s %(filename)s:%(lineno)d %(message)s'))
    root_logger.addHandler(handler)
    root_logger.addHandler(logging.StreamHandler(sys.stdout))
    logging.info("Logger initialized")
