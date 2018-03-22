import os


def replace_audio(videoname, finalname, audioname="audio"):

    os.system("ffmpeg -i " + videoname + ".avi -i " + audioname +
              ".wav -codec copy -shortest " + finalname + ".avi")


#replace_audio("v", "a", "newvideo")
