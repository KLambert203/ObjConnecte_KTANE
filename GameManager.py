import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import time


class GameManager:
    def __init__(self, broker_ip, listener_port, game_modules):
        self.broker_ip = broker_ip
        self.listener_port = listener_port
        self.game_modules = game_modules
        self.mqttc = paho.Client(client_id="manager", clean_session=False)

    def start_game(self):
        self.connect_to_broker()
        self.mqttc.publish("game/lives", 3, 1, True)

    def connect_to_broker(self):
        self.mqttc.connect(self.broker_ip, port=self.listener_port, keepalive=60, bind_address="")

    def activate_module(self, module):
        path = "modules/" + module + "active"
        self.mqttc.publish(path, True, 1, True)

    def deactivate_module(self, module):
        path = "modules/" + module + "active"
        self.mqttc.publish(path, False, 1, True)

    def decrease_number_of_lives(self):
        current_lives = subscribe.simple("game/lives", hostname=self.broker_ip)
        updated_lives = current_lives - 1
        self.mqttc.publish("game/lives", updated_lives, 1, True)
