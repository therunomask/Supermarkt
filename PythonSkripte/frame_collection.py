import numpy as np
from _bisect import bisect


def cut_frames(time_stamps, frame_list):
    steady_frames = []
    aimed_time = np.arange(
        int((time_stamps[-1] - time_stamps[0]) * 30) + 5) / 30
    for aim in aimed_time:
        steady_frames.append(frame_list[bisect(time_stamps, aim) - 1])
    return steady_frames
