import tornado
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.options import options, define, parse_command_line
from settings import url


class GenHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        http = AsyncHTTPClient()
        response = yield gen.Task(http.fetch, url)
        self.write(response.body)
        self.finish()


class GenMultiHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        http = AsyncHTTPClient()
        response, response1, response2 = yield [gen.Task(http.fetch, url),
                                                gen.Task(http.fetch, url),
                                                gen.Task(http.fetch, url)]
        b1 = response1.body
        b2 = response2.body
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
        (r'/gen', GenHandler),
        (r'/gen_multi', GenMultiHandler),
    ], **settings)

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
