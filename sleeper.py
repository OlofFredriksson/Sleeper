#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
from datetime import datetime
from tornado.options import define, options
from subprocess import call

define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ""
        self.render("form.html", title="My title", items=items)

class GetSleepValue(tornado.web.RequestHandler):
    def get(self):
         self.write(str(self.application.sleepTicker.secondsLeft))
         #self.write("55")

class UpdateSleepValue(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.application.sleepTicker.secondsLeft = int(self.get_argument("sleep"))
        os.system("pactl set-sink-volume 0 -- 100%")
        self.redirect("/",permanent=True)

class Sleep:
    def __init__(self):
        self.secondsLeft = 9999
    def ticker(self):
        print (datetime.now());
        print(self.secondsLeft)
        if self.secondsLeft > 0:
            self.secondsLeft = self.secondsLeft -1 #Why aint -- working like a normal language, like php?
        else:
                os.system("pactl set-sink-volume 0 -- -20%")


def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        # Rputes
        [
            (r"/", MainHandler),
            (r"/getSleepValue", GetSleepValue),
            (r"/updateSleepValue", UpdateSleepValue),
        ],

        # Settings
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static")
    )
    main_loop = tornado.ioloop.IOLoop.instance()

    # Setting upp Sleep class
    app.sleepTicker = Sleep()
    
    #Adding 
    sleepLoop = tornado.ioloop.PeriodicCallback(app.sleepTicker.ticker,1000,io_loop = main_loop)
    sleepLoop.start();
    
    try:
        app.listen(options.port);
        main_loop.start();
    except KeyboardInterrupt:
        print("Good bye")
    except:
        print("Could not start application!")
        exit()
    
if __name__ == "__main__":
    main()
    