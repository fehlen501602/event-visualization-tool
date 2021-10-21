import pandas as pd
import numpy as np
from os.path import splitext
import zipfile

class Fixed_Events_Numbers_iterator:
    def __init__(self, event_file_path, num_events=1000, start_index=0):
     self.iterator = pd.read_csv(event_file_path, delim_whitespace=True, header=None,
                                    names=['x', 'y', 't', 'pol'],
                                    dtype={'x': np.int16, 'y': np.int16, 't': np.float64, 'pol': np.int16},
                                    engine='python',
                                    skiprows=start_index + 1, chunksize=num_events, nrows=None, memory_map=True)
    
    def __iter__(self):
     return self

class Fixed_Frame_Duration_iterator:
    def __init__(self, event_file_path, duration_ms=60.0, start_index=0):
        file_extension = splitext(event_file_path)[1]
        assert(file_extension in ['.txt', '.zip'])
        self.is_zip_file = (file_extension == '.zip')
        self.is_txt_file = (file_extension == '.txt')
        self.is_pkl_file = (file_extension == '.pkl')

        if self.is_zip_file:
            self.zip_file = zipfile.ZipFile(event_file_path)
            files_in_archive = self.zip_file.namelist()
            assert(len(files_in_archive) == 1) 
            self.event_file = self.zip_file.open(files_in_archive[0], 'r')
        elif self.is_txt_file:
            self.event_file = open(event_file_path, 'r')
        elif self.is_pkl_file:
            self.event_file = open(event_file_path, 'rb')

        for i in range(1 + start_index):
            self.event_file.readline()

        self.last_stamp = None
        self.duration_s = duration_ms / 1000.0 

    def __iter__(self):
     return self  


