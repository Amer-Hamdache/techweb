from fastapi import FastAPI
#On importe l'APIRouter qui se trouve dans le fichier routes.py se trouvant dans le dossier routes 
from routes.routes import router as library_routes
#Application du nom Library
app = FastAPI(title="Library")
#On inclut le routeur provenant de l'importation faite plus tôt, ainsi on peut utiliser nos routes(endpoint) crées
app.include_router(library_routes) 