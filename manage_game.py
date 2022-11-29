#!/usr/bin/env python3
########################################################################
# Filename    : MatrixKeypad.py
# Description : obtain the key code of 4x4 Matrix Keypad
# Author      : freenove
# modification: 2018/08/03
########################################################################
import GameManager
import threading

manager = GameManager.GameManager("10.4.1.43", 1883, [])
manager.game_modules = ["Keypad", "Simon"]

def start_game(input_choice):
    if input_choice == "S":
        print("Game has started. Timer set to 3 minutes!")
        print("Good luck!")
        manager.start_game()
        manager.manage_game()
    elif input_choice == "E":
        print("Game has ended. Thanks for playing!")
        manager.end_game()
        exit(0)
    else:
        print("Command not recognized.")


def loop():
    print("Press S to start game.")
    print("Press E to end game.")
    while True:
        start_game(input())



if __name__ == '__main__':  # Program start from here
    print("Program is starting ... ")
    try:
        loop()
        manager.end_game()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, exit the program.
        print("Game has ended")