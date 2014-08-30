
#! usr/bin/env python
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import json
import dbQuery
import django.utils.html

def application(environ, start_response):
   ret = ""  # return value

   # the environment variable CONTENT_LENGTH may be empty or missing
   try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
   except (ValueError):
      request_body_size = 0

   response_body = ['%s: %s' % (key, value)
                    for key, value in sorted(environ.items())]
   response_body = '\n'.join(response_body)

   print (response_body)

   method = environ.get("REQUEST_METHOD")
   if (method == "GET"):

      # Returns a dictionary containing lists as values.
      d = parse_qs(environ['QUERY_STRING'])

      if (len(d) == 0):
         d = escape(django.utils.html.escape(environ['QUERY_STRING']))
         if (d == "pall"):
            ret = dbQuery.getPrinters()
         elif (d == "etypes"):
            ret = dbQuery.getErrorTypes()
      else:
         if ("pid" in d):
            ret = dbQuery.getPrinters(id = escape(d.get("pid",[''])[0]))

   elif (method == "POST"):
      # When the method is POST the query string will be sent
      # in the HTTP request body which is passed by the WSGI server
      # in the file like wsgi.input environment variable.
         request_body = environ['wsgi.input'].read(request_body_size)

         print (request_body)
         ret = parse_qs(request_body)
         print (request_body)

   status = '200 OK'

   # Now content type is text/html
   response_headers = [('Content-Type', 'application/json')]#ext/html')]
   start_response(status, response_headers)

   return ret

