import RPi.GPIO as GPIO
buzzerPin = 11  # define buzzerPin


def setup():
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    GPIO.setup(buzzerPin, GPIO.OUT)  # set buzzerPin to OUTPUT mode



def loop():
    while True:
        answer = input("Allumer le buzzer? V ou F :")
        if answer == "V":  # if button is pressed
            GPIO.output(buzzerPin, GPIO.HIGH)  # turn on buzzer
            print('buzzer turned on >>>')
        else:  # if button is relessed
            GPIO.output(buzzerPin, GPIO.LOW)  # turn off buzzer
            print('buzzer turned off <<<')


def destroy():
    GPIO.cleanup()  # Release all GPIO


if __name__ == '__main__': # Program entrance
    print('Program is starting...')
setup()
try:
    loop()
except KeyboardInterrupt:  # Press ctrl-c to end the program.
    destroy()
