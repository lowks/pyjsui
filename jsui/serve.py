#!/usr/bin/env python

import flask
import flask_sockets
import gevent
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from . import wrapper


server = flask.Flask('rpc')
sockets = flask_sockets.Sockets(server)


def register(obj, url=None):
    if url is None:
        url = '/ws'

    @sockets.route(url)
    def websocket(ws):
        handler = wrapper.JSONRPC(obj, ws)
        while not ws.closed:
            gevent.sleep(0.001)
            handler.update()


def register(spec):
    @sockets.route('/{}/ws'.format(spec['name']))
    def websocket(ws):
        handler = wrapper.JSONRPC(spec['object'], ws)
        while not ws.closed:
            gevent.sleep(0.001)
            handler.update()
    # register template
    if 'template' in spec:
        # register template
        @server.route('/{}')
        def template():
            # spec['template']
            pass
    if 'css' in spec:
        @server.route('/{}/css')
        def css():
            # spec['css']
            pass
    if 'js' in spec:
        @server.route('/{}/js')
        def js():
            # for signals, register persistant callbacks
            # for functions, register temporary callbacks
            # spec['js']
            pass
    if 'html' in spec:
        @server.route('/{}/html')
        def html():
            pass
    # pde?


def serve():
    wsgi_server = pywsgi.WSGIServer(
        ('', 5000), server, handler_class=WebSocketHandler)
    wsgi_server.serve_forever()
