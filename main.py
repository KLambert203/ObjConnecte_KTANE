#!/usr/bin/env python3
########################################################################
# Filename    : MatrixKeypad.py
# Description : obtain the key code of 4x4 Matrix Keypad
# Author      : freenove
# modification: 2018/08/03
########################################################################
import GameManager

manager = GameManager.GameManager("10.4.1.43", 1883, [])

def loop():
    manager.start_game()
    while True:
        print("hello world \r")


if __name__ == '__main__':  # Program start from here
    print("Program is starting ... ")
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, exit the program.
        print("Game has ended")