import os
import functools
import logging
import tornado.web
from tornado.options import options

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("form.html")

class GetSleepValue(tornado.web.RequestHandler):
    def get(self):
         self.write(str(self.application.sleepTicker.endTime.strftime("%Y-%m-%d %H:%M:%S ")))

class UpdateSleepValue(tornado.web.RequestHandler):
    def post(self):
        try:
            seconds = int(self.get_argument("sleep",0))
            self.application.sleepTicker.increaseTicker(seconds)
        except ValueError:
            logging.error("Variable is not an int")
        self.set_header("Content-Type", "text/plain")
        self.redirect("/",permanent=True)


class ErrorHandler(tornado.web.RequestHandler):
    def get(self):

        #Always send out 404 status code
        self.set_status(404)
        self.render(u"../templates/404.html",
            path = self.request.path,
            options = options)