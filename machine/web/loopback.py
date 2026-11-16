"""The web servers The Machine starts on 127.0.0.1 (the dashboard, App.serve; the key-waiting page, waiting.py).

http.server's own server names itself when it binds, with socket.getfqdn on its address: a reverse DNS lookup that
can take seconds on macOS before the server answers anything. Nothing here reads that name, so Server binds without
the lookup."""
import http.server
import socketserver


class Server(http.server.ThreadingHTTPServer):
    def server_bind(self):
        socketserver.TCPServer.server_bind(self)
        self.server_name, self.server_port = 'localhost', self.server_address[1]  # what HTTPServer sets, without the lookup
