# encoding:utf-8
import logging
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler(filename="phoneco.log", mode='a', maxBytes=5*1024**2, backupCount=0, encoding=None, delay=0)

handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
