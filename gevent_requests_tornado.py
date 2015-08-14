import requests
from gevent import pywsgi as wsgi, monkey
import tornado.ioloop
import tornado.web
from tornado.wsgi import WSGIApplication
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
    monkey.patch_all()
    parse_command_line()
    settings = {
        'debug': options.debug,
    }

    application = WSGIApplication([
        (r'/requests', RequestsHandler),
        (r'/requests_multi', RequestsMultiHandler),
    ], **settings)

    server = wsgi.WSGIServer(('0.0.0.0', options.port), application)
    server.backlog = 256
    server.serve_forever()
