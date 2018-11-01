# coding:utf-8
import logzero
import logging
from logzero import logger
from .config import logfile_path


logzero.logfile(logfile_path, maxBytes=1024**4*100, backupCount=3)
formatter = logging.Formatter('%(asctime)-15s - %(levelname)s: %(message)s')
logzero.formatter(formatter)
log_template = 'OPERATE:%s\tINFO:%s\tSTATUS:%s'
