#!/usr/bin/env python3
########################################################################
# Filename    : MatrixKeypad.py
# Description : obtain the key code of 4x4 Matrix Keypad
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
from keypad import Keypad # import module Keypad
from PCF8574 import PCF8574_GPIO
from ADAFruit_LCD1602 import Adafruit_CharLCD


PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F

try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print('I2C Address Error !')
        exit(1)

lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)

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
    mcp.output(3, 1)  # turn on LCD backlight
    lcd.begin(16, 2)  # set number of LCD lines and columns
    stringArray = []
        # lcd.clear()
    string = ""
    while (True):
        key = keypad.getKey()  # obtain the state of keys
        if (key != keypad.NULL):  # if there is key pressed, print its key code.
            lcd.setCursor(0, 0)  # set cursor position
            stringArray.append(str(key))
            string = ""
            for a in stringArray:
                string += str(a)
            lcd.clear()
            lcd.message(string + '\n')  # display CPU temperature



if __name__ == '__main__':  # Program start from here
    print("Program is starting ... ")
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, exit the program.
        GPIO.cleanup()
    finally:
        lcd.clear()
