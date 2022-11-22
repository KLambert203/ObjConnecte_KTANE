#!/usr/bin/env python3
########################################################################
# Filename    : MatrixKeypad.py
# Description : obtain the key code of 4x4 Matrix Keypad
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
from LCD_Service import LCD
import threading

lcd_service = LCD()

if __name__ == '__main__':
    print("Program is starting ... ")
    try:
        threading.Thread(target=lcd_service.start_timer, args=(60,)).start()
        threading.Thread(target=lcd_service.run, args=()).start()
        threading.Thread(target=lcd_service.loop, args=()).start()


    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, exit the program.
        GPIO.cleanup()
    finally:
        lcd_service.clear()
