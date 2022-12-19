import paho.mqtt.client as paho
import time


class GameManager:
    def __init__(self, broker_ip, listener_port, game_modules):
        self.broker_ip = broker_ip
        self.listener_port = listener_port
        self.game_modules = game_modules
        self.mqttc = None
        self.module_index = 0
        self.time_left = 180
        self.number_of_lives = 3
        self.simon_failure = False
        self.simon_success = False
        self.keypad_failure = False
        self.keypad_success = False

    def start_game(self):
        self.connect_to_broker()
        print("Game starting")
        self.mqttc.publish("game/hasBeenWon", False, 2, True)
        self.mqttc.publish("game/lives", 3, 1, True)
        self.mqttc.publish("game/isStarted", True, 1, True)
        self.mqttc.publish("game/timer", 180, 1, True)
        self.mqttc.publish("game/hasBeenWon", False, 1, True)
        self.activate_module(self.game_modules[self.module_index])
        if len(self.game_modules) > 1:
            self.deactivate_module(self.game_modules[self.module_index + 1])
        for module in self.game_modules:
            path = "game/modules/" + module + "/Fail"
            self.mqttc.publish(path, False, 1, True)
        self.module_index = 0

    def end_game(self):
        self.connect_to_broker()
        print("Game is ending")
        self.mqttc.publish("game/isStarted", False, 1, True)
        self.mqttc.publish("game/hasBeenWon", False, 1, True)
        for module in self.game_modules:
            path1 = "game/modules/" + module + "/isActive"
            path2 = "game/modules/" + module + "/Fail"
            path3 = "game/modules/" + module + "/Success"
            self.mqttc.publish(path1, False, 1, True)
            self.mqttc.publish(path2, False, 1, True)
            self.mqttc.publish(path3, False, 1, True)
        time.sleep(1)
        exit(0)

    def game_over(self):
        print("You have lost! Game Over!")
        self.end_game()

    def manage_game(self):
        while True:
            self.mqttc.loop()
            current_module = self.game_modules[self.module_index]
            self.is_there_still_lives_left()
            self.is_there_still_time_left()
            self.is_module_in_failure(current_module)
            self.has_module_been_won(current_module)
            time.sleep(0.5)

    def on_connect(self, client, userdata, flags, rc):
        #print("Connected with result code " + str(rc))
        client.subscribe("game/modules/Simon/Fail")
        client.subscribe("game/modules/Simon/Success")
        client.subscribe("game/modules/Keypad/Fail")
        client.subscribe("game/modules/Keypad/Success")
        client.subscribe("game/timer")
        client.subscribe("game/lives")

    def on_message(self, client, userdata, msg):
        if msg.topic == "game/lives":
            self.number_of_lives = int(msg.payload.decode())
        if msg.topic == "game/timer":
            self.time_left = int(msg.payload.decode())
        if msg.topic == "game/modules/Simon/Fail":
            self.simon_failure = msg.payload.decode()
        if msg.topic == "game/modules/Keypad/Fail":
            self.keypad_failure = msg.payload.decode()
        if msg.topic == "game/modules/Simon/Success":
            self.simon_success = msg.payload.decode()
        if msg.topic == "game/modules/Keypad/Success":
            self.keypad_success = msg.payload.decode()

    def connect_to_broker(self):
        self.mqttc = paho.Client(client_id="manager", clean_session=False)
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
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
        updated_lives = self.number_of_lives - 1
        self.mqttc.publish("game/lives", updated_lives, 1, True)

    def has_module_been_won(self, module):
        if module == "Simon":
            if self.simon_success == "True":
                self.win_module(module)
                path = "game/modules/" + module + "/Fail"
                self.mqttc.publish(path, False, 1, True)
        elif module == "Keypad":
            if self.keypad_success == "True":
                self.win_module(module)
                path = "game/modules/" + module + "/Fail"
                self.mqttc.publish(path, False, 1, True)
        else:
            print("Erreur: aucun nom de module")

    def is_module_in_failure(self, module):
        if module == "Simon":
            if self.simon_failure == "True":
                self.is_there_still_lives_left()
                self.decrease_number_of_lives()
                path = "game/modules/" + module + "/Fail"
                self.mqttc.publish(path, False, 1, True)
                self.activate_module(module)
        elif module == "Keypad":
            if self.keypad_failure == "True":
                self.is_there_still_lives_left()
                self.decrease_number_of_lives()
                path = "game/modules/" + module + "/Fail"
                self.mqttc.publish(path, False, 1, True)
                self.activate_module(module)
        else:
            print("Erreur: aucun nom de module")

    def win_module(self, module):
        if self.module_index + 1 == len(self.game_modules):
            self.win_game()
            return 0
        self.module_index += 1
        self.deactivate_module(module)
        self.activate_module(self.game_modules[self.module_index])

    def win_game(self):
        self.mqttc.publish("game/hasBeenWon", True, 1, True)
        print("Congratulations! You have won the game!")
        self.wait_for_new_game()

    def is_there_still_lives_left(self):
        if self.number_of_lives == 0:
            self.game_over()

    def is_there_still_time_left(self):
        if self.time_left <= 0:
            print("Out of time!")
            self.game_over()

    def wait_for_new_game(self):
        self.mqttc.publish("game/isStarted", False, 1, True)
        while True:
            print("Do you want to start a new game? Y or N")
            result = input()
            if result == "Y" or result == "y":
                print("Starting new game!")
                self.start_game()
                break
            elif result == "N" or result == "n":
                print("Thanks for playing!")
                self.end_game()
                break
            else:
                print("Command not recognized")
