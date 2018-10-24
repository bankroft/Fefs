# coding:utf-8
import logzero
import logging
from logzero import logger


logzero.logfile("Fefs.log", maxBytes=1024**4*100, backupCount=3)
formatter = logging.Formatter('%(asctime)-15s - %(levelname)s: %(message)s')
logzero.formatter(formatter)
log_template = '操作:%s\t信息:%s\t状态:%s'
