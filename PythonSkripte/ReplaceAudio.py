import os


def replace_audio(videoname, finalname, audioname="audio"):

    os.system("ffmpeg -i " + videoname + ".avi -i " + audioname +
              ".wav -codec copy -shortest " + finalname + ".avi")


def shorten_audio(inputname, outputname, time1, time2):
    os.system("ffmpeg -i " + inputname +
              ".wav -ss {} -to {} -c copy ".format(time1, time2) + outputname + ".wav")

#replace_audio("v", "a", "newvideo")
