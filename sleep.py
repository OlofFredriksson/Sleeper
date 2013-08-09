from audio.alsa import *
from datetime import datetime
class Sleep:
    def __init__(self, secondsLeft, startUpAudioVolume):
        self.secondsLeft = secondsLeft

        #Only have support for Alsa plugin right now, should be possible to add more plugins
        self.audio = Alsa()
        self.audio.setAudio(startUpAudioVolume)
    def ticker(self):
        print (datetime.now());
        print(self.secondsLeft)
        if self.secondsLeft > 0:
            self.secondsLeft = self.secondsLeft -1 #Why aint -- working like a normal language, like php?
        else:
                self.audio.setAudio(-20)
    def increaseTicker(self, seconds):
        self.secondsLeft = seconds
        self.audio.setAudio(100)
