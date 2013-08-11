import os
import sys
class Pactl:
    def setAudio(self,value):
        os.system("pactl set-sink-volume 0 -- " + str(value) + "%" )