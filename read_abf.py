import neo
import numpy as np
import logging
from matplotlib import pyplot as plt


logging.basicConfig(format='[%(funcName)s]: %(message)s', level=logging.INFO)
logger = logging.getLogger()

filename = '../19n28000.abf'
r = neo.io.AxonIO(filename)
block = r.read_block()
logger.info(block)

for seg in block.segments:
    print("Analyzing segment %d" % seg.index)

    avg = np.mean(seg.analogsignals[0], axis=1)

    plt.figure()
    plt.plot(avg)
    plt.title("Peak response in segment %d: %f" % (seg.index, avg.max()))
    plt.show()