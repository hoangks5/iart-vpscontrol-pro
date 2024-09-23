import socket
import json
import time

def check_server_socket(ip, port):
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
        response = client_socket.recv(1024)
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
    print('Sending command to server:', command)
    client_socket.sendall(json.dumps(command).encode())
    # Receive response from server
    response = client_socket.recv(1024)
    response = json.loads(response.decode())
    print('Received response from server:', response)
    return response['result']


def send_command(ip, port, file_path_python):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    client_socket.connect(server_address)
    
    
    command = {
        'cmd': 'python',
        'clients': ['DESKTOP-HF75HP8:118.70.190.129'],
        'code': open(file_path_python, 'r').read()
    }

    print('Sending command to server:', command)
    client_socket.sendall(json.dumps(command).encode())
    
   
    
    
