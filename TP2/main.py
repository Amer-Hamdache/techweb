from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from dataclass_livres import LivreModel
from data_livre import liste_livres  # Assurez-vous que cette importation fonctionne avec votre structure de données.
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_all_livres(request: Request):
    # Utilisation de LivreModel pour créer des objets Livre à partir de liste_livres
    livres = [LivreModel(**liste_livres[id]) for id in liste_livres]
    return templates.TemplateResponse("liste_livres.html", {"request": request, "livres": livres, "total": len(livres)})

@app.get("/ajouter-livre")
async def ajouter_livre_form(request: Request):
    return templates.TemplateResponse("ajouter_livre.html", {"request": request})

@app.post("/ajouter-livre")
async def ajouter_livre(id: int = Form(...), nom: str = Form(...), auteur: str = Form(...), editeur: str = Form(...)):
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
    if id not in liste_livres:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    # Créez une instance de LivreModel avec les données du livre
    livre = LivreModel(**liste_livres[id])
    # Passez l'instance de LivreModel au template
    return templates.TemplateResponse("modifier_livre.html", {"request": request, "livre": livre, "id": id})

@app.post("/modifier-livre/{id}")
async def modifier_livre(id: int, nom: str = Form(...), auteur: str = Form(...), editeur: str = Form(...)):
    if id not in liste_livres:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    liste_livres[id] = {"id": id, "nom": nom, "auteur": auteur, "editeur": editeur}
    return {"message": "Livre modifié avec succès"}

@app.get("/supprimer-livre/{id}")
async def supprimer_livre(id: int):
    if id in liste_livres:
        del liste_livres[id]
        return {"message": "Livre supprimé avec succès"}
    else:
        raise HTTPException(status_code=404, detail="Livre non trouvé")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("erreur_404.html", {"request": request}, status_code=404)
    # Gérez d'autres codes d'erreur HTTP ici si nécessaire
    else:
        return HTMLResponse(content=f"Erreur inattendue : {exc.detail}", status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse("erreur_validation.html", {"request": request, "errors": exc.errors()}, status_code=422)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
