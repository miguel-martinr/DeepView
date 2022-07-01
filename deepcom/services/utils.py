from scipy import stats
import numpy as np


def segment(values, size):
    segments = []
    for i in range(0, len(values), size):
        segments.append(values[i:i+size])
    return segments


def mode_by_segment(segments):
    result = []
    for segment in segments:                
        mode = stats.mode(segment)[0]
        result.append(int(mode[0]))
    return result



def get_particles_quantity(frames: list, unit='seconds'):

    particles_per_frame = [len(frame['particles']) for frame in frames]

    seconds_segments = segment(particles_per_frame, 30)
    by_second = mode_by_segment(seconds_segments)

    if unit == 'seconds': return by_second

    if unit == 'minutes': 
      
      minutes_segments = segment(by_second, 60)
      by_minute = mode_by_segment([np.sum(min) for min in minutes_segments])
      return by_minute
    
    else:
      hours_segments = segment(by_second, 1800)
      by_hour = mode_by_segment([np.sum(hour) for hour in hours_segments])
      return by_hour
