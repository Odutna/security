# -*- coding:utf-8 -*-
import functools


def hexdump(src, length=16):
    # http://code.activestate.com/recipes/142812-hex-dumper/
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = bytes(' '.join(["%0*X" % (digits, ord(x)) for x in s]), 'utf-8')
        text = bytes(''.join([x if 0x20 <= ord(x) < 0x7F else '.' for x in s]), 'utf-8')
        result.append("%04X  %-*s  %s" % (i, length*(digits + 1), hexa, text))
    print('\n'.join(result))


def until_interrupt(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            while True:
                function(*args, **kwargs)
        except KeyboardInterrupt:
            print('Interrupted.')
    return wrapper
