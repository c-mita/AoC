import hashlib
import random
import sys
import time
import threading


def print_animation(code_array):
    while True:
        s = "\r"
        x_found = False
        for c in code_array:
            if c == 'x':
                c = chr(random.randrange(0, 26, 1) + ord('a'))
                x_found = True
            s += c
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(0.02)
        if not x_found:
            break

def find_password(door_id, in_array=None):
    length = 8
    passcode = in_array if in_array is not None else ['x'] * 8
    found = 0
    idx = 0
    while found < length:
        md5 = hashlib.md5(door_id + str(idx)).hexdigest()
        if md5[:5] == "00000":
            passcode[found] = md5[5]
            found += 1
        idx += 1
    return passcode

def find_password_2(door_id, in_array=None):
    length = 8
    passcode = in_array if in_array is not None else ['x'] * 8
    found = 0
    idx = 0
    while found < length:
        md5 = hashlib.md5(door_id + str(idx)).hexdigest()
        if md5[:5] == "00000":
            try:
                n = int(md5[5])
                if passcode[n] == 'x':
                    passcode[n] = md5[6]
                    found += 1
            except:
                pass
        idx += 1
    return passcode

def solve_1():
    password = ['x'] * 8
    animation_thread = threading.Thread(None, print_animation, args=(password,))
    animation_thread.start()
    find_password("ojvtpuvg", password)
    animation_thread.join()

def solve_2():
    password = ['x'] * 8
    animation_thread = threading.Thread(None, print_animation, args=(password,))
    animation_thread.start()
    find_password_2("ojvtpuvg", password)
    animation_thread.join()

solve_2()
