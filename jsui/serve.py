#!/usr/bin/env python

import flask
import gevent

import rpc


def rename(name):
    def wrap(func):
        func.func_name = name
        return func
    return wrap


def make_blueprint(spec):
    kwargs = {'url_prefix': '/{}'.format(spec['name'])}
    for k in ('static_folder', 'template_folder', 'static_url_path',
              'url_prefix'):
        if k in spec:
            kwargs[k] = spec[k]
    bp = flask.Blueprint(spec['name'], spec['name'], **kwargs)

    @rpc.serve.sockets.route('/{}/ws'.format(spec['name']))
    @rename('{}_ws'.format(spec['name']))
    def websocket(ws):
        handler = rpc.wrapper.JSONRPC(
            spec['object'], ws, encoder=spec.get('encoder', None),
            decoder=spec.get('decoder', None))
        while not ws.closed:
            gevent.sleep(0.001)
            handler.update()

    if 'css' in spec:
        @bp.route('/css')
        def css():
            return flask.render_template_string(spec['css'], **spec)
    if 'js' in spec:
        @bp.route('/js')
        def js():
            return flask.render_template_string(spec['js'], **spec)
    if 'html' in spec:
        @bp.route('/html')
        def html():
            return flask.render_template_string(spec['html'], **spec)
    if 'template' in spec:
        @bp.route('/')
        def template():
            local_spec = spec.copy()
            for item in ('css', 'js', 'html'):
                if item in spec:
                    local_spec[item] = flask.render_template_string(
                        spec[item], **spec)
            return flask.render_template_string(
                spec['template'], **local_spec)
    if 'template_folder' in spec:
        @bp.route('/template/<template>')
        def named_template(template):
            return flask.render_template(template)
    return bp


def register(spec):
    bp = make_blueprint(spec)
    rpc.serve.server.register_blueprint(bp)


def serve():
    rpc.serve.server.debug = True
    rpc.serve.serve()
