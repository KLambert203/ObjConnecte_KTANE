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
pattern = []
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
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(yellow, GPIO.LOW)
GPIO.output(red, GPIO.LOW)
GPIO.output(green, GPIO.LOW)
GPIO.output(blue, GPIO.LOW)
GPIO.output(pwr_indicator, GPIO.LOW)
client = paho.Client(client_id="simon", clean_session=False)
client.connect(server_ip_addr, 1883, 60)


def game_over():
    pattern.clear()
    client.publish("game/modules/Simon/Fail", payload=True, qos=1, retain=True)
    GPIO.output(blue, GPIO.HIGH)
    GPIO.output(red, GPIO.HIGH)
    GPIO.output(green, GPIO.HIGH)
    GPIO.output(yellow, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(blue, GPIO.LOW)
    GPIO.output(red, GPIO.LOW)
    GPIO.output(green, GPIO.LOW)
    GPIO.output(yellow, GPIO.LOW)
    GPIO.output(pwr_indicator, GPIO.LOW)


def flash(color):
    GPIO.output(lights[color], GPIO.HIGH)
    GPIO.output(beeper, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(beeper, GPIO.LOW)
    time.sleep(0.8)
    GPIO.output(lights[color], GPIO.LOW)


while True:
    module_is_active = str(sub.simple("game/modules/Simon/isActive", hostname=server_ip_addr).payload, "utf-8")
    fail = str(sub.simple("game/modules/Simon/Fail", hostname=server_ip_addr).payload, "utf-8")

    if module_is_active == "True" and fail == "False":
        alive = True
        GPIO.output(pwr_indicator, GPIO.HIGH)

        while alive:
            pattern.append(random.randint(0, 3))
            print(pattern)

            for color in pattern:
                flash(color)

            for color in pattern:
                waitingForInput = True

                while waitingForInput:
                    redButtonState = GPIO.input(17)
                    yellowButtonState = GPIO.input(5)
                    greenButtonState = GPIO.input(4)
                    blueButtonState = GPIO.input(22)

                    if redButtonState == 0:
                        flash(color)
                        waitingForInput = False
                        if color != 0:
                            alive = False

                    if yellowButtonState == 0:
                        flash(color)
                        waitingForInput = False
                        if color != 1:
                            alive = False

                    if greenButtonState == 0:
                        flash(color)
                        waitingForInput = False
                        if color != 2:
                            alive = False

                    if blueButtonState == 0:
                        flash(color)
                        waitingForInput = False
                        if color != 3:
                            alive = False

        game_over()
