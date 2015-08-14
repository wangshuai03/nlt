import httplib
from urlparse import urlparse
import tornado.ioloop
import tornado.web
from tornado.options import options, define, parse_command_line
from settings import url


class HttpLibHandler(tornado.web.RequestHandler):
    def get(self):
        pr = urlparse(url)
        host = pr.hostname
        path = pr.path
        if pr.query:
            path = path + '?' + pr.query
        conn = httplib.HTTPConnection(host)
        conn.request('GET', path)
        r = conn.getresponse()
        result = r.read()
        self.write(result)


class HttpLibMultiHandler(tornado.web.RequestHandler):
    def get(self):
        pr = urlparse(url)
        host = pr.hostname
        path = pr.path
        if pr.query:
            path = path + '?' + pr.query

        conn = httplib.HTTPConnection(host)
        conn.request('GET', path)
        r = conn.getresponse()
        result = r.read()

        conn1 = httplib.HTTPConnection(host)
        conn1.request('GET', path)
        r1 = conn1.getresponse()
        result1 = r1.read()

        conn2 = httplib.HTTPConnection(host)
        conn2.request('GET', path)
        r2 = conn2.getresponse()
        result2 = r2.read()

        self.write(result)

if __name__ == '__main__':
    define('port', type=int, default=8888)
    define('debug', type=bool, default=True)
    parse_command_line()
    settings = {
        'debug': options.debug,
    }

    application = tornado.web.Application([
        (r'/httplib', HttpLibHandler),
        (r'/httplib_multi', HttpLibMultiHandler),
    ], **settings)

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
