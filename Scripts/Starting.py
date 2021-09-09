# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 15:05:32 2021

@author: Fabio Diuana
"""
#%%
import pandas as pd
import os
import numpy as np
from calendar import monthrange

import datetime
from datetime import datetime as dt
from datetime import timedelta
import itertools


from matplotlib.dates import date2num
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import math
import sys
#%%

pd.set_option('display.max_columns', 10)

#%%
MyPath = os.getcwd()

try:
    os.makedirs(os.path.join(MyPath, 'Dados'))
except:
    pass

try:
    os.makedirs(os.path.join(MyPath, 'Dados', 'Hidro','Original'))
except:
    pass

try:
    os.makedirs(os.path.join(MyPath, 'Dados', 'Hidro','Modificado'))
except:
    pass

caduhe = pd.read_csv(os.path.join(MyPath, 'Dados', 'Hidro', 'Original', 'CadUsH.csv'), sep=';', decimal=',', encoding='latin1')
