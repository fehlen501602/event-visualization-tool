# Event visualization tool
A simple tool to visualize the events data. Events are buffered into event windows and those event windows are transformed into alternative representations that facilitate the extraction of meaningful information.
## Dependencies
- Pandas
- Numpy
- matplotlib.pyplot
## Parameters
- ``--fixed_size`` Accumulate fixed number of events per window.
- ``--fixed_duration`` Accumulate events within a fixed duration (i.e. a fixed output frame rate).
- ``--fixed_size_and_fixed_duration`` Setup minimum size limitation for each window. First accumulate events within a fixed duration into event window, if window size is lower than the lower band, it will be filled up to the minimum size limit.
- ``--window_size`` / ``-N`` (default: 1000) Number of events per window.
- ``--window_duration`` / ``-T`` (default: 60 ms) Duration of each event window, in milliseconds. 
- ``--event_histogramm`` the method you choose to represent the events data.
## Run
fixed size:
```
python reconstructor.py  -i data/file.csv  --fixed_size  -N 500  --event_histogram
```
fixed duration:
```
python reconstructor.py  -i data/file.csv  --fixed_duration  -T 200  --event_histogram
```
fixed duration and size:
```
python reconstructor.py  -i data/file.csv  --fixed_size_and_fixed_duration  -N 100 -T 200  --event_histogram
```
## Example
Some example results are given in tha data folder.


