# Cahier des charges de **"Dungeon Crawler: Endless Descent"**

(Disponible aussi sur GitHub: https://github.com/OJddJO/DungeonCrawler )

## 1. ***Introduction***

Nom du Projet : Dungeon Crawler: Endless Descent
Objectif du Projet : Créer un jeu d'exploration de donjons infini basé sur du texte, avec des éléments de combat, de butin, de progression du personnage et de gestion de ressources.

## 2. ***Caractéristiques Principales***

-   Donjons Générés de Manière Procédurale : Création aléatoire de donjons offrant une variété de salles, de pièges et d'ennemis. 
    Les donjons sont basées sur des labyrinthes générés avec une adaptation du "Randomized Prim's algorithm".
-   Combat en Temps Réel : Système de combat permettant aux joueurs de combattre une variété de monstres et de boss.
-   Butin et Équipement : Collecte de butin pour améliorer les capacités du personnage.
-   Gestion des Ressources : Gestion de la santé et de la mana (utilisé pour lancer des sorts) du personnage.
-   Collecte de Ressources : Récolte de matériaux pour la fabrication d'armes et d'armures.
-   Niveaux et Arbres de Compétences : Progression du personnage par gain d'expérience et investissement de points de compétence.
-   Histoire : Pas d'histoire dans le jeu pour qu'il soit entièrement infini.
    Le jeu risque donc d'être quelque peu répétitif et sans but.

## 3. ***Fonctionnalités Additionnelles***

-   Artisanat et Alchimie : Création d'objets à partir de matériaux et de recettes.
-   Évolutivité : Augmentation de la difficulté avec le niveau du personnage.
-   Système de Quêtes : Intégration d'objectifs facultatifs dans le donjon.
-   Événements Aléatoires : Introduction d'événements aléatoires pour pimenter le gameplay.
-   ~Multijoueur : Possibilité de jouer en coopération.
    Le multijoueur sera du multijoueur local soit directement sur le même ordinateur soit sur le même réseau (mis en place avec le module Python "socket")~

## 4. ***Exigences Techniques***

-   Plateforme : Compatible avec les systèmes d'exploitation Windows et peut-être Linux. (Le projet est fait sur Windows donc est nativement supporté par Windows) 
-   Langage de Programmation : Python
-   Interface Utilisateur : Création d'une interface utilisateur basée sur le terminal.
-   Graphismes et Son : Intégration de graphismes ASCII, pas de son.
-   ~Multijoueur : Mise en place d'une fonctionnalité multijoueur locale.~

## 5. ***Échéancier***

-   Phase de Pré-production : Planification et conception du jeu. (Fin le 1er Octobre)
-   Phase de Production : Développement du jeu. (Fin le 1er Novembre)
-   Phase de Test : Tests et débogage. (Fin le 7 Novembre)
-   Phase de 1er rendu : Première version compilée jouable. (8 Novembre)
-   Première mise à jour : Ajout de la nouvelle interface et de nouvelles fonctionalités. (20 décembre)

## 7. ***Équipe de Développement***

-   Jérémy: Tout le projet

## 8. ***Révision et Approbation***

-   M. Djahnit

## 9. ***Mises à jour***

-   20/12/2020: Ajout de la ***nouvelle interface***. Ajout de la ***Forge***. Ajout de la possibilité de forger des armes et armures. Ajout de la possibilité d'améliorer son équipement. Ajout de la possibilité de récolter des matériaux. ***Début de la phase de développement/test pour linux.*** 