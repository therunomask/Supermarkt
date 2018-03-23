import numpy as np
from _bisect import bisect


def cut_frames(time_stamps, frame_list):
    time_stamps = np.array(time_stamps) - time_stamps[0]
    steady_frames = []
    aimed_time = np.arange(
        int((time_stamps[-1] - time_stamps[0]) * 20) + 5) / 20
    for aim in aimed_time:
        steady_frames.append(frame_list[bisect(time_stamps, aim) - 1])
    return steady_frames
