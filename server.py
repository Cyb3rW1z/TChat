import threading
import socket


host = "127.0.0.1"
port = 9876

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
usernames = []
passwords = []
users = {}


def sending(message):
    for client in clients:
        client.send(message)


def manage(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('/ban'):
                print(msg.decode('ascii')[5:])
                name_to_ban = msg.decode('ascii')[5:]
                if name_to_ban != 'boss':
                    name_index = usernames.index(name_to_ban)
                    client_to_kick = clients[name_index]
                    clients.remove(client_to_kick)
                    client_to_kick.send('You Were Kicked from Chat !'.encode('ascii'))
                    client_to_kick.close()
                    usernames.remove(name_to_ban)
                    sending(f'{name_to_ban} was kicked from the server!'.encode('ascii'))
                    with open('bans.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')
                        print(f'{name_to_ban} was banned by the BOSS!')
                else:
                    client.send('Command Refused!'.encode('ascii'))
            else:
                sending(message)

        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = usernames[index]
                sending(f'{nickname} left the Chat!'.encode('ascii'))
                usernames.remove(nickname)
                break


def receive():
    while True:
        client, address = server.accept()
        client.send('R to Register, or L to login:'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        if nickname + '\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
        if nickname + '\n' in usernames:
            client.send('Username Exists'.encode('ascii'))
            client.close()
            continue

        client.send('Welcome to the chat'.encode('ascii'))

        usernames.append(nickname)
        clients.append(client)
        users[address] = nickname

        print(f'Nickname of the client is {nickname}')
        sending(f'{nickname} joined the Chat'.encode('ascii'))
        client.send('Connected to the Server!'.encode('ascii'))

        thread = threading.Thread(target=manage, args=(client,))
        thread.start()


print('Server is Listening ...')
receive()
