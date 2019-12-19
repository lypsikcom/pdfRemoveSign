import sys

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from .api import app

def gooo():
    sys.path.append(".")
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)  #flask默认的端口
    IOLoop.instance().start()