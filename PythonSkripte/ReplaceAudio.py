import os


def replace_audio(videoname, finalname, audioname="audio"):

    os.system("ffmpeg -i " + videoname + ".mp4 -i " + audioname +
              ".wav -c:" + videoname + " copy -map 0:" + videoname + ":0 -map 1:"
              + audioname + ":0 " + finalname + ".mp4")


replace_audio("v", "a", "newvideo")
