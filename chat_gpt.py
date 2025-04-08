import base64
import io
from PIL import Image
from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def pil_image_to_base64(image):
    """
    Convierte una imagen PIL a base64 en formato PNG.
    """
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def send_image(image,
               role_system,
               role_user,
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

    try:
        image_base64 = pil_image_to_base64(image)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": role_system},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": role_user},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error al enviar imagen a la API: {e}")
        exit(-1)
        return None

def send_message(
        role_system,
        role_user,
        debug=False
    ):
    """
    Envía un mensaje a la API de OpenAI para generar apuntes detallados.
    """
    if debug: return "Debug mode is on. No API call made."

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": role_system
                },
                {
                    "role": "user",
                    "content": role_user
                }
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error al generar apuntes: {e}")
        return None
