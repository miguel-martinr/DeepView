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

def summarize(values, segments_size):    
    unit_segments = segment(values, segments_size)
    by_unit = mode_by_segment(unit_segments)
    return by_unit


def get_particles_by_second(frames: list):
  particles_per_frame = [len(frame['particles']) for frame in frames]
  segments_30frames = segment(particles_per_frame, 30)
  return [int(stats.mode(segment)[0]) for segment in segments_30frames]    


def get_particles_quantity(frames: list, unit='seconds'):

    particles_per_frame = [len(frame['particles']) for frame in frames]

    by_second = summarize(particles_per_frame, 60)

    if unit == 'seconds': return by_second

    if unit == 'minutes':       
      by_minute = summarize(by_second, 60)
      return by_minute
    
    else:
      by_hour = summarize(by_second, 3600)
      return by_hour


