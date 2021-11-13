import numpy as np
from events_iterator import Fixed_Events_Numbers_iterator, Fixed_Events_and_Duration_iterator, Fixed_Frame_Duration_iterator
import argparse
from events_to_representation import generate_event_histogram
from image_reconstructor import image_reconstructor
import torch

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True, type=str)
    parser.add_argument('--fixed_duration', dest='fixed_duration', action='store_true')
    parser.add_argument('--fixed_size', dest='fixed_size', action='store_true')
    parser.add_argument('--fixed_size_and_fixed_duration', dest='fixed_size_and_fixed_duration', action='store_true')
    parser.add_argument('-N', '--window_size', default=10000, type=int,
                         help="Size of each event window, in number of events")
    parser.add_argument('-T', '--window_duration', default=60, type=float, 
                         help="Duration of each event window, in milliseconds")
    parser.add_argument('--event_histogram', dest='event_histogram', action='store_true')
    parser.set_defaults(fixed_duration=False)
    
    
    height = 260
    width = 346

    args = parser.parse_args()
    N = args.window_size
    T = args.window_duration
    event_path  = args.input_file
    start_index = 0

    

    if args.fixed_duration:
        events_iterator = Fixed_Frame_Duration_iterator(event_path,
                                                         duration_ms=args.window_duration,
                                                         start_index=start_index)
    elif args.fixed_size:
        events_iterator = Fixed_Events_Numbers_iterator(event_path, num_events=N, start_index=start_index)       

    elif args.fixed_size_and_fixed_duration:
        events_iterator = Fixed_Events_and_Duration_iterator(event_path, num_events=N, duration_ms=T, start_index=start_index)                                    

    for idx, event_window in enumerate(events_iterator):
        #print(len(event_window), event_window[8])
        #last_timestamp = event_window[-1, 2]
        if args.fixed_duration:
          for i in range(len(event_window)):
           if args.event_histogram:
                    event_histo = generate_event_histogram(event_window[i],(height,width))
                    #event_tensor = torch.from_numpy(event_tensor)
                    reconstructor = image_reconstructor(event_histo, event_path + str(i) + '.png')
        if args.fixed_size:
          for i in range(len(event_window)):
           if args.event_histogram:
                    event_histo = generate_event_histogram(event_window,(height,width))
                    #event_tensor = torch.from_numpy(event_tensor)
        
          num_events_in_window = event_window.shape[0]
          reconstructor = image_reconstructor(event_histo, event_path + str(idx) + '.png')
        #reconstructor.update_reconstruction(event_tensor, start_index + num_events_in_window, last_timestamp)

          start_index += num_events_in_window

        if args.fixed_size_and_fixed_duration:
          for i in range(len(event_window)):
           if args.event_histogram:
                    event_histo = generate_event_histogram(event_window[i],(height,width))
                    #event_tensor = torch.from_numpy(event_tensor)
                    reconstructor = image_reconstructor(event_histo, event_path + str(i) + '.png')
