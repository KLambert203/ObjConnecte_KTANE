import paho.mqtt.client as paho
import time


class GameManager:
    def __init__(self, broker_ip, listener_port, game_modules):
        self.broker_ip = broker_ip
        self.listener_port = listener_port
        self.game_modules = game_modules

    def connect_to_broker(self):
        mqttc = paho.Client(client_id="pub_test", clean_session=False)
        mqttc.connect(self.broker_ip, port=self.listener_port, keepalive=60, bind_address="")

