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
        print("Game starting")
        self.mqttc.publish("game/hasBeenWon", False, 2, True)
        self.mqttc.publish("game/lives", 3, 1, True)
        self.mqttc.publish("game/isStarted", True, 1, True)
        self.mqttc.publish("game/timer", 180, 1, True)
        self.activate_module(self.game_modules[self.module_index])
        if len(self.game_modules) > 1:
            self.deactivate_module(self.game_modules[self.module_index + 1])
        for module in self.game_modules:
            path = "game/modules/" + module + "/Fail"
            self.mqttc.publish(path, False, 1, True)

    def end_game(self):
        self.connect_to_broker()
        print("Game is ending")
        self.mqttc.publish("game/isStarted", False, 1, True)
        for module in self.game_modules:
            path = "game/modules/" + module + "/isActive"
            self.mqttc.publish(path, False, 1, True)
        exit(0)

    def game_over(self):
        print("You have lost! Game Over!")
        self.end_game()

    def manage_game(self):
        while True:
            current_module = self.game_modules[self.module_index]
            self.is_there_still_lives_left()
            self.is_there_still_time_left()
            self.is_module_in_failure(current_module)
            self.has_module_been_won(current_module)
            time.sleep(0.5)

    def connect_to_broker(self):
        self.mqttc.connect(self.broker_ip, port=self.listener_port, keepalive=60, bind_address="")

    def activate_module(self, module):
        path1 = "game/modules/" + module + "/isActive"
        path2 = "game/modules/" + module + "/Fail"
        path3 = "game/modules/" + module + "/Success"
        self.mqttc.publish(path1, True, 1, True)
        self.mqttc.publish(path2, False, 1, True)
        self.mqttc.publish(path3, False, 1, True)

    def deactivate_module(self, module):
        path1 = "game/modules/" + module + "/isActive"
        path2 = "game/modules/" + module + "/Fail"
        self.mqttc.publish(path1, False, 1, True)
        self.mqttc.publish(path2, False, 1, True)

    def decrease_number_of_lives(self):
        current_lives = int(subscribe.simple("game/lives", hostname=self.broker_ip).payload)
        updated_lives = current_lives - 1
        print("updated_lives : " + str(updated_lives))
        self.mqttc.publish("game/lives", updated_lives, 1, True)

    def has_module_been_won(self, module):
        module_status = str(subscribe.simple("game/modules/" + module + "/Success", hostname=self.broker_ip).payload)
        if module_status == "b'True'":
            self.win_module(module)
            path = "game/modules/" + module + "/Fail"
            self.mqttc.publish(path, False, 1, True)

    def is_module_in_failure(self, module):
        path = "game/modules/" + module + "/Fail"
        module_status = str(subscribe.simple(path, hostname=self.broker_ip).payload)
        if module_status == "b'True'":
            self.is_there_still_lives_left()
            self.decrease_number_of_lives()
            path = "game/modules/" + module + "/Fail"
            self.mqttc.publish(path, False, 1, True)

    def win_module(self, module):
        if self.module_index + 1 > len(self.game_modules):
            self.win_game()
            return 0
        self.module_index += 1
        self.deactivate_module(module)
        self.activate_module(module)

    def win_game(self):
        self.mqttc.publish("game/hasBeenWon", True, 2, True)
        print("Congratulations! You have won the game!")
        self.end_game()

    def is_there_still_lives_left(self):
        number_of_lives = int(subscribe.simple("game/lives", hostname=self.broker_ip).payload)
        if number_of_lives == 0:
            self.game_over()

    def is_there_still_time_left(self):
        time_left = int(subscribe.simple("game/timer", hostname=self.broker_ip).payload)
        if time_left <= 0:
            print("Out of time!")
            self.game_over()
