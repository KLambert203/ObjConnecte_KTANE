from keypad import Keypad
from PCF8574 import PCF8574_GPIO
from ADAFruit_LCD1602 import Adafruit_CharLCD
import time

class LCD:
    def __init__(self):
        self.lcd = self.init_chips()
        self.keypad = self.init_keypad()
        self.timeformat = None

    def init_chips(self):
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

        return Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp), mcp

    def init_keypad(self):
        rows = 4  # number of rows of the Keypad
        cols = 4  # number of columns of the Keypad
        keys = ['1', '2', '3', 'A',  # key code
                '4', '5', '6', 'B',
                '7', '8', '9', 'C',
                '*', '0', '#', 'D']
        rows_pins = [36, 38, 40, 29]
        cols_pins = [31, 33, 35, 37]
        return Keypad(keys, rows_pins, cols_pins, rows, cols)

    def loop(self):
        self.keypad.setDebounceTime(50)
        self.lcd[1].output(3, 1)
        self.lcd[0].begin(16, 2)
        string_array = []
        while True:
            key = self.keypad.getKey()
            self.lcd[0].setCursor(0, 0)
            self.lcd[0].message(self.timeformat)
            if key != self.keypad.NULL:
                string_array.append(str(key))
                string = ""
                for a in string_array:
                    string += str(a)

                self.lcd[0].message('\n' + string)



    def start_timer(self, sec):
        while sec:
            minute, second = divmod(sec, 60)
            self.timeformat = '{:02d}:{:02d}'.format(minute, second)
            print('\r' + self.timeformat)
            time.sleep(1)
            sec -= 1

    def clear(self):
        self.lcd[0].clear()


