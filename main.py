#!/usr/bin/env python3
########################################################################
# Filename    : MatrixKeypad.py
# Description : obtain the key code of 4x4 Matrix Keypad
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
from keypad import Keypad # import module Keypad

ROWS = 4  # number of rows of the Keypad
COLS = 4  # number of columns of the Keypad
keys = ['1', '2', '3', 'A',  # key code
        '4', '5', '6', 'B',
        '7', '8', '9', 'C',
        '*', '0', '#', 'D']
rowsPins = [36, 38, 40, 29]
colsPins = [31, 33, 35, 37]


def loop():
    keypad = Keypad(keys, rowsPins, colsPins, ROWS, COLS)  # creat Keypad object
    keypad.setDebounceTime(50)  # set the debounce time
    while (True):
        key = keypad.getKey()  # obtain the state of keys
        if (key != keypad.NULL):  # if there is key pressed, print its key code.
            print("You Pressed Key : %c " % (key))


if __name__ == '__main__':  # Program start from here
    print("Program is starting ... ")
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, exit the program.
        GPIO.cleanup()