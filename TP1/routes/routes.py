from fastapi import APIRouter,HTTPException,Path
#On importe la class Livre
from classes.dataclass_Livre import Livre
from dataclasses import asdict
#On importe la liste des livres
from data.data_livres import liste_livres
 
 
#Permet de définir les différentes routes (endpoint) avec sous titre = tags
router = APIRouter(tags=["Routes[GET/POST]"])
 
# Endpoint pour récupérer la liste de tous les livres
@router.get("/Livres")
def get_all_Livres() -> list[Livre]:
    """
    Récupère la liste complète de tous les livres.
 
    Returns:
        list[Livre]: Une liste contenant tous les livres sous forme d'objets Livre.
    """
    # Initialise une liste vide pour stocker les livres à retourner
    res = []
   
    # Parcourt chaque ID de livre dans le dictionnaire liste_livres
    for id in liste_livres:
        # Crée un objet Livre à partir des données de chaque livre dans le dictionnaire et l'ajoute à la liste des résultats
        res.append(Livre(**liste_livres[id]))
   
    # Retourne la liste complète des livres
    return res
 
@router.get("/total_livres")
def get_total_livres() -> dict:
    """
    Récupère le nombre total de livres disponibles.
 
    Returns:
        dict: Un dictionnaire contenant le nombre total de livres.
    """
    # Utilise la fonction len() pour obtenir le nombre d'éléments dans le dictionnaire liste_livres
    # Cela représente le nombre total de livres
    total_livres = len(liste_livres)
   
    # Retourne un dictionnaire avec la clé "total" et la valeur du nombre total de livres
    return {"total": total_livres}
 
 
@router.get("/livre/{id}")
def get_livre_by_id(id: int = Path(ge=1)) -> Livre:
    """
    Récupère un livre par son ID.
 
    Args:
        id (int): L'ID du livre à récupérer. Par défaut, doit être supérieur ou égal à 1.
 
    Returns:
        Livre: Les informations sur le livre récupéré.
 
    Raises:
        HTTPException: Si le livre avec l'ID spécifié n'est pas trouvé, une exception HTTP 404 est levée.
    """
    # Vérifie si l'ID du livre est présent dans le dictionnaire des livres.
    if id not in liste_livres:
        # Si l'ID du livre n'est pas trouvé, lève une exception HTTP 404 avec un message d'erreur.
        raise HTTPException(status_code=404, detail="Le livre demandé n'a pas été trouvé. Veuillez vérifier l'ID du livre et réessayer.")
   
    # Si l'ID du livre est trouvé, retourne les informations sur le livre correspondant.
    return Livre(**liste_livres[id])
 
 
def validate_string(string: str) -> bool:
    """
    Vérifie si la chaîne de caractères n'est pas vide ou ne contient que des espaces.
 
    Args:
        string (str): La chaîne de caractères à valider.
 
    Returns:
        bool: True si la chaîne est valide, False sinon.
    """
    return bool(string.strip())  # Retourne True si la chaîne n'est pas vide ou ne contient pas que des espaces
 
# Endpoint pour créer un livre
@router.post("/livre/{id}")
def create_livre(livre: Livre, id: int, nom: str, auteur: str, editeur: str) -> Livre:
    """
    Endpoint pour ajouter un nouveau livre à la liste des livres.
 
    Args:
        livre (Livre): Les informations sur le livre à ajouter.
        id (int): L'ID du livre.
        nom (str): Le nom du livre.
        auteur (str): L'auteur du livre.
        editeur (str): L'éditeur du livre.
 
    Returns:
        Livre: Les informations sur le livre ajouté.
 
    Raises:
        HTTPException: Si un livre avec le même ID existe déjà, une exception HTTP 400 est levée.
        HTTPException: Si le nom, l'auteur, l'éditeur ou l'ID est vide, une exception HTTP 400 est levée.
    """
    # Vérifie si le nom, l'auteur, l'éditeur et l'ID ne sont pas vides ou ne contiennent que des espaces
    if not validate_string(nom) or not validate_string(auteur) or not validate_string(editeur) or id is None:
        # Si l'une des conditions n'est pas remplie, lève une exception HTTP 400 avec un message d'erreur approprié
        raise HTTPException(status_code=400, detail="Le nom, l'auteur, l'éditeur et l'ID ne peuvent pas être vides ou ne contenir que des espaces.")
   
    # Assignation des valeurs de l'ID, nom, auteur et éditeur à l'objet Livre
    livre.id = id
    livre.nom = nom
    livre.auteur = auteur
    livre.editeur = editeur
   
    # Vérifie si un livre avec le même ID existe déjà dans la liste
    if id in liste_livres:
        # Si oui, lève une exception HTTP 400 avec un message d'erreur approprié
        raise HTTPException(status_code=400, detail=f"Le livre avec l'ID {id} existe déjà !")
   
    # Ajoute le livre à la liste des livres
    liste_livres[id] = asdict(livre)
   
    # Retourne les informations sur le livre ajouté
    return livre
 
 
# Endpoint pour mettre à jour un livre
@router.put("/livre/{id}")
def update_livre(livre: Livre,
                 id: int = Path(ge=1),#ID doit obligatoirement être supérieur ou égal à 1
                 nom: str = "",#Nom est égal à "", doit être modifier par utilisateur sinon HTTPException suite à validate_String
                 auteur: str = "",#Auteur est égal à "", doit être modifier par utilisateur sinon HTTPException suite à validate_String
                 editeur: str = "",#Editeur est égal à "", doit être modifier par utilisateur sinon HTTPException suite à validate_String
                 )-> Livre:
    """
    Endpoint pour mettre à jour les informations d'un livre existant.
 
    Args:
        livre (Livre): Les nouvelles informations sur le livre à mettre à jour.
        id (int): L'ID du livre à mettre à jour.
        nom (str): Le nom du livre.
        auteur (str): L'auteur du livre.
        editeur (str): L'éditeur du livre.
    Returns:
        Livre: Les informations sur le livre mis à jour.
 
    Raises:
        HTTPException: Si le livre avec l'ID spécifié n'est pas trouvé, une exception HTTP 404 est levée.
    """
    # Vérifie si le nom, l'auteur et l'éditeur ne sont pas vides ou ne contiennent que des espaces
    if not validate_string(nom) or not validate_string(auteur) or not validate_string(editeur):
        # Si l'une des conditions n'est pas remplie, lève une exception HTTP 400 avec un message d'erreur approprié
        raise HTTPException(status_code=400, detail="Le nom, l'auteur et l'éditeur ne peuvent pas être vides ou ne contenir que des espaces.")
   
    # Vérifie si le livre avec l'ID spécifié existe dans la liste des livres
    if id not in liste_livres:
        # Si le livre n'est pas trouvé, lève une exception HTTP 404 avec un message d'erreur approprié
        raise HTTPException(status_code=404, detail=f"Désolé, nous n'avons pas pu trouver le livre {id} que vous cherchez. Veuillez vérifier l'ID et réessayer.")
   
    # Assurez-vous que l'ID du livre à mettre à jour correspond à l'ID de l'URL
    livre.id = id  # pour qu'on puisse pas modifier l'ID de livre (pour éviter d'avoir un même ID mais des livres différents)
    livre.nom = nom #Associe le nouveau nom introduit par l'utilisateur à l'ancien nom du livre en question
    livre.auteur = auteur #Associe le nouveau nom introduit par l'utilisateur à l'ancien auteur du livre en question
    livre.editeur = editeur #Associe le nouveau nom introduit par l'utilisateur à l'ancien editeur du livre en question
    # Met à jour les informations du livre avec les nouvelles données
    liste_livres[id] = asdict(livre)
   
    # Retourne les informations sur le livre mis à jour
    return livre
 
 
 
# Endpoint pour supprimer un livre
@router.delete("/livre/{id}")
def delete_livre(id: int = Path(ge=1)) -> Livre:
    """
    Endpoint pour supprimer un livre de la liste des livres.
 
    Args:
        id (int): L'ID du livre à supprimer.
 
    Returns:
        Livre: Les informations sur le livre supprimé.
 
    Raises:
        HTTPException: Si le livre avec l'ID spécifié n'est pas trouvé, une exception HTTP 404 est levée.
    """
    # Vérifie si le livre avec l'ID spécifié existe dans la liste des livres
    if id in liste_livres:
        # Si le livre existe, crée un objet Livre à partir de ses données
        livre = Livre(**liste_livres[id])
        # Supprime le livre de la liste des livres
        del liste_livres[id]
        # Retourne les informations sur le livre supprimé
        return livre
    # Si le livre n'existe pas, lève une exception HTTP 404 avec un message d'erreur
    raise HTTPException(status_code=404, detail=f"Le livre {id} n'existe pas.")
 