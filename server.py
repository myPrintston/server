#!/usr/bin/env python

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import json

def application(environ, start_response):

   # Returns a dictionary containing lists as values.
   d = environ['QUERY_STRING']


   #Refer to http://webpython.codepoint.net/wsgi_request_parsing_get
   d = escape(d)
   print (d)

   status = '200 OK'

   # Now content type is text/html
   response_headers = [('Content-Type', 'application/json')]#text/html')]
   start_response(status, response_headers)

   return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
