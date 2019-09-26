#!/usr/bin/env python

import sys
import pandas as pd

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

ofile = sys.argv[1]

df = pd.read_csv(ofile, sep=' ', names=['t', 'x', 'y', 'z'])
t = np.linspace(df.t.min(), df.t.max(), len(df) )# new_timestamps
#ax = plt.subplot(113)
plt.plot(t, df.x)
plt.show()



