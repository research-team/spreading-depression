import neo
import logging

logging.basicConfig(format='[%(funcName)s]: %(message)s', level=logging.INFO)
logger = logging.getLogger()

filename = '../19n28000.abf'
r = neo.io.AxonIO(filename)
blk = r.read_block()
logger.info(blk)