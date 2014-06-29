#!/usr/bin/env python3

import socket

HOST = '131.urlab.be'
PORT = 6600


def parse(response):
    result = {}
    for line in response:
        if ':' in line:
            name, value = line.split(': ', 1)
            result[name] = value
    return result


def readline(s):
    buffer = ''
    while True:
        buffer += s.recv(1).decode()
        if buffer.endswith('\n'):
            return buffer[:-1]


def get_response(s):
    response = {}
    line = readline(s)
    while not line.startswith('OK'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            response[key] = value
        else:
            print('WEIRD', [line])
        line = readline(s)
    return response


def play(s):
    s.send(b'play\n')
    return get_response(s)


def pause(s):
    s.send(b'pause\n')
    return get_response(s)


def next(s):
    s.send(b'next\n')
    return get_response(s)


def currentsong(s):
    s.send(b'currentsong\n')
    return get_response(s)


def volume(s, valeur):
    s.send(b'volume {}\n'.format(valeur))
    return get_response(s)


def status(s):
    s.send(b'status\n')
    return get_response(s)


def main():
    s = socket.socket()
    s.connect((HOST, PORT))
    get_response(s)

    while True:
        order = input('Que faire ? ')
        if order == 'play':
            play(s)
        elif order == 'pause':
            pause(s)
        elif order == 'suivant':
            next(s)
        elif order == 'morceau':
            print(currentsong(s)['Title'])
        elif order == 'artiste':
            print(currentsong(s)['Artist'])
        elif order == 'position':
            print(status(s)['elapsed'])
        elif order in ('repetition', 'répétition'):
            print(status(s)['repeat'])



if __name__ == '__main__':
    main()
