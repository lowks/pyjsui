#!/usr/bin/env python

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


s = pizco.Server(Foo(), 'tcp://127.0.0.1:12345')
s.serve_forever()
