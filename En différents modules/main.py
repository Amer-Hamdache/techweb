import uvicorn
#Lance l'application FastAPI qui se trouve dans le fichier test.py
if __name__ == "__main__":
    uvicorn.run("Appli_Web:app", host="127.0.0.1", port=8000, reload=True)#le reload pour qu'il enregistre les modifications qu'on fait dans le code
