import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import time


class GameManager:
    def __init__(self, broker_ip, listener_port, game_modules):
        self.broker_ip = broker_ip
        self.listener_port = listener_port
        self.game_modules = game_modules
        self.mqttc = paho.Client(client_id="manager", clean_session=False)
        self.module_index = 0

    def start_game(self):
        self.connect_to_broker()
        self.mqttc.publish("game/hasBeenWon", False, 2, True)
        self.mqttc.publish("game/lives", 3, 1, True)
        self.mqttc.publish("game/isStarted", True, 1, True)
        self.mqttc.publish("game/timer", 180, 1, True)
        self.activate_module(self.game_modules[self.module_index])
        self.deactivate_module(self.game_modules[self.module_index + 1])
        for module in self.game_modules:
            path = "game/modules/" + module + "/Fail"
            self.mqttc.publish(path, False, 1, True)

    def end_game(self):
        self.mqttc.publish("game/lives", 3, 1, True)
        self.mqttc.publish("game/isStarted", False, 1, True)
        for module in self.game_modules:
            path = "game/modules/" + module + "/isActive"
            self.mqttc.publish(path, False, 1, True)


    def connect_to_broker(self):
        self.mqttc.connect(self.broker_ip, port=self.listener_port, keepalive=60, bind_address="")

    def activate_module(self, module):
        path1 = "game/modules/" + module + "/isActive"
        path2 = "game/modules/" + module + "/Fail"
        self.mqttc.publish(path1, True, 1, True)
        self.mqttc.publish(path2, False, 1, True)

    def deactivate_module(self, module):
        path1 = "game/modules/" + module + "/isActive"
        path2 = "game/modules/" + module + "/Fail"
        self.mqttc.publish(path1, False, 1, True)
        self.mqttc.publish(path2, False, 1, True)

    def decrease_number_of_lives(self):
        current_lives = int(subscribe.simple("game/lives", hostname=self.broker_ip).payload)
        updated_lives = current_lives - 1
        self.mqttc.publish("game/lives", updated_lives, 1, True)

    def win_module(self):
        if self.module_index + 1 > len(self.game_modules):
            self.win_game()
        won_module = "game/modules/" + self.game_modules[self.module_index] + "/isActive"
        new_module = "game/modules/" + self.game_modules[self.module_index + 1] + "/isActive"
        self.module_index += 1
        self.mqttc.publish(won_module, False, 1, True)
        self.mqttc.publish(new_module, True, 1, True)

    def win_game(self):
        self.mqttc.publish("game/hasBeenWon", True, 2, True)
        print("Congratulations! You have won the game!")
        self.end_game()