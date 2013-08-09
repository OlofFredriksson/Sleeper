import os
import sys
class Alsa:
    def setAudio(self,value):
        os.system("pactl set-sink-volume 0 -- " + str(value) + "%" )