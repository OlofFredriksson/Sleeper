#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import os
from tornado.options import define, options
from subprocess import call
from sleep import Sleep
from handlers import *
def init_configuration():
    define("port", type=int, help="Run on the given port")
    define("audio", help="Audio plugin")
    define("debug", type=bool, help="Debug mode enabled")
    define("startUpAudioVolume", type=int)
    define("secondsLeft", type=int)
    try:
        tornado.options.parse_command_line()
        tornado.options.parse_config_file("sleeper.conf")
        
    except IOError:
        logging.warning("Cant find configuration file! (sleeper.conf)")
        exit(1)

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application(
        # Routes
        [
            (r"/", MainHandler),
            (r"/getSleepValue", GetSleepValue),
            (r"/updateSleepValue", UpdateSleepValue),

            (r".*", ErrorHandler)
        ],

        # Settings
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug=options.debug
    )
    main_loop = tornado.ioloop.IOLoop.instance()

    # Setting upp Sleep class
    application.sleepTicker = Sleep(options.audio,options.secondsLeft,options.startUpAudioVolume)
    
    #Adding callback for Sleep Class
    sleepLoop = tornado.ioloop.PeriodicCallback(application.sleepTicker.ticker,1000,io_loop = main_loop)
    sleepLoop.start();

    logging.info("Sleeper is started")
    
    try:
        application.listen(options.port);
        main_loop.start();
    except KeyboardInterrupt:
        logging.info("Good bye")
    except:
        logging.error("Could not start application!")
        exit()
    
if __name__ == "__main__":
    init_configuration()
    main()