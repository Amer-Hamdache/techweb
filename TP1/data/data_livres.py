import json
import os
#Obtient sans générer d'erreur le fichier livres.json et sans spécifier le chemin/répertoire du fichier
livres_json = os.path.join(os.path.dirname(__file__), "livres.json")
# Chargement des données du fichier JSON
with open(livres_json, "r") as f:
    livres_list = json.load(f)

# Création d'un dictionnaire indexé par l'ID du livre
# Nous utilisons enumerate() pour obtenir à la fois l'indice k et la valeur v de chaque élément de la liste
# Nous ajoutons 1 à l'indice k pour obtenir un ID commençant à 1 plutôt qu'à 0
liste_livres = {k+1: v for k, v in enumerate(livres_list)}
# À ce stade, list_livres est un dictionnaire où chaque clé est l'ID d'un livre et chaque valeur est un dictionnaire représentant un livre avec ses attributs (nom, auteur, éditeur, etc.)
# Nouas pouvons utiliser list_livres pour accéder aux informations sur les livres dans votre application