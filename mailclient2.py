from socket import *
#msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
CRLF = "\r\n"
header = "Content-Type: text/html;"
header += "Subject: Test"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp2.bhsi.xyz'

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 2525))

recv = clientSocket.recv(1024)
print(recv)

def sendCommand(command, rc):
    print(command)
    # Write command to server
    clientSocket.send((command + CRLF).encode())

    # Read the response
    response = clientSocket.recv(1024).decode()

    print(response)

    if int(response[:3]) != rc:
        print(str(rc) + ' reply not received from server')


# Send HELO command and print server response.
heloCommand = 'HELO' # EHLO for extended SMTP
sendCommand(heloCommand, 250)

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

msg = header
msg += '\r\n'
msg += input("Enter your message: ")

clientSocket.send((msg).encode())
clientSocket.send(endmsg.encode())

resp = clientSocket.recv(1024).decode()
print(resp)

# Send QUIT command and get server response.
quit = 'QUIT'
sendCommand(quit, 221)

