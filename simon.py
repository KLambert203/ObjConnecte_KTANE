import random
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
import paho.mqtt.subscribe as sub

red = 13
yellow = 19
green = 6
blue = 26
beeper = 18
pwr_indicator = 27
red_btn = 17
yellow_btn = 5
green_btn = 4
blue_btn = 22
pattern = []
max_pattern_length = 3
lights = [red, yellow, green, blue]
module_is_active = False
server_ip_addr = "10.4.1.43"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(beeper, GPIO.OUT)
GPIO.setup(pwr_indicator, GPIO.OUT)
GPIO.setup(red_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yellow_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(blue_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(yellow, GPIO.LOW)
GPIO.output(red, GPIO.LOW)
GPIO.output(green, GPIO.LOW)
GPIO.output(blue, GPIO.LOW)
GPIO.output(pwr_indicator, GPIO.LOW)
client = paho.Client(client_id="simon", clean_session=False)
client.connect(server_ip_addr, 1883, 60)


def game_success():
    x = 0
    while x <= 5:
        GPIO.output(blue, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(blue, GPIO.LOW)

        GPIO.output(yellow, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(yellow, GPIO.LOW)

        GPIO.output(red, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(red, GPIO.LOW)

        GPIO.output(green, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(green, GPIO.LOW)

        x = x + 1


def game_over():
    x = 0
    while x <= 5:
        GPIO.output(blue, GPIO.HIGH)
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(yellow, GPIO.HIGH)
        GPIO.output(beeper, GPIO.HIGH)
        time.sleep(0.05)

        GPIO.output(blue, GPIO.LOW)
        GPIO.output(red, GPIO.LOW)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(yellow, GPIO.LOW)
        GPIO.output(pwr_indicator, GPIO.LOW)
        GPIO.output(beeper, GPIO.LOW)
        time.sleep(0.05)

        x = x + 1


def flash(color):
    GPIO.output(lights[color], GPIO.HIGH)
    GPIO.output(beeper, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(beeper, GPIO.LOW)
    time.sleep(0.8)
    GPIO.output(lights[color], GPIO.LOW)


def game():
    alive = True
    pattern.clear()

    while alive:
        pattern.append(random.randint(0, 3))
        print(pattern)

        if pattern.__len__() > max_pattern_length:
            return True

        for color in pattern:
            flash(color)

        for color in pattern:
            waiting_for_input = True

            while waiting_for_input:
                red_btn_state = GPIO.input(red_btn)
                yellow_btn_state = GPIO.input(yellow_btn)
                green_btn_state = GPIO.input(green_btn)
                blue_btn_state = GPIO.input(blue_btn)

                if red_btn_state == 0:
                    flash(color)
                    waiting_for_input = False
                    if color != 0:
                        return False

                if yellow_btn_state == 0:
                    flash(color)
                    waiting_for_input = False
                    if color != 1:
                        return False

                if green_btn_state == 0:
                    flash(color)
                    waiting_for_input = False
                    if color != 2:
                        return False

                if blue_btn_state == 0:
                    flash(color)
                    waiting_for_input = False
                    if color != 3:
                        return False


while True:
    module_is_active = str(sub.simple("game/modules/Simon/isActive", hostname=server_ip_addr).payload, "utf-8")
    GPIO.output(pwr_indicator, GPIO.LOW)

    if module_is_active == "True":
        GPIO.output(pwr_indicator, GPIO.HIGH)

        if game():
            game_success()
            client.publish("game/modules/Simon/Success", payload=True, qos=1, retain=True)
            client.publish("game/modules/Simon/isActive", payload=False, qos=1, retain=True)
        else:
            game_over()
            client.publish("game/modules/Simon/Fail", payload=True, qos=1, retain=True)
