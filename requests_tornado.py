import requests
import tornado.ioloop
import tornado.web
from tornado.options import options, define, parse_command_line
from settings import url


class RequestsHandler(tornado.web.RequestHandler):
    def get(self):
        r = requests.get(url)
        result = r.text
        self.write(result)


class RequestsMultiHandler(tornado.web.RequestHandler):
    def get(self):
        r = requests.get(url)
        result = r.text

        r1 = requests.get(url)
        result = r1.text

        r2 = requests.get(url)
        result = r2.text

        self.write(result)


if __name__ == '__main__':
    define('port', type=int, default=8888)
    define('debug', type=bool, default=True)
    parse_command_line()
    settings = {
        'debug': options.debug,
    }

    application = tornado.web.Application([
        (r'/requests', RequestsHandler),
        (r'/requests_multi', RequestsMultiHandler),
    ], **settings)

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
