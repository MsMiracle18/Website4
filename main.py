import socket
import json
import http.server
import threading
import os

# Конфігурація HTTP сервера
class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, this is your HTTP server!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data_dict = json.loads(post_data.decode())
        
        with open('storage/data.json', 'w') as json_file:
            json.dump(data_dict, json_file)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Data received and stored.')

# Конфігурація Socket сервера
def socket_server():
    HOST = '0.0.0.0'
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print("Сокет сервер прослуховує на порту", PORT)

    while True:
        data, addr = server_socket.recvfrom(1024)
        data_dict = json.loads(data.decode())
        
        with open('storage/data.json', 'w') as json_file:
            json.dump(data_dict, json_file)

        print("Дані збережено:", data_dict)

def main():
    if not os.path.exists('storage'):
        os.makedirs('storage')
        with open('storage/data.json', 'w') as json_file:
            json.dump({}, json_file)

    http_thread = threading.Thread(target=http.server.HTTPServer(('localhost', 3000), MyHTTPRequestHandler).serve_forever)
    socket_thread = threading.Thread(target=socket_server)

    http_thread.start()
    socket_thread.start()

if __name__ == "__main__":
    main()
