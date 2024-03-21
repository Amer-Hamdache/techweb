from pydantic import BaseModel, Field

class LivreModel(BaseModel):
    id: int = Field(..., gt=0, description="L'ID doit être un nombre positif") # "gt=0" (greater than 0) garantit que l'ID doit être supérieur à zéro et le paramètre ... indique que ce champ est obligatoire.
    nom: str
    auteur: str
    editeur: str
