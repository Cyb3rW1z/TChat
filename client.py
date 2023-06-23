import socket
import threading
import hashlib

un1 = ''
password = ''

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9876))
stop_thread = False

users = {}


def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')

            if message == 'R to Register, or L to login:':
                uname, pass1 = logging()
            else:
                print(message)
        except:
            print('Error Occurred while Connecting')
            client.close()
            exit()
            break


def logging():
    while True:
        option = input('R to Register, L to login')
        if option == 'R':
            print("Choose a Proper Username and Password:")
            un1 = input('Please, Enter Your Username:')
            pw1 = input("Please, Enter Your Password:")
            pw1 = hashlib.sha256(pw1.encode('ascii')).hexdigest()
            if un1 in users:
                print("User is in Database! Try Again!")
                continue
            pw1 = hashlib.sha256(pw1.encode('ascii')).hexdigest()
            users[un1] = pw1
            f = open('PASSWORDS.txt', 'a+')
            f.write('\n' + un1 + ': ' + users[un1])
            f.close()
            return un1, pw1
        elif option == 'L':
            un1 = input("Please, Enter Your Username:\n")
            pw1 = input("Please, Enter Your Password:\n")
            pw1 = hashlib.sha256(pw1.encode('ascii')).hexdigest()
            f = open("PASSWORDS.txt", 'r+')
            content = f.read()
            f.close()
            if un1 not in content:
                print("Username is Not in Database! Try Again!")
                continue
            if un1 in content and pw1 in content:
                if ((content[content.find(un1) + len(un1) + 2:content.find(pw1) + len(pw1)]) == pw1):
                    return un1, pw1
        else:
            print("Wrong Input, Try Again!")
            continue
        print("Sorry Wrong Input!")
        client.close()
        exit()


def write(un2, p1):
    while True:
        if stop_thread:
            break
        in1 = input("")
        message = f'{un2}: {in1}'
        if in1.startswith('/ban'):
            print(un2)
            if un2 == 'boss':
                client.send(in1.encode('ascii'))
            else:
                print("Ban is executed by Boss only !!")
        else:
            client.send(message.encode('ascii'))


msg = client.recv(1024).decode('ascii')
if msg == 'R to Register, or L to login:':
    un, pw = logging()
    client.send(un.encode('ascii'))
access = (client.recv(1024)).decode('ascii')
print(access)
if access == 'BAN':
    client.close()
    exit()


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write, args=(un, pw,))
write_thread.start()
