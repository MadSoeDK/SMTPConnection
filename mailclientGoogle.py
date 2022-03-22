from socket import *
import ssl
import base64

#msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
CRLF = "\r\n"
header = "Subject: Test\nContent-Type: text/html;\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((mailserver, 587))
clientSocket.send('STARTTLS'.encode())

SSL = ssl.create_default_context()
wrappedSocket = SSL.wrap_socket(clientSocket, server_hostname=mailserver)

def sendCommand(command, rc):
    print(command)
    # Write command to server
    wrappedSocket.send((command + CRLF).encode())

    # Read the response
    response = wrappedSocket.recv(1024).decode('utf-8')

    print(response)

    if int(response[:3]) != rc or response[:3] == 'DAT':
        print(str(rc) + ' reply not received from server')


# Send HELO command and print server response.
heloCommand = 'EHLO' # EHLO for extended SMTP
sendCommand(heloCommand, 250)

login = 'AUTH LOGIN'
sendCommand(login, 334)

username = input("Input username")
sendCommand(username, 334)

psw = input("Input password")
sendCommand(psw, 235)

# Send MAIL FROM command and print server response.
mailFrom = 'MAIL FROM:<'
mailFrom += input("Enter sender: ")
mailFrom += '>'
sendCommand(mailFrom, 250)

# Send RCPT TO command and print server response.
rcptTo = 'RCPT TO:<'
rcptTo += input("Enter recipient: ")
rcptTo += '>'
sendCommand(rcptTo, 250)

# Send DATA command and print server response.
data = 'DATA'
sendCommand(data, 354)

msg = input("Enter your message: ")

clientSocket.send((header + (msg + CRLF) + endmsg).encode())
#clientSocket.send(endmsg.encode())

resp = clientSocket.recv(1024).decode()
print(resp)

# Send QUIT command and get server response.
quit = 'QUIT'
sendCommand(quit, 250)