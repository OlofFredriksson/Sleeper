#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/getSleepValue", GetSleepValue),
            (r"/updateSleepValue", UpdateSleepValue),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        ## Sleep function comming here


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ""
        self.render("form.html", title="My title", items=items)

class GetSleepValue(tornado.web.RequestHandler):
    def get(self):
        self.write("100")

class UpdateSleepValue(tornado.web.RequestHandler):
    def get(self):
        #do something here
        self.write("")

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
    