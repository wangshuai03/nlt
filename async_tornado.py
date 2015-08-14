import tornado
import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from tornado.options import options, define, parse_command_line
from settings import url


class AsyncHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = AsyncHTTPClient()
        http.fetch(url, callback=self.on_response)

    def on_response(self, response):
        body = response.body
        self.write(body)
        self.finish()


class AsyncMultiHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = AsyncHTTPClient()
        http.fetch(url, callback=self.on_response)

    def on_response(self, response):
        body = response.body
        http = AsyncHTTPClient()
        http.fetch(url, callback=self.on_response1)

    def on_response1(self, response):
        body = response.body
        http = AsyncHTTPClient()
        http.fetch(url, callback=self.on_response2)

    def on_response2(self, response):
        self.write(response.body)
        self.finish()


if __name__ == '__main__':
    define('port', type=int, default=8888)
    define('debug', type=bool, default=True)
    parse_command_line()
    settings = {
        'debug': options.debug,
    }

    application = tornado.web.Application([
        (r'/async', AsyncHandler),
        (r'/async_multi', AsyncMultiHandler),
    ], **settings)

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
