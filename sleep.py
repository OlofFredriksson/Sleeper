# -*- coding: utf-8 -*-
from audio.pactl import *
from datetime import *
import logging
from utils import *

class Sleep:
    def __init__(self, audioPlugin, secondsLeft, startUpAudioVolume):
        self.endTime = datetime.now() + timedelta(seconds=secondsLeft)
        self.AudioDisabled = False

        # Init the audio plugin class, configurable in the config file
        pluginClass = load_class("audio."+ audioPlugin.lower() + "." + audioPlugin)
        logging.info("Audio plugin " + audioPlugin + " is activated")
        self.audio = pluginClass()
        self.audio.setAudio(startUpAudioVolume)

    def ticker(self):
        if datetime.now() > self.endTime and self.AudioDisabled == False:
            self.audio.setAudio(0)
            logging.info("Audio is disabled")
            self.AudioDisabled = True

    def increaseTicker(self, minutes):
        self.AudioDisabled = False
        self.endTime =  self.endTime + timedelta(minutes=minutes)
        logging.info("Audio is activated, end time is " + str(self.endTime))
        self.audio.setAudio(100)
