import random
import string
from typing import Union
from utils import DynamoManager

from fastapi import FastAPI
from fastapi import Body

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def test():
    return {"test": "Hello World"}

def generate_short_url(length=6):
    """
    Genera un string aleatorio de longitud `length` con caracteres alfanuméricos.

    Args:
        length (int): Longitud del string a generar.

    Returns:
        str: String aleatorio de longitud `length`.

    Created:
        - 10/07/2024
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.post("/short-cut/generate")
def generate_short_cut(url: str = Body(..., embed=True)):
    """
    Api para generar un short url a partir de una url original.

    Args:
        url (str): Url original.

    Returns:
        dict: Diccionario con la url original y la url corta generada.
        - short_url (str): Url corta generada.
        - original_url (str): Url original.

    Created:
        - 10/07/2024
    """
    
    short_url = generate_short_url(12)
    DynamoManager.save_url(url, short_url)

    return {"short_url": short_url, "original_url": url}

@app.get("/short-cut/{short_url}")
def redirect_short_cut(short_url: str):
    """
    Api para redirigir a la url original a partir de la url corta.

    Args:
        short_url (str): Url corta.

    Returns:
        dict: Diccionario con la url original y la url corta.
        - short_url (str): Url corta.
        - original_url (str): Url original.

    Created:
        - 10/07/2024
    """
    # TODO: arreglar error 
    # An error occurred (ValidationException) when calling the GetItem operation: The provided key element does not match the schema
    response = DynamoManager.update_clicks(short_url)
    if response:
        return {"short_url": short_url, "original_url": response}
    
    return {"short_url": short_url, "original_url": None}
