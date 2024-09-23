
from PyQt6 import QtCore


import socket
import json
import time

def check_server(ip, port):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    server_address = (ip, port)
    try:
        client_socket.connect(server_address)
        command = {
            'cmd': 'connect'
        }
        client_socket.sendall(json.dumps(command).encode())
        response = client_socket.recv(4069)
        response = json.loads(response.decode())
        if response['result'] == 'success':
            return True
        else:
            return False
    except Exception as e:
        return False
    

def get_clients(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    client_socket.connect(server_address)
    # Send command to the server
    command = {
        'cmd': 'ls_clients'
    }
    client_socket.sendall(json.dumps(command).encode())
    # Receive response from server
    response = client_socket.recv(4096)
    response = json.loads(response.decode())
    return response['result']


def send_command(client_socket, command):

# Send a message to the server
    try:

        """ command = {
            'cmd': 'python',
            'clients': ['118.70.190.129'],
            'code': 'import webbrowser; webbrowser.open("https://www.google.com")'
        }
        
        client_socket.sendall(json.dumps(command).encode()) """
        
        
        client_socket.shutdown(socket.SHUT_WR)
        
    finally:
        client_socket.close()
    
    


class LoadClientsThread(QtCore.QThread):
    clients = QtCore.pyqtSignal(list)
    old_clients = []
    def __init__(self, ip_socket, port_socket):
        self.ip_socket = ip_socket
        self.port_socket = port_socket
        super().__init__()
    def run(self):
        self.main()
        
    def main(self):
        while True:
            clients = get_clients(self.ip_socket, int(self.port_socket))
            if clients != self.old_clients:
                self.old_clients = clients
                self.clients.emit(clients)
                time.sleep(2)
            else:
                time.sleep(2)