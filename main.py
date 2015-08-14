__author__ = 'wangshuai03@tudou.com'

from gevent import pywsgi as wsgi, monkey
import tornado
from tornado.wsgi import WSGIApplication
from tornado.options import options, define, parse_command_line
from httplib_tornado import HttpLibHandler, HttpLibMultiHandler
from requests_tornado import RequestsHandler, RequestsMultiHandler
from async_tornado import AsyncHandler, AsyncMultiHandler
from gen_engine_tornado import GenHandler, GenMultiHandler
from gevent_tornado import HttpLibHandler as GHttpLibHandler, \
    HttpLibMultiHandler as GHttpLibMultiHandler
from gevent_requests_tornado import RequestsHandler as GRequestsHandler, \
    RequestsMultiHandler as GRequestsMultiHandler

define('server', type=str, default='default')
define('port', type=int, default=8888)
define('debug', type=bool, default=True)


def main():

    settings = {
        'debug': options.debug,
    }

    if options.server == 'default':
        application = tornado.web.Application([
            (r'/httplib', HttpLibHandler),
            (r'/httplib_multi', HttpLibMultiHandler),
            (r'/requests', RequestsHandler),
            (r'/requests_multi', RequestsMultiHandler),
            (r'/async', AsyncHandler),
            (r'/async_multi', AsyncMultiHandler),
            (r'/gen', GenHandler),
            (r'/gen_multi', GenMultiHandler),
        ], **settings)

        application.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()

    elif options.server == 'gevent':
        monkey.patch_all()
        application = WSGIApplication([
            (r'/httplib', GHttpLibHandler),
            (r'/httplib_multi', GHttpLibMultiHandler),
            (r'/requests', GRequestsHandler),
            (r'/requests_multi', GRequestsMultiHandler),
        ], **settings)

        server = wsgi.WSGIServer(('0.0.0.0', options.port), application)
        server.backlog = 256
        server.serve_forever()

if __name__ == "__main__":
    parse_command_line()
    main()
