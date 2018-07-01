#!/usr/bin/env python
# coding: utf-8

"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from urlparse import parse_qs
import logging
import sys
import time

import lib


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
loggerHandler = logging.StreamHandler(sys.stdout)  # set output to stdout
loggerHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(loggerHandler)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        # Simulate a dead lock
        setDeadLock = parse_qs(self.path[2:]).get('deadLock', ['']).pop().lower()
        logger.debug(setDeadLock)
        while setDeadLock == 'true':
            time.sleep(0.1)

        self._set_headers()
        self.wfile.write("<html><body><h1>" + lib.msg('hi') + "</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=8088):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()