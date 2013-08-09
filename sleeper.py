#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import os
from datetime import datetime
from tornado.options import define, options
from subprocess import call
from sleep import Sleep
def init_configuration():
    define("port", type=int, help="Run on the given port")
    define("audio", help="Audio plugin")
    define("startUpAudioVolume", type=int)
    define("secondsLeft", type=int)
    try:
        tornado.options.parse_command_line()
        tornado.options.parse_config_file("sleeper.conf")
        
    except IOError:
        logging.warning("Cant find configuration file! (sleeper.conf)")
        exit(1)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ""
        self.render("form.html", title="My title", items=items)

class GetSleepValue(tornado.web.RequestHandler):
    def get(self):
         self.write(str(self.application.sleepTicker.secondsLeft))

class UpdateSleepValue(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.application.sleepTicker.increaseTicker(int(self.get_argument("sleep")))
        self.redirect("/",permanent=True)


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application(
        # Routes
        [
            (r"/", MainHandler),
            (r"/getSleepValue", GetSleepValue),
            (r"/updateSleepValue", UpdateSleepValue),
        ],

        # Settings
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static")
    )
    main_loop = tornado.ioloop.IOLoop.instance()

    # Setting upp Sleep class
    application.sleepTicker = Sleep(options.secondsLeft,options.startUpAudioVolume)
    
    #Adding callback for Sleep Class
    sleepLoop = tornado.ioloop.PeriodicCallback(application.sleepTicker.ticker,1000,io_loop = main_loop)
    sleepLoop.start();
    
    try:
        application.listen(options.port);
        main_loop.start();
    except KeyboardInterrupt:
        print("Good bye")
    except:
        print("Could not start application!")
        exit()
    
if __name__ == "__main__":
    init_configuration()
    main()
