from socket import *

# Choose a mail server (e.g. Google mail server) and call it mailserver
bhsi_mailserver = 'smtp2.bhsi.xyz'
bhsi_port = 2526

google_mailserver = 'smtp.gmail.com'
google_port = 587


def main():
    while True:
        option = input("Send mail? (y/n)")
        if option == 'y':
            send_mail()
        else:
            print("Quitting...")
            break


def createSocket(mailserver, port):
    # AF_INET refers to the address-family ipv4.
    # The SOCK_STREAM means connection-oriented TCP protocol.
    # ----------------------------------------------------------
    # Create socket called clientSocket and
    # establish a TCP connection with mailserver
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, port))
    clientSocket.recv(2048)

    return clientSocket


def send_mail():
    msg = input("Message: ")
    msg = create_make_body_mailable(msg)

    # SMTP protocol message
    smtp_commands = ["EHLO localhost\r\n",
                     "MAIL FROM: <" + input("Mail from:") + ">\r\n",
                     "RCPT TO: <" + input("Mail to: ") + ">\r\n",
                     "DATA\r\n",
                     f"{msg}\r\n",
                     ".\r\n",
                     "QUIT\r\n"]

    clientsocket = createSocket(bhsi_mailserver, bhsi_port)

    # Send commands
    for i in range(len(smtp_commands)):
        clientsocket.send(smtp_commands[i].encode())
        if i == 4:
            clientsocket.send(smtp_commands[i + 1].encode())
        clientsocket.recv(2048)


def create_make_body_mailable(body):
    new_body = f'000000000000382db0057f0910d5"\n' \
               f'Content-Type: text/plain; charset="UTF-8"\n' \
               f'Content-Transfer-Encoding: quoted-printable\n' \
               f'\n' \
               f'{body}\n' \
               f'\n' \
               f'000000000000382db0057f0910d5'

    return new_body


main()
