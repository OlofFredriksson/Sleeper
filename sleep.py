# -*- coding: utf-8 -*-
from audio.alsa import *
from datetime import *
class Sleep:
    def __init__(self, secondsLeft, startUpAudioVolume):
        self.endTime = datetime.now() + timedelta(seconds=secondsLeft)

        #Only have support for Alsa plugin right now, should be possible to add more plugins
        self.audio = Alsa()
        self.audio.setAudio(startUpAudioVolume)

    def ticker(self):
        if datetime.now() > self.endTime:
            self.audio.setAudio(-20)

    def increaseTicker(self, seconds):
        self.endTime = datetime.now() + timedelta(seconds=seconds)
        self.audio.setAudio(100)
