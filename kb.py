import msvcrt
import os
import sys
import coins

def read_stop():
    while True:
        try:
            if msvcrt.getch() == '~':
                clear = lambda: os.system('cls')
                clear()
                os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception:
            next