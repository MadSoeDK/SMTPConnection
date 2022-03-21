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
SSL = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
wrappedSocket = SSL.wrap_socket(clientSocket)

wrappedSocket.connect((mailserver, 465))

recv = wrappedSocket.recv(2048)
print(recv)

def sendCommand(command, rc):
    #print(command)
    # Write command to server
    wrappedSocket.send(base64.b64encode((command + CRLF).encode('utf-8')))


    # Read the response
    response = wrappedSocket.recv(1024).decode('utf-8')

    print(base64.b64decode(response))

    if int(response[:3]) != rc or response[:3] == 'DAT':
        print(str(rc) + ' reply not received from server')


# Send HELO command and print server response.
heloCommand = 'EHLO localhost' # EHLO for extended SMTP
sendCommand(heloCommand, 250)

login = 'AUTH LOGIN'
sendCommand(login, 334)

username = 'c29lcmVuc2VubWFkczJAZ21haWwuY29t'
sendCommand(username, 334)

psw = 'TWFkczE1MDQh'
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