#!/usr/bin/env python

import flask
import gevent

import rpc


def rename(name):
    def wrap(func):
        func.func_name = name
        return func
    return wrap


def register(spec):
    @rpc.serve.sockets.route('/{}/ws'.format(spec['name']))
    def websocket(ws):
        handler = rpc.wrapper.JSONRPC(
            spec['object'], ws, encoder=spec.get('encoder', None),
            decoder=spec.get('decoder', None))
        while not ws.closed:
            gevent.sleep(0.001)
            handler.update()
    # register template
    if 'css' in spec:
        @rpc.serve.server.route('/{}/css'.format(spec['name']))
        @rename('{}_css'.format(spec['name']))
        def css():
            return flask.render_template_string(spec['css'], **spec)
    if 'js' in spec:
        @rpc.serve.server.route('/{}/js'.format(spec['name']))
        @rename('{}_js'.format(spec['name']))
        def js():
            # for signals, register persistant callbacks
            # for functions, register temporary callbacks
            return flask.render_template_string(spec['js'], **spec)
    if 'html' in spec:
        @rpc.serve.server.route('/{}/html'.format(spec['name']))
        @rename('{}_html'.format(spec['name']))
        def html():
            return flask.render_template_string(spec['html'], **spec)
    if 'template' in spec:
        # register template
        @rpc.serve.server.route('/{}'.format(spec['name']))
        @rename('{}_template'.format(spec['name']))
        def template():
            # pre-render css, html, js
            local_spec = spec.copy()
            for item in ('css', 'js', 'html'):
                if item in spec:
                    local_spec[item] = flask.render_template_string(
                        spec[item], **spec)
            return flask.render_template_string(
                spec['template'], **local_spec)
    # pde?


def serve():
    rpc.serve.server.debug = True
    rpc.serve.serve()
