#!/usr/bin/env python

from tornado.ioloop import IOLoop
import jsui

import pizco


js = """
        var ecb = function (e) {
            console.log({'error': e});
        };
        var rcb = function (r) {
            console.log({'result': r});
        };
        var socket;
        $(function () {
            socket = new $.JsonRpcClient(
            {'socketUrl': 'ws://' + window.location.host + '/{{ name }}/ws'});
        });
"""

template = """
<html>
    <head>
        <script src="{{url_for('static', filename='js/jquery-2.1.0.js')}}" type="text/javascript"></script>
        <script src="{{url_for('static', filename='js/jquery.json-2.4.js')}}" type="text/javascript"></script>
        <script src="{{url_for('static', filename='js/jquery.jsonrpcclient.js')}}" type="text/javascript"></script>
    </head>
    <body>
        {% if js is defined %}
            <script type="text/javascript">
            {{ js }}
            </script>
        {% endif %}
    </body>
</html>
"""

# this pollutes tornado.ioloop.IOLoop
p = pizco.Proxy('tcp://127.0.0.1:12345')
del IOLoop._instance

spec = {
    'name': 'a',
    'object': p,
    #'encoder': ,
    #'decoder': ,
    'template': template,
    #'css': ,
    #'html': ,
    'js': js,
}

jsui.serve.register(spec)

jsui.serve.serve()
