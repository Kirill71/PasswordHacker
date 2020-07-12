import argparse
import socket


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", type=str)
    parser.add_argument('port', type=int)
    parser.add_argument('message', type=str)
    return parser.parse_args()


def main():
    args = parse_args()
    buffer_size = 1024
    with socket.socket() as client:
        address = (args.hostname, args.port)
        client.connect(address)
        client.send(args.message.encode())
        response = client.recv(buffer_size)
        print(response.decode())


if __name__ == '__main__':
    main()

