# Notre application de gestion de livres

Cette application fournit une API pour gérer une librairie de livre. (Voir organigramme pour plus d'explications)
## L'application est découpée en différents modules(fichier.py)
- Un module pour qui initialise le serveur FastAPI à l'adresse http://127.0.0.1:8000/	- Un module pour lancer l'application
- Un module pour définir notre objet "Livre"
- Un module pour traiter les données des livres 
- Un module pour traiter les routes 

## Routes HTTP

- GET /livres : Récupérer la liste de tous les livres.
- POST /livre : Ajouter un nouveau livre.
- GET /livre/{id} : Récupérer les informations d'un livre spécifique.
- PUT /livre/{id} : Mettre à jour les informations d'un livre existant.
- DELETE /livre/{id} : Supprimer un livre existant.
- GET /total_livres : Obtenir le nombre total de livres.

## Classe Livre 

Un livre est définit par un ID, un nom, un auteur et un éditeur 

## Agrémentation de l'application via CSS
Définition de styles pour les différentes parties de l'application

## Agrémentation de l'application via HTML
En date du 21/03, aucune fonctionnalité n'a été modifié. Seuls des templates ont été implémantes permettant d'agrémenter notre application.
Ainsi l'ajout de templates permet d'afficher :  
- Nouvelle page principale/d'accueil où il sera possible pour l'utilisateur d'effectuer des requêtes (ajout, modification, ...)
- Nouvelle page permettant d'ajouter un livre 
- Nouvelle page d'erreur lorsqu'une erreur est rencontrée
- Nouvelle page affichant la listre des livres
- Nouvelle page permettant la modification des données d'un livre
