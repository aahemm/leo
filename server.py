import threading
import socket
import argparse
import os
from db_control import DBController

class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connections = {}
        
    def start_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(1)
        print('listening at ', sock.getsockname())
        
        while True:
            server_socket, socket_name = sock.accept()
            self.connections[socket_name] = server_socket
            print(socket_name, 'connected')
            
            server_socket_thread = ServerSocketThread(server_socket, socket_name, self)
            server_socket_thread.start()
        sock.close()
            
    def remove_connection(self, socket_name):
        self.connections.pop(socket_name)
        print(self.connections)
        
        
class ServerSocketThread(threading.Thread):
    def __init__(self, server_socket, client_socket_name, server):
        super().__init__()
        self.server_socket = server_socket
        self.client_socket_name = client_socket_name
        self.server = server
        self.db_controller = DBController()
            
    def run(self):
        while True:
            message = self.server_socket.recv(1024).decode('ascii')
            if message == 'q':
                print(self.client_socket_name, 'left')
                self.server_socket.close()
                self.server.remove_connection(self.client_socket_name)
                break
            elif message == 'db':
                send_msg = self.db_controller.get_messages()
                self.broadcast_message(send_msg.encode('ascii'))
            else:
                self.db_controller.create_msg(message)
                              
    def broadcast_message(self, message):
        connections = self.server.connections
        for conn in connections.keys():
            if conn != self.client_socket_name:
                connections[conn].sendall(message)
                

if __name__ == '__main__':
    server = Server('localhost', 3000)
    server.start_server()