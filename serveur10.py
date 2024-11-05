###############################################################################################################
#                      Sacha Veillon Rodrigues      Messagerie Mqtt              28/10/24                     #
###############################################################################################################
import threading                        # module qui permet de créer des threads
import tkinter as tk                    # tkinter qui nous permet de créer des interfaces
from tkinter import ttk, messagebox     # ttk pour les widget et messagebox pour les dialogues box
import paho.mqtt.client as mqtt         # paho.mqtt.client qui nous permet de manipuler le protocole mqtt

# Dictionnaire pour stocker les onglets des topics
tableau_topics = {} # dictionnaire tableau_topics qui permet de stocker les onglets des topics et leur zones de textes
                # les keys sont les noms des topics et les valeurs est une zone de textes
                
logs = []       # liste logs pour stocker chaque message de log


###################################################################################################################################################################
#                                                       Fonction de rappel pour la connexion
#   fonction callback, dès qu'une connextion est en train de s'établir, la fonction on connect est lancé, elle récupère le code rc de retour de connexion, un peu
#   comme les code de statuts http si le code est égal a 0 alors on prépare un message qu'on rentre dans les logs, et on fait apparaître un pop up 
#
# Fonction de rappel pour la connexion
# Un peu complexe a comprendre au début, mais si client, use, flags ne sont pas mit en paramètre, les fonctions de
# callback ne fonctionneront pas car paho.mqtt.client en a besoin pour appeler les fonctions de callback

def on_connect(client, use, flags, rc): # fctn utiliser quand le client mqtt se connecte au broker
    # client : instance du client Mqtt
    # use -> userdata : data user défini lors de configuration
    # flags : drapeaux de connexions
    # rc : code de retour de connexions 
    if rc == 0: # si le rc = 0 la connexion est réussite
        message = "Connecté au serveur MQTT"
        print(message) # on affiche un message dans la console 
        logs.append(message) # on oublie pas de rentrer les logs dans la liste 
        messagebox.showinfo("Succès", "Connecté au broker MQTT!") # affichage d'une box pop up pour dire que la connexion a réussie
    else:
        message = f"Échec de la connexion, code de retour: {rc}" # the same thing but for the reverse 
        print(message)                                           # ' ' ' '
        logs.append(message)                                     # ' ' ' ' 
        messagebox.showerror("Erreur", f"Échec de la connexion: {rc}") # on incorpore le code d'éreur afin de mieux comprendre

#                                                           FIN DE FONCTIONS ON_CONNECT
#
#


#####################################################################################################################################################################
#                                                              Fonction de rappel pour la réception des messages
# dès qu'un message est reçu on print le message dans la console et on rendre le messages dans les logs, ensuite elle nous permet de creer des onglet, si
# le topic est dans la listes des topics existant alors 
# 
# On utilise un Notebook pour afficher différent onglets (chaque topic a son onglet), la zone de est récup, elle est créer au
# lors de l'abonnement a un topic, si celui si n'existe pas (s'il il n'est pas dans le tableau des topic)
#
def on_message(client, userdata, msg): # fctn appelé quand lorsque le client mqtt reçoit un message sur un topic abonné
    message = f"Message reçu sur {msg.topic}: {msg.payload.decode()}" # le .payload est pour avoir le message en byte, puis on le decode en utf -8 
    print(message) # on print le message 
    logs.append(message) # on oublie pas de le mettre dans les logs
    if msg.topic in tableau_topics:  # if msg.topic est dans tableau_topics -> un onglet existe pour ce topic
        zone_texte = tableau_topics[msg.topic] # recup de la zone de texte 
        zone_texte.insert(tk.END, f"{msg.topic}: {msg.payload.decode()}\n") # insert permet d'inserer un texte, a un endroit précis
        # ici on a précisé à la fin avec le tk.END qui représente la fin de la zone de texte, donc à la fin du contenu existant
#
#                                                           FIN DE LA FONCTION ON_MESSAGE
#
#
#####################################################################################################################################################################



#####################################################################################################################################################################
#                                           Fonction de rappel pour se connecter au broker MQTT
#
#
#

