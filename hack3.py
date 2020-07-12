import argparse
import socket
import itertools


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", type=str)
    parser.add_argument('port', type=int)
    return parser.parse_args()


class PasswordHacker:
    BUFFER_SIZE = 1024

    def __init__(self, args, file_name):
        self._args = args
        self._file_name = file_name
        self._client_socket = socket.socket()

    def __del__(self):
        self._client_socket.close()

    @staticmethod
    def _generate_passwords(passwords):
        def gen_word_case_combinations(password):
            return map(''.join, itertools.product(*zip(password.upper(), password.lower())))

        return itertools.chain.from_iterable(gen_word_case_combinations(password) for password in passwords)

    def process(self):
        passwords = []
        with socket.socket() as client:
            address = (self._args.hostname, self._args.port)
            client.connect(address)
            with open('passwords.txt') as content:
                passwords = content.read().split('\n')
                for possible_password in self._generate_passwords(passwords):
                    client.send(possible_password.encode())
                    response = client.recv(self.BUFFER_SIZE)
                    if response.decode() == 'Connection success!':
                        print(possible_password)
                        break


def main():
    args = parse_args()
    hacker = PasswordHacker(args, 'passwords.txt')
    hacker.process()


if __name__ == '__main__':
    main()

