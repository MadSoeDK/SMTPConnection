import base64
import ssl
from socket import *

bhsi_mailserver = 'smtp2.bhsi.xyz'
bhsi_port = 2526

google_mailserver = 'smtp.gmail.com'
google_port = 587


def main():
    while True:
        option = input("Send mail? (y/n): ")
        if option == 'y':
            server = input("Gmail or Bhujip mailserver? (g/b): ")
            if server == "g":
                username = input("Enter your Google username (base64): ")
                psw = input("Enter your Google password (base64): ")
                send_google_mail(google_mailserver, google_port, username, psw)
                print("Sending mail via smtp.gmail.com...")
            else:
                send_mail(bhsi_mailserver, bhsi_port)
                print("Sending mail via smtp2.bhsi.xyz...")
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


# Sends an e-mail via Bhujips servers
def send_mail(mailserver, port):
    msg = input("Message: ")
    msg = create_body(msg)

    image_path = input("Image attachment (path): ")

    if image_path != '':
        msg = msg + image_attachment(msg, image_path)

    # SMTP protocol message
    smtp_commands = ["EHLO localhost\r\n",
                     "MAIL FROM: <" + input("Mail from:") + ">\r\n",
                     "RCPT TO: <" + input("Mail to: ") + ">\r\n",
                     "DATA\r\n",
                     f"{msg}\r\n",
                     ".\r\n",
                     "QUIT\r\n"]

    clientsocket = createSocket(mailserver, port)

    # Send commands
    for i in range(len(smtp_commands)):
        clientsocket.send(smtp_commands[i].encode())
        if i == 4:
            clientsocket.send(smtp_commands[i + 1].encode())
        clientsocket.recv(2048)


# Sends an e-mail via Google servers
def send_google_mail(mailserver, port, username, psw):
    msg = input("Message: ")
    msg = create_body(msg)

    image_path = input("Image attachment (path): ")

    if image_path != '':
        msg = msg + image_attachment(msg, image_path)

    # SMTP protocol message
    smtp_commands = ["EHLO localhost\r\n",
                     "STARTTLS\r\n",
                     "AUTH LOGIN\r\n",
                     username + "\r\n", psw + "\r\n",
                     "MAIL FROM: <" + input("Mail from: ") + ">\r\n",
                     "RCPT TO: <" + input("Mail to: ") + ">\r\n",
                     "DATA\r\n",
                     f"{msg}\r\n",
                     ".\r\n",
                     "QUIT\r\n"]

    clientsocket = createSocket(mailserver, port)

    # Prepare for TLS
    for i in range(2):
        clientsocket.send(smtp_commands[i].encode())
        clientsocket.recv(2048)

    # TLS Connection
    ctx = ssl.create_default_context()
    clientsocket = ctx.wrap_socket(clientsocket, server_hostname=mailserver)

    # Authenticate and send mail
    for i in range(2, len(smtp_commands)):
        clientsocket.send(smtp_commands[i].encode())
        clientsocket.recv(2048)


# Encapsulates the messages in headers
def create_body(msg):
    body = f'Subject: E-mail\n' \
               f'Content-Type: text/plain; charset="UTF-8\n' \
               f'Content-Transfer-Encoding: quoted-printable\n' \
               f'\n' \
               f'{msg}\n' \
               f'\n'

    return body


def image_to_base64(image_path):
    with open(image_path, "rb") as imgFile:
        return base64.b64encode(imgFile.read())


def base64_string_converter(string):
    string_in_bytes = string.encode('utf-8')
    string_in_base64 = base64.b64encode(string_in_bytes)
    result_as_string = string_in_base64.decode('utf-8')
    return result_as_string


def base_64_to_string(bytes_to_conv):
    return bytes_to_conv.decode('utf-8')


def image_attachment(body, image_path):
    image_base64 = base_64_to_string(image_to_base64(image_path))
    msg = f'Content-Type: multipart/mixed; boundary="===============0814515963129319972=="\n' \
          f'MIME-Version: 1.0\n'

    # Text plain
    msg = msg + f'--===============0814515963129319972==\n' \
                f'Content-Type: text/plain; charset="utf-8"\n' \
                f'Content-Transfer-Encoding: quoted-printable\n' \
                f'\n' \
                f'{body}\n' \
                f'\n'

    # Image attachment
    if image_path != '':
        msg = msg + '--===============0814515963129319972==\n' \
                    'Content-Type: image/octet_stream\n' \
                    'MIME-Version: 1.0\n' \
                    'Content-Transfer-Encoding: base64\n' \
                    f'Content-Disposition: attachment; filename="{image_path}"\n' \
                    '\n' \
                    f'{image_base64}==\n' \
                    '\n' \

    # End of message
    msg = msg + f'--===============0814515963129319972==--'

    return msg


main()
