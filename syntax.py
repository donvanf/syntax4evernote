#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import cgi

base_path = os.path.dirname(os.path.abspath(__file__))

PORT_NUMBER = 80


#This class will handles any incoming request from
#the browser
class SyntaxHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        try:
            #Check the file extension required and
            #set the right mime type

            send_reply = False
            if self.path.endswith(".html"):
                mime_type = 'text/html'
                send_reply = True
            if self.path.endswith(".jpg"):
                mime_type = 'image/jpg'
                send_reply = True
            if self.path.endswith(".gif"):
                mime_type = 'image/gif'
                send_reply = True
            if self.path.endswith(".js"):
                mime_type = 'application/javascript'
                send_reply = True
            if self.path.endswith(".css"):
                mime_type = 'text/css'
                send_reply = True

            if send_reply:
                #Open the static file requested and send it
                f = open(base_path + self.path)
                self.send_response(200)
                self.send_header('Content-type', mime_type)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        if self.path == "/":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                })
            self.path = "/result.html"
            try:
                f = open(base_path + self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                replay = form["code"].value.replace('<', '&lt;').replace('>', '&gt;')
                self.wfile.write(''.join(f.readlines()) % replay)
                return
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), SyntaxHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
