# Projet_Majeur_Adrien_Deloffre

Le fichier simulation.py correspond au main, il gère l'affichage des informations pertinentes et les commandes clavier du jeu :
- affichage :
	- Temps
	- Vitesse : de 0 à vitesse max = 40
	- Tours par minute
	- Rapport boite de vitesse :  de -1 à 3
	- Phare : allumé/éteint
  

# Listes des commandes clavier
    - A : mode autonome / mode manuel
	- L : allume/éteint feux de croisement (low_beam)
	- H : allume/éteint feux de route (high_beam)
	- F1 : premier design de vehicule
	- F2 : deuxieme design de vehicule (celui par defaut)
	- F3 : troisieme design de vehicule
	- F4 : quatrieme design de vehicule
en mode manuel :
	- UP : accélération vehicule
	- DOWN : décélération/accélération inverse véhicule
	- RIGHT : tourne à droite / clignotant droit
	- LEFT : tourne à gauche / clignotant gauche
	
# Description des différentes classes

- La classe World spawn les objets suivants :
	- immeuble
	- passage-pieton (méthode vertical_pedestrian_crossing et méthode horizontal_pedestrian_crossing)
	- pieton
	
- La classe Vehicule gère tous les paramètres du véhicule : capacité de déplacement, phares, designs...

- La classe CanBus génère des trames de données can a partir d'un id d'identification et des données


Dans le dossier vehicule parts :
	
- La classe DrivingSystem gère la capacité de déplacement du véhicule et retourne les tours/minute et rapport de la boite de vitesse
	
- La classe Lighting gère le calcul de position des 
	- feux de croisement
	- feux de route
	- clignotant droit
	- clignotant gauche
Calcul par formule de projection à partir de la position (x,y) de la voiture ainsi que son angle

- La classe Design charge les 4 différents design de véhicule

- La classe Ranger calcule la distance entre l'avant de la voiture et l'obstacle le plus proche

- La classe ImageSegmentation gère le calcul de position de chaque point de collision autour de la voiture (au nombre de 6) et change le booléen approprié si un point de collision rencontre un obstacle

![GitHub Logo](/img/collision_box.png)


# Représentation des noeuds
```mermaid
graph LR
    T1[DrivingSystem] --> Node((Vehicule))
    T2[Design] --> Node((Vehicule))
    T3[Lighting] --> Node((Vehicule))
    T4[Sensing] --> Node((Vehicule))

    Node -->D[Simulation]
```


# Vidéos de présentation

[Lien vers la vidéo pitch youtube](url)

# Liste des dépendances et pré-requis
- Compatibilité Ubuntu 14.04
- Compatibilité Python 3.5
- bibliothèque pygame
- bibliothèque can

# Procédure de mise en route
- lancer un terminal sous Ubuntu et run le fichier "simulation.py" :
- user@dupont:~$ python3 simulation.py


