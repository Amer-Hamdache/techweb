from pydantic import BaseModel, Field

class LivreModel(BaseModel):
    id: int = Field(..., gt=0, description="L'ID doit être un nombre positif")
    nom: str
    auteur: str
    editeur: str