def connect_to_broker(): 
    ip = zone_txt_ip.get() # recup la valeur de l'adresse ip taper dans le champ 
    port = zone_txt_port.get() # recup la valeur du port taper dans le champ 
    
    if not ip or not port: # si l'un des deux n'est pas saisie
        messagebox.showerror("Erreur", "Veuillez entrer l'adresse IP et le port.")
        return
    # si l'un des deux est vide il affiche un pop up erreur
    try: # vérification 
        port = int(port) # le port est forcément un entier
    except ValueError:
        messagebox.showerror("Erreur", "Le port doit être un nombre entier.")
        return
     # affichage erreur
    
    global client # l'utilisation de la variable global permet de modifier le client en dehors de la fonction
    client = mqtt.Client() # créartion d'une nouvelle instance de client mqtt 
    client.on_connect = on_connect # on lie le callack a l'événement de connexion du client Mqtt
    client.on_message = on_message # n lie le callack a l'événement de réception de messages 
    
    try:
        client.connect(ip, port) # essaye de se connecter au broker
        client.loop_start() # on démarre une boucle en arrère plan pour gérer les messages mqtt
    except Exception as e: # si la connexion echoue alors un pop up d'érreurs sera affiché 
        messagebox.showerror("Erreur", f"Échec de la connexion: {e}")

# Fonction pour se déconnecter du broker MQTT
def deconnection_broker(): # fonction pour la déconnexion broker
    try:
        client.disconnect() # essaye de se déconnecté avec une méthode de client
        message = "Déconnexion du serveur MQTT"
        print(message) 
        logs.append(message) # on insère le message de log
        messagebox.showinfo("Succès", "Déconnecté du broker MQTT!") # pop up status
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de la déconnexion: {e}") # pop up status

# Fonction pour exporter les logs dans un fichier texte
def export_logs():
    with open("logs.txt", "w") as file: # on créer ou on open si il existe le fichier logs.txt et on le met en mode Write
        for log in logs: # pour chaque log dans la liste logs
            file.write(log + "\n") # on écrit une ligne puis on saute une ligne
    messagebox.showinfo("Succès", "Les logs ont été exportés dans logs.txt") # pop up status

# Fonction de rappel pour s'abonner à un topic
def abonnement_a_topic():
    topic = entry_topic.get() # on récup les données donc le topic auquel on souhaite s'abonner
    
    if not topic: # si il n'y a rien dans le champs topic 
        messagebox.showerror("Erreur", "Veuillez entrer un topic.") # pop up status
        return
    
    try:
        client.subscribe(topic)  # essaye de susbricbe au topic 
        messagebox.showinfo("Succès", f"Souscrit au topic '{topic}'!") # pop up status
        
        # Ajouter un nouvel onglet pour le topic
        if topic not in tableau_topics:  # on verfie si le topic n'est pas déja dans le dictionnaiire avec tt les topics 
                                     # si il n'y est pas alors 
            new_onglet = ttk.Frame(onglet)  # on créer un new onglet , onglet est une instance de Notebook, un notebook pour chaque onglet
            onglet.add(new_onglet, text=topic) # ajoute l'onglet au controle des onglet
            zone_texte = tk.Text(new_onglet) # création de la nouvelle zone de texte 
            zone_texte.pack(expand=1, fill="both", padx=5, pady=5) # ajout de la zone de texte à l'onglet et configure son positionnement pour qu'elle s'étende et remplisse tt l'espace dispo 
            tableau_topics[topic] = zone_texte # on ajoute la zone de texte au dictionnaire 
            topics_liste['values'] = list(tableau_topics.keys())  # Mettre à jour la liste déroulante des topics avec les keys du dictionnaire
    
    except Exception as e: # message d'erreurs 
        messagebox.showerror("Erreur", f"Échec de la souscription: {e}")

# Fonction pour envoyer un message à un topic sélectionné
def envoyer_message(): 
    topic = topics_liste.get() # on récupère le topic sélectionné dans la liste  
    message = zone_ecrit_message.get() # on récip le message 
    
    if not topic or not message: # si un des deux n'est pas sélectionné ou vide... 
        messagebox.showerror("Erreur", "Veuillez sélectionner un topic et entrer un message.") # pop up status 
        return
    
    try:
        client.publish(topic, message) # publication du message 
        messagebox.showinfo("Succès", f"Message envoyé au topic '{topic}'!") # pop up status
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'envoi du message: {e}") # pop up status

# Fonction pour démarrer le client MQTT dans un thread séparé
def start_mqtt_client():
    mqtt_thread = threading.Thread(target=client.loop_forever) # création d'une nouvelle instance de thread dans le module threading, avec comme target client.loop_forever 
    # qui démarre une boucle infinie pour traiter les messages mqtt
    mqtt_thread.daemon = True # definit le thread en deamon qui est un processus qui tourne en arrière plan
    mqtt_thread.start() # Démarre l'exécution du thread. Cela appelle la méthode client.loop_forever dans le thread séparé, permettant au client MQTT de traiter les messages de manière asynchrone.




#####################################################################################################################################################################
#                                                       ##AFFICHAGE##
#
#####################################################################################################################################################################



# Créer la fenêtre principale
app = tk.Tk() # représentation de la fenêtre de l'app 
app.title("Interface Organisée avec tkinter") # on définit le titre 


#####################################################################################################################################################################
#                                                       WIDGET DE CONNEXION
#

