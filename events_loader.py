import pandas as pd
import numpy as np
import pickle
from os.path import splitext
import zipfile


def __geteventsdata__(filename):
        """
        returns events, loading events from files
        :param filename(filepath):
        :return: csv
        """
        with open (str(filename), 'rb') as pickle_file:
             events= pickle.load(pickle_file)

        t, y, x, p = events
        x = x.astype(np.int)
        y = y.astype(np.int)
        tmp = events[0].astype(np.int)
        events[2] = tmp
        events[1] = y
        events[0] = x
        events=events.T

        np.savetxt(str(filename)+'.csv', events, delimiter=",")

