from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse #HTMLResponse : Une classe de réponse qui permet de renvoyer du contenu HTML au client.
from fastapi.exceptions import RequestValidationError #RequestValidationError : Importe l'exception utilisée par FastAPI pour gérer les erreurs de validation des données de requête.
from fastapi.staticfiles import StaticFiles #StaticFiles : Permet de servir des fichiers statiques (CSS, des images et des fichiers JavaScript) dans une application FastAPI.
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException #StarletteHTTPException : Importe l'exception HTTPException de Starlette (le framework asynchrone sur lequel FastAPI est construit) pour une gestion d'erreur plus fine.
from dataclass_livres import LivreModel # LivreModel : Un modèle de données pour représenter un livre.
from data_livre import liste_livres  # liste_livres : Un dictionnaire stockant des informations sur les livres.
import uvicorn

# Crée une instance de l'application FastAPI.
app = FastAPI()

# Monte un répertoire de fichiers statiques sous le chemin "/static".
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure le répertoire des templates Jinja2.
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_all_livres(request: Request):
    """
    Récupère la liste complète de tous les livres et les affiche sur la page.

    Args:
        request (Request): L'objet requête FastAPI.

    Returns:
        TemplateResponse: Renvoie une réponse HTML avec la liste des livres et le nombre total.
    """

    # Route pour afficher tous les livres. Utilise le modèle LivreModel pour créer des objets Livre à partir de liste_livres
    livres = [LivreModel(**liste_livres[id]) for id in liste_livres]
    # Renvoie le template HTML avec la liste des livres et le total.
    return templates.TemplateResponse("liste_livres.html", {"request": request, "livres": livres, "total": len(livres)})

@app.get("/ajouter-livre")
async def ajouter_livre_form(request: Request):
    """
    Affiche le formulaire permettant d'ajouter un nouveau livre.

    Args:
        request (Request): L'objet requête FastAPI.

    Returns:
        TemplateResponse: Renvoie une réponse HTML avec le formulaire d'ajout de livre.
    """

    # Route pour afficher le formulaire d'ajout de livre.
    return templates.TemplateResponse("ajouter_livre.html", {"request": request})


@app.post("/ajouter-livre")
async def ajouter_livre(id: int = Form(...), nom: str = Form(...), auteur: str = Form(...), editeur: str = Form(...)):
    """
    Traite les données soumises du formulaire d'ajout de livre et ajoute le livre.

    Args:
        id (int): L'ID du livre à ajouter, obtenu du formulaire.
        nom (str): Le nom du livre, obtenu du formulaire.
        auteur (str): L'auteur du livre, obtenu du formulaire.
        editeur (str): L'éditeur du livre, obtenu du formulaire.

    Returns:
        dict: Un message indiquant le succès de l'ajout du livre.
    """

    # Route pour traiter le formulaire d'ajout de livre. Lève une exception si l'ID existe déjà.
    if id in liste_livres:
        raise HTTPException(status_code=400, detail="Livre déjà existant avec cet ID.")
    # Convertit les données de formulaire en dictionnaire compatible avec LivreModel
    livre_data = {"id": id, "nom": nom, "auteur": auteur, "editeur": editeur}
    # Valide et crée un objet LivreModel à partir des données de formulaire
    livre = LivreModel(**livre_data)
    # Ajoute le livre validé au dictionnaire des livres
    liste_livres[id] = livre.dict()
    return {"message": "Livre ajouté avec succès"}

@app.get("/modifier-livre/{id}")
async def get_modifier_livre_form(request: Request, id: int):
    """
    Affiche le formulaire de modification pour un livre existant.

    Args:
        request (Request): L'objet requête FastAPI.
        id (int): L'ID du livre à modifier.
    
    Raises:
        HTTPException: Une exception est levée avec un code d'erreur 404 si aucun livre correspondant à l'ID fourni n'est trouvé dans `liste_livres`.

    Returns:
        TemplateResponse: Renvoie une réponse HTML avec le formulaire de modification rempli avec les données du livre sélectionné.
    """

    # Route pour afficher le formulaire de modification d'un livre. Vérifie si le livre existe.
    if id not in liste_livres:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    # Créez une instance de LivreModel avec les données du livre
    livre = LivreModel(**liste_livres[id])
    # Renvoie le template de modification avec les données du livre.
    return templates.TemplateResponse("modifier_livre.html", {"request": request, "livre": livre, "id": id})

