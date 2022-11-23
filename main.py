#!/usr/bin/env python3
########################################################################
# Filename    : MatrixKeypad.py
# Description : obtain the key code of 4x4 Matrix Keypad
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
from LCD_Service import LCD
import asyncio
lcd_service = LCD()

def main():
    print("Program is starting ... ")
    try:
        lcd_service.run()

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, exit the program.
        GPIO.cleanup()
    finally:
        lcd_service.clear()

if __name__ == '__main__':
    main()
