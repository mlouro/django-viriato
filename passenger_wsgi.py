import sys
import os

def application(environ, start_response):
        start_response("200 OK", [])
        ret = ["%s: %s\n" % (key, value)
                for key, value in environ.iteritems()]
        return ret