@app.get("/modifier-livre")
async def modifier_livre_form(request: Request, id: int):
    """
    Affiche le formulaire de modification pour un livre spécifique.

    Cette route est appelée pour afficher un formulaire pré-rempli avec les informations d'un livre existant, permettant à l'utilisateur de modifier ces informations. Elle utilise l'ID du livre passé en paramètre pour rechercher le livre correspondant dans la base de données (ou, dans ce cas, le dictionnaire `liste_livres`).

    Args:
        request (Request): L'objet requête FastAPI, nécessaire pour générer une réponse appropriée qui inclut le contexte de la requête.
        id (int): L'ID du livre que l'on souhaite modifier, passé en tant que paramètre dans l'URL.

    Raises:
        HTTPException: Une exception est levée avec un code d'erreur 404 si aucun livre correspondant à l'ID fourni n'est trouvé dans `liste_livres`.

    Returns:
        TemplateResponse: Renvoie une réponse HTML qui rend le template `modifier_livre.html`, contenant le formulaire de modification du livre. Le formulaire est pré-rempli avec les informations actuelles du livre, permettant à l'utilisateur de voir les valeurs actuelles et de les modifier si nécessaire.
"""

    if id not in liste_livres:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    livre = LivreModel(**liste_livres[id])
    return templates.TemplateResponse("modifier_livre.html", {"request": request, "livre": livre})

@app.post("/modifier-livre/{id}")
async def modifier_livre(id: int, nom: str = Form(...), auteur: str = Form(...), editeur: str = Form(...)):
    """
    Traite les données soumises du formulaire de modification et met à jour le livre.

    Args:
        id (int): L'ID du livre à modifier.
        nom (str): Le nouveau nom du livre, obtenu du formulaire.
        auteur (str): Le nouvel auteur du livre, obtenu du formulaire.
        editeur (str): Le nouvel éditeur du livre, obtenu du formulaire.

    Returns:
        dict: Un message indiquant le succès de la modification du livre.
    """

    # Route pour traiter le formulaire de modification d'un livre. Vérifie si le livre existe.
    if id not in liste_livres:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    # Met à jour les informations du livre dans le dictionnaire.
    liste_livres[id] = {"id": id, "nom": nom, "auteur": auteur, "editeur": editeur}
    return {"message": "Livre modifié avec succès"}

@app.get("/supprimer-livre/{id}")
async def supprimer_livre(id: int):
    """
    Supprime un livre de la liste et réattribue les ID pour garder la séquence.

    Args:
        id (int): L'ID du livre à supprimer.

    Returns:
        dict: Un message indiquant le succès de la suppression et la réattribution des ID.
    """

    # Route pour supprimer un livre. Vérifie si le livre existe avant de le supprimer.
    global liste_livres
    if id in liste_livres:
        del liste_livres[id]
        # Réattribue les ID pour s'assurer qu'ils sont séquentiels après la suppression
        new_liste_livres = {}
        for new_id, livre in enumerate(liste_livres.values(), start=1):
            livre['id'] = new_id
            new_liste_livres[new_id] = livre

        liste_livres = new_liste_livres
        return {"message": "Livre supprimé avec succès et ID réattribués"}
    else:
        raise HTTPException(status_code=404, detail="Livre non trouvé")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Gère les exceptions HTTP et affiche une page d'erreur correspondante.

    Args:
        request (Request): L'objet requête FastAPI.
        exc (HTTPException): L'exception HTTP capturée.

    Returns:
        TemplateResponse: Renvoie une réponse HTML adaptée au code d'erreur HTTP.
    """

    # Gestionnaire d'exceptions pour les erreurs HTTP. Affiche une page d'erreur spécifique pour le code 404.
    if exc.status_code == 404:
        return templates.TemplateResponse("erreur_404.html", {"request": request}, status_code=404)
    # Gérez d'autres codes d'erreur HTTP ici si nécessaire
    else:
        return HTMLResponse(content=f"Erreur inattendue : {exc.detail}", status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Gère les erreurs de validation de données pour les requêtes entrantes et affiche une page d'erreur.

    Args:
        request (Request): L'objet requête FastAPI.
        exc (RequestValidationError): L'exception de validation de requête capturée.

    Returns:
        TemplateResponse: Renvoie une réponse HTML avec les détails des erreurs de validation.
    """

    # Gestionnaire d'exceptions pour les erreurs de validation de requête.
    # Renvoie une page d'erreur montrant les détails de la validation.
    return templates.TemplateResponse("erreur_validation.html", {"request": request, "errors": exc.errors()}, status_code=422)

#Lance l'application FastAPI
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