# Frame pour la connexion au broker
# on créé un cadre nommée (label frame) pour grouper les widgets de connections
fenetre_conexion = tk.LabelFrame(app, text="Connexion au Broker", padx=10, pady=10)
#padx et pady ajoute un espace de 10 px autour du contenu du cadre
fenetre_conexion.pack(fill="both", expand="yes", padx=10, pady=10)
# pack pour ajouté le cadre a la fenêtre principal, les paramètres fill et expand permette de s'étendre et remplir l'espace dispo

# Ajouter des widgets dans le fenetre_conexion
texte_for_IP = tk.Label(fenetre_conexion, text="Adresse IP:") # label texte pour adresse ip (texte affiché)
texte_for_IP.grid(row=0, column=0, padx=5, pady=5) # grid permet de placer sur la ligne 0 et la colonne 0 
zone_txt_ip = tk.Entry(fenetre_conexion) # le champ où on tape l'adresse IP 
zone_txt_ip.grid(row=0, column=1, padx=5, pady=5) # grid pour placer ce label a droite (ligne 0 colonne 1)

label_port = tk.Label(fenetre_conexion, text="Port:") # Pareil 
label_port.grid(row=1, column=0, padx=5, pady=5) # Same 
zone_txt_port = tk.Entry(fenetre_conexion) # Same 
zone_txt_port.grid(row=1, column=1, padx=5, pady=5) # Same

bouton_connecte = tk.Button(fenetre_conexion, text="Connecter", command=connect_to_broker) # bouton pour valider, qui lance la fonction connect_to_broker
bouton_connecte.grid(row=2, columnspan=2, pady=10) # on la place sur ligne 2 et sur 2 colonne  

button_disconnect = tk.Button(fenetre_conexion, text="Déconnecter", command=deconnection_broker) # same pour le disconnect
button_disconnect.grid(row=3, columnspan=2, pady=10)

bouton_expt_logs = tk.Button(fenetre_conexion, text="Exporter les logs", command=export_logs) # same pour l'export logs 
bouton_expt_logs.grid(row=4, columnspan=2, pady=10)

#####################################################################################################################################################################
#####################################################################################################################################################################

#####################################################################################################################################################################
#                                                       WIDGET DE SOUSCRIPTIONS
#

# Frame pour souscrire à un topic
fenetre_abbonement = tk.LabelFrame(app, text="Souscrire à un topic", padx=10, pady=10) # création d'un frame subscription
fenetre_abbonement.pack(fill="both", expand="yes", padx=10, pady=10) 

# Ajouter des widgets dans le fenetre_abbonement # SAME 
label_topic = tk.Label(fenetre_abbonement, text="Topic:")  # 
label_topic.grid(row=0, column=0, padx=5, pady=5)
entry_topic = tk.Entry(fenetre_abbonement)
entry_topic.grid(row=0, column=1, padx=5, pady=5)

bouton_abonnement = tk.Button(fenetre_abbonement, text="Souscrire", command=abonnement_a_topic)
bouton_abonnement.grid(row=1, columnspan=2, pady=10)

#####################################################################################################################################################################
#####################################################################################################################################################################

#####################################################################################################################################################################
#                                                              WIDGET MESSAGE
#

# Frame pour envoyer des messages
fenetre_envoye = tk.LabelFrame(app, text="Envoyer un message", padx=10, pady=10)
fenetre_envoye.pack(fill="both", expand="yes", padx=10, pady=10)

# Ajouter des widgets dans le fenetre_envoye
choix_topics = tk.Label(fenetre_envoye, text="Sélectionner un topic:")
choix_topics.grid(row=0, column=0, padx=5, pady=5)
topics_liste = ttk.Combobox(fenetre_envoye) #liste des topics
topics_liste.grid(row=0, column=1, padx=5, pady=5)

ecrit_message = tk.Label(fenetre_envoye, text="Message:")
ecrit_message.grid(row=1, column=0, padx=5, pady=5)
zone_ecrit_message = tk.Entry(fenetre_envoye)
zone_ecrit_message.grid(row=1, column=1, padx=5, pady=5)

bouton_envoyer = tk.Button(fenetre_envoye, text="Envoyer", command=envoyer_message)
bouton_envoyer.grid(row=2, columnspan=2, pady=10)

#####################################################################################################################################################################
#####################################################################################################################################################################

#####################################################################################################################################################################
#                                                                   NOTEBOOK ONGLET
#

# Ajouter un Notebook pour les onglets des topics
onglet = ttk.Notebook(app) # Note book est un conteneur 
onglet.pack(expand=1, fill="both")

#####################################################################################################################################################################
#####################################################################################################################################################################


# Lancer la boucle principale
app.mainloop()