import socket

def run_client():

    # 1.declare server host and ipaddress
    host = socket.gethostname()
    port = 12345

    # 2.create client socket
    client_socket = socket.socket()

    # 3.connecct to server
    client_socket.connect((host, port))

    # 4.read message
    message = input(' => ')

    while message.lower().strip() != 'close':

        # 5. send message
        client_socket.send(message.encode())

        # 6.read responsee from server
        data = client_socket.recv(1024).decode()
        print("daata received from server is : "+data)

        message = input(' => ')

    client_socket.close()

if __name__ == '__main__':
    run_client()






















