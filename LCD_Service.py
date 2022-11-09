from keypad import Keypad
from PCF8574 import PCF8574_GPIO
from ADAFruit_LCD1602 import Adafruit_CharLCD
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time

class LCD:
    def __init__(self):
        self.lcd = self.init_chips()
        self.keypad = self.init_keypad()
        self.time_format = None
        self.lives = None

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
            self.lcd[0].message(self.time_format)
            self.lcd[0].setCursor(13, 0)
            self.lcd[0].message(self.lives)

            if key != self.keypad.NULL:
                string_array.append(str(key))
                string = ""
                for a in string_array:
                    string += str(a)
                self.lcd[0].message('\n' + string)
                print(len(string))
                if len(string) > 4:
                    if string == "1234":
                        print("win")
                    self.lcd[0].clear()
                    string_array.clear()
                    string = ""



    def start_timer(self, sec):
        while sec:
            minute, second = divmod(sec, 60)
            self.time_format = '{:02d}:{:02d}'.format(minute, second)
            time.sleep(1)
            sec -= 1

    def life(self):
        client = mqtt.Client("Display", False)
        client.connect("10.4.1.43", 1883, 60, "")
        while True:
            self.lives = subscribe.simple("game/lives", "10.4.1.43", qos=0)
            time.sleep(0.5)

    def clear(self):
        self.lcd[0].clear()


