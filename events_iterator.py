import pandas as pd
import numpy as np
from os.path import splitext
import zipfile
import events_loader

class Fixed_Events_Numbers_iterator:
    def __init__(self, event_file_path, num_events=10000, start_index=0):
        self.iterator = pd.read_csv(event_file_path, delim_whitespace=False, header=None,
                                    names=['x', 'y', 't', 'pol'],
                                    dtype={'x': np.int16, 'y': np.int16, 't': np.float64, 'pol': np.int16},
                                    engine='python',
                                    skiprows=start_index + 1, chunksize=num_events, nrows=None, memory_map=True)
    def __iter__(self):
     return self

    def __next__(self):
        event_window = self.iterator.__next__().values
        return event_window

class Fixed_Frame_Duration_iterator:
    def __init__(self, event_file_path, duration_ms=60.0, start_index=0):
        file_extension = splitext(event_file_path)[1]
        assert(file_extension in ['.txt', '.zip', '.csv'])
        self.is_zip_file = (file_extension == '.zip')
        self.is_txt_file = (file_extension == '.txt')
        self.is_csv_file = (file_extension == '.csv')

        if self.is_zip_file:
            self.zip_file = zipfile.ZipFile(event_file_path)
            files_in_archive = self.zip_file.namelist()
            assert(len(files_in_archive) == 1) 
            self.event_file = self.zip_file.open(files_in_archive[0], 'r')
        elif self.is_txt_file:
            self.event_file = open(event_file_path, 'r')
        elif self.is_csv_file:
            with open(event_file_path) as file:
                self.event_file = np.loadtxt(file, delimiter="," , skiprows=start_index + 1)
            

        for i in range(1 + start_index):
            if self.is_zip_file or self.is_txt_file:
                self.event_file.readline()
            #if self.is_csv_file:
            #    self.event_file = self.event_file[0:1 + start_index]
                

        self.last_stamp = None
        self.duration_s = duration_ms / 1000.0
        self.duration_ms = duration_ms

    def __iter__(self):
     return self  

    def __del__(self):
        if self.is_zip_file:
            self.zip_file.close()
        elif self.is_txt_file:
            self.event_file.close()

    def __next__(self):
            event_list = []
            event_window = []
            for line in self.event_file:               
                if self.is_zip_file:
                    line = line.decode("utf-8")
                if self.is_zip_file or self.is_txt_file:
                 x, y, t, pol = line.split(' ')
                 x, y, t, pol = int(x), int(y), float(t), int(pol)
                else:
                 idx, x, y, t, pol = line
                event_list.append([x, y, t, pol])
                if self.last_stamp is None:
                    self.last_stamp = t
                if t < self.last_stamp + self.duration_ms:
                    #self.last_stamp = t
                    ew = np.array(event_list)
                if t >= self.last_stamp + self.duration_ms:
                    self.last_stamp = t
                    event_list=[]
                    event_list.append([x, y, t, pol])
                    event_window.append(ew)
            return event_window
    
class Fixed_Events_and_Duration_iterator:
    def __init__(self, event_file_path, num_events=100, duration_ms=200.0, start_index=0):
        file_extension = splitext(event_file_path)[1]
        assert(file_extension in ['.txt', '.zip', '.csv'])
        self.is_zip_file = (file_extension == '.zip')
        self.is_txt_file = (file_extension == '.txt')
        self.is_csv_file = (file_extension == '.csv')

        if self.is_zip_file:
            self.zip_file = zipfile.ZipFile(event_file_path)
            files_in_archive = self.zip_file.namelist()
            assert(len(files_in_archive) == 1) 
            self.event_file = self.zip_file.open(files_in_archive[0], 'r')
        elif self.is_txt_file:
            self.event_file = open(event_file_path, 'r')
        elif self.is_csv_file:
            with open(event_file_path) as file:
                self.event_file = np.loadtxt(file, delimiter="," , skiprows=start_index + 1)
            

        for i in range(1 + start_index):
            if self.is_zip_file or self.is_txt_file:
                self.event_file.readline()
            #if self.is_csv_file:
            #    self.event_file = self.event_file[0:1 + start_index]
                
        self.num_events = num_events
        self.last_stamp = None
        self.duration_s = duration_ms / 1000.0
        self.duration_ms = duration_ms

    def __iter__(self):
     return self  

    def __del__(self):
        if self.is_zip_file:
            self.zip_file.close()
        elif self.is_txt_file:
            self.event_file.close()

    def __next__(self):
            event_list = []
            event_window = []
            for line in self.event_file:               
                if self.is_zip_file:
                    line = line.decode("utf-8")
                if self.is_zip_file or self.is_txt_file:
                 x, y, t, pol = line.split(' ')
                 x, y, t, pol = int(x), int(y), float(t), int(pol)
                else:
                 idx, x, y, t, pol = line
                event_list.append([x, y, t, pol])
                if self.last_stamp is None:
                    self.last_stamp = t
                if t < self.last_stamp + self.duration_ms:
                    #self.last_stamp = t
                    ew = np.array(event_list)
                if t >= self.last_stamp + self.duration_ms:
                    if ew.shape[0] < self.num_events:
                        ew = np.array(event_list)
                        continue
                    else:
                     self.last_stamp = t
                     event_list=[]
                     event_list.append([x, y, t, pol])
                     event_window.append(ew)
            return event_window





#raise StopIteration






