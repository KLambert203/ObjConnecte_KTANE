# ObjConnecte_KTANE
Le repo pour notre implémentation du jeu Keep Talking and Nobody Explodes dans le cadre du cours Programmation d'objets connectés du Cégep Beauce-Applaches

# Documentation
## LCD_Service
### Keypad
Le keypad fonctionne grâce au script `keypad.py`. Celui-ci possède la classe keypad où est définit tous les fonctions permettant au bon fonctionnement du Keypad.
Afin de pouvoir se servir du Keypad, il faut tout simplement créer une fonction qui génère une instance de la classe avec tous les paramètres nécessaire
puis définir son DebounceTime. Ensuite, créer une boucle infini qui vérifie qu'elle touche a été appuyé. Cette fonction doit être appelé dans un try catch qui nettoie 
les GPIO si l'application se ferme.
### LCD
Pour faire fonctionner le LCD, trois scripts tirés d'une librairie sont nécessaire : `ADAFruit_LCD1602.py` `PCF8574_GPIO.py` `I2CLCD1602.py`.
Quelques initialisations doivent être configuré pour le bon fonctionnement du LCD : 
- Initialiser les adresses `PCF8574` et `PCF8574A` si le précédent ne fonctionne pas.
- Créer une instance de la classe `PCF8574_GPIO`
- Créer une instance de la classe `Adafruit_CharLCD`
- Retourner les deux instances pour leurs utilisations.
### LCD_Service.py
Le script LCD_Service est un script contenant une seul classe nommé LCD, elle contient la fonction init_chips qui initialise et retourne le nécessaire pour utiliser le LCD. Elle contient également la fonction init_keypad qui contient le nécessaire pour le bon fonctionnement du keypad. La fonction connect_mqtt permet de se connecter au serveur MQTT puis recevoir des données du serveur à l'aide d'abonnement. La fonction start_timer créer un timer avec le temps voulu et envoie à chaque seconde le temps restant au serveur. La fonction loop est la fonction principale qui permet d'afficher sur le LCD toutes les informations pertinente en rapport au jeu. Elle affiche le temps restant, le nombre de vie et le code entré par l'utilisateur pour défuser la bombe. Finalement la fonction run ouvre plusieurs threads roulant en parallèle les fonctions start_timer, loop et le loop_forever du client MQTT. C'est la fonction run qui est appelé par le script main.py.
## Simon Says
## GameManager




# DOCUMENTATION DES ITEMS
https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi
