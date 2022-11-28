import socket
import threading

HOST = '127.0.0.1'
PORT = 1234   #port can be any number between 0 - 65535
LISTENER_LIMIT = 5
active_clients = []

def listen_for_msg(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != "":
            final_msg = username + " -> " + message
            send_message_to_all(final_msg)
        else:
            print(f"the message send from {username} is empty")

# send msg to single client
def send_message_to_client(client, message):
    client.sendall(message.encode())


# send the msg to all the client
def send_message_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# function to handle client
def client_handler(client):

    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != "":
            active_clients.append((username, client))
            prompt_msg = "SERVER -> "+f"{username} added to the chat"
            send_message_to_all(prompt_msg)
            break
        else:
            print("client username is empty")

    threading.Thread(target=listen_for_msg, args=(client, username, )).start()


def main():

    #creating the socket class object
    # AF_INET, it specify that we are using ipv4 addressing
    # SOCk_STREAM, we are using tcp packet for communication(for udp-SOCK_DGRAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"running he server on  {HOST}, {PORT}")
    except:
        print(f"unable to connect with host {HOST} and port {PORT}")

    #set server connection limit
    server.listen(LISTENER_LIMIT)

    #keep listening to new connection
    while 1:

        client, address = server.accept()
        print(f"sucessfully connected to {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client,)).start()


if __name__ == "__main__":
    main()
