# Continue de parler et personne n'explose
Keep Talking and Nobody Explodes, sauf que vous manipulez la bombe dans la vraie vie!

## Matériel requis
- 2 Raspberry Pi
- 1 ordinateur Windows ou un 3e Raspberri Pi
- 3 platines d'expérimentations (breadboards)
- Les montages sont assemblés à l'aide du contenu de cette trousse : [Freenove Starter Kit](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi)
  - Montage "Simon"
  - Montage "Minuteur+Clavier numérique"
  - Montage "Fouilli de fils"

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
1. Installez PyCharm sur un Raspberry Pi
2. Créez un nouveau projet PyCharm
3. Lors de la création, décochez l'option *Create a main.py welcome script*
4. Déplacez le script simon.py et le fichier `requirements_simon.txt` dans la racine de votre projet
6. Ajoutez une nouvelle configuration d'exécution (Alt-u) --> Edit configurations --> Add new run configuration (Alt-insert) --> Python --> Script path: `simon.py` --> OK
7. Ouvrez le terminal dans PyCharm (Alt-F12)
8. Exécutez la commande suivante :
```
pip install < requirements_simon.py
```
9. Spécifiez l'addresse IP de votre serveur MQTT dans la variable `server_ip_addr` (Par défaut, la valeur est `10.4.1.43`)
10. Branchez Simon dans le GPIO 
11. Exécutez le script (Maj-F10)

## GameManager
Le module GameManager est l'ensemble qui contrôle la partie. Il contient deux scripts: manage_game.py et GameManager.py

### manage_game.py
C'est le script de gestion de la partie. Nous devons l'ajouter comme une configuration de démarrage de l'interpréteur Python pour l'exécuter. Il utilise la classe Game_Manager.py pour écrire et lire les informations du serveur MQTT. C'est dans ce script que nous pourrons configurer l'adresse IP et le port du serveur, en plus des modules connectés au jeu. Présentement, le jeu ne supporte pas de modules supplémentaires, mais ceci est une option dans le futur.

Pour changer les valeurs de l'adresse IP et des modules, seulement ajuster les valeurs dans les lignes 
```
manager = GameManager.GameManager("10.4.1.43", 1883, [])
manager.game_modules = ["Simon", "Keypad"]
```

Il est important de seulement changer l'adresse IP et le numéro de port si tel est le cas, puisque la librairie Paho-MQTT ne s'attends qu'à ces options.
Advenant le cas que vous ajoutiez un nouveau module au jeu, il est important de l'ajouter avec son nom en string séparé par une virgule des autres. Le serveur MQTT utilise ce nom pour générer les sujets à l'écriture.

#### Utilisation
Lors du démarrage du script, la console questionnera l'utilisateur pour définir la prochaine action. S ou s commencera la partie et E ou e terminera la partie. Tout autre commande retournera une erreur.

Au départ de la partie, le script appelle les méthodes `start_game()` et `manage_game()` du GameManager. Celles-ci s'occupe de lire et écrire les informations pertinentes de la partie. Une fois que le Manager détecte un échec ou une victoire, il demandera à l'utilisateur s'il veut recommencer une partie ou terminer. Dans la 2e option, le Manager remettra les valeurs par défaut au niveau du serveur et terminera l'exécution.

### GameManager.py
Ceci est le script qui applique la gestion concrètement. Il n'a pas à être configuré comme script de démarrage, mais il doit être dans le projet puisque manage_game.py importe la classe. Pour le bon fonctionnement de cette classe, nous devons installer le module paho-mqtt dans l'environnement virtuel. Pour ce faire :
```
pip install paho-mqtt
```

Le script manage_game.py instancie la classe avec les informations du serveur et des modules. Dans son constructeur, il remet les valeurs du jeu aux valeurs par défaut. Il serait possible ici de changer le temps alloué au joueur en changeant la valeur de la ligne `self.time_left = 180`. Les autres valeurs doivent rester inchangées.

#### Utilisation
Aucune manipulation n'est à faire ici. Le script s'exécute en boucle infinie jusqu'à ce qu'une défaite ou une victoire soit détectée. À la fin d'une partie, le joueur sera questionné s'il veut recommencer une partie ou terminer. Il est possible de répondre Y/y pour recommencer, ou N/n pour terminer.