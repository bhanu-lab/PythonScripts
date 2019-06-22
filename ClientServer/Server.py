import socket


def run_server():
    # 1.get host address and port number
    host = socket.gethostname()
    port = 12345

    # 2.create a socket
    server_socket = socket.socket()

    # 3.bind host  address and port number to socket create abaove
    server_socket.bind((host, port))

    # 4.listen number of clients
    server_socket.listen(3)

    # 5.accept connections which retunns connection and from ip adrress
    conn, address = server_socket.accept()

    print("connecction recevied from : "+ str(address))

    while True:

        # read data from connecction established
        data = conn.recv(1024).decode()
        if not data :
            break

        print("from conneccted user : "+str(data))

        # send data from server to client
        data = input('->') # read input from console
        conn.send(data.encode())
    conn.close()


if __name__ == '__main__':
    run_server()

