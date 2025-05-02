import pathlib
import textwrap

import google.generativeai as genai
from dotenv import load_dotenv

from IPython.display import display
from IPython.display import Markdown

import os

from PIL import Image
# Cargar variables de entorno desde el archivo .env
load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def send_image(image,
               role_user: str,
               role_system: str,
               debug=False):
    """
    Envía una imagen (PIL.Image) junto con un prompt textual al modelo GPT-4 con visión.

    Parámetros:
        - image: objeto PIL.Image
        - role_system: prompt para el sistema
        - role_prompt: mensaje del usuario que acompaña a la imagen
        - debug: si es True, no se llama a la API

    Devuelve:
        - Respuesta textual generada por el modelo
    """
    if debug: return

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([role_user, image], stream=True)
    response.resolve()

    return to_markdown(response.text).data


def send_mesage(role_user: str,
               role_system: str,
               debug=False):
    """
    Envía una imagen (PIL.Image) junto con un prompt textual al modelo GPT-4 con visión.

    Parámetros:
        - image: objeto PIL.Image
        - role_system: prompt para el sistema
        - role_prompt: mensaje del usuario que acompaña a la imagen
        - debug: si es True, no se llama a la API

    Devuelve:
        - Respuesta textual generada por el modelo
    """
    if debug: return

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([role_user], stream=True)
    response.resolve()

    return to_markdown(response.text).data

def numerate_models():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)



