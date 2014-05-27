#!/usr/bin/env python


import jsui
import pizco


class Foo(object):
    def __init__(self):
        self.msg = ""
        self.new_message = pizco.Signal(nargs=1)

    def hi(self):
        print("hi")
        return "hi"

    def set_message(self, msg):
        self.msg = msg
        self.new_message.emit(self.msg)

    def get_message(self):
        return self.msg


template = """
<html>
    <head>
        <script src="{{url_for('static', filename='js/jquery-2.1.0.js')}}" type="text/javascript"></script>
        <script src="{{url_for('static', filename='js/jquery.json-2.4.js')}}" type="text/javascript"></script>
        <script src="{{url_for('static', filename='js/jquery.jsonrpcclient.js')}}" type="text/javascript"></script>
    </head>
    <body>
        <script type="text/javascript">
        var ecb = function (e) {
            console.log({'error': e});
        };
        var rcb = function (r) {
            console.log({'result': r});
        };
        var socket;
        $(function () {
            socket = new $.JsonRpcClient({'socketUrl': 'ws://127.0.0.1:5000/{{ name }}/ws'});
        });
        </script>
    </body>
</html>
"""


specs = [
    {
        'name': 'a',
        'object': Foo(),
        #'encoder': ,
        #'decoder': ,
        'template': template,
        #'css': ,
        #'html': ,
        #'js': ,
    },
    {
        'name': 'b',
        'object': Foo(),
        'template': template,
    },
]

for s in specs:
    jsui.serve.register(s)

jsui.serve.serve()
