#!/usr/bin/env python3

import inspect
import sys

#from nutils import watch
__all__ = ["msg", "msg_wng", "msg_err", "msg_exc", "NException"]

def msg(text, tag=""):
    """Print message
    """

    print()
    msgL = text.splitlines()
    for line in msgL:
        print("{0} {1}".format(tag, line))

def msg_wng(text, tag="WNG:", info=False):
    ind = 2
    if len(inspect.stack()) == ind:
        ind = -1
    st = inspect.stack()[ind]

    if info:
        fn = st[1]
        ln = st[2]
        text += "\nFile: {} line: {}".format(fn, ln)

    msg(text, tag=tag)

def msg_err(text, tag="ERR:", sts=1, info=False):
    msg_wng(text, tag=tag, info=info)
    sys.exit(sts)

class NException(Exception):
    pass

def msg_exc(text):
    raise NException(text)
