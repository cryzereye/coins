import msvcrt
import os
import sys

def restart():
    clear = lambda: os.system('cls')
    clear()
    os.execl(sys.executable, sys.executable, *sys.argv)

def read_stop():
    while True:
        try:
            if msvcrt.getch() == '~':
                restart()
        except Exception:
            next