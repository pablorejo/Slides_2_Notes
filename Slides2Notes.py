import os
from pdf2image import convert_from_path
import chat_gpt  # Asegúrate de que chat_gpt.py esté en el mismo directorio o en el PYTHONPATH
import chat_gemini
from tqdm import tqdm

MODELS = {
    "chat_gpt": chat_gpt,
    "chat_gemini": chat_gemini,
}

def extraer_explicacion(image, num_pagina, debug=False, model=MODELS['chat_gemini']):
    """
    Envía la imagen a la API para obtener una explicación detallada en español.
    """
    prompt = "Explica detalladamente el contenido de la imagen en español en tono académico."
    respuesta = model.send_image(
        image=image,
        role_system="Eres un asistente que explica documentos.",
        role_user=prompt,
        debug=debug
    )
    return respuesta if respuesta is not None else "[No se obtuvo respuesta]"


def crear_doc_con_imagen_y_explicacion(pdf_entrada, folder_salida, debug=False, dpi=200):
    """
    Convierte las páginas del PDF en imágenes, obtiene una explicación para cada una y genera un documento DOCX con:
      - Página de título
      - Tabla de contenidos
      - Encabezados y pies de página con numeración
      - Cada imagen centrada seguida de su explicación formateada en Markdown.
    """
    print("Convirtiendo páginas a imágenes...")
    imagenes = convert_from_path(pdf_entrada, dpi=dpi)
    num_paginas = len(imagenes)
    print(f"El PDF tiene {num_paginas} páginas convertidas a imagen.")

    name_file = os.path.basename(pdf_entrada).replace(".pdf", "")
    folder_salida = os.path.join(folder_salida, name_file)

    if not os.path.exists(folder_salida): os.mkdir(folder_salida)
    doc_salida = os.path.join(folder_salida, f"{name_file}_salida.md")


    with open(doc_salida, "w",encoding="utf8") as file:
        for i,image in tqdm(enumerate(imagenes),total=num_paginas, desc="Generando documento"):
            # Guardar la imagen en el folder_salida
            folder_img_name = "img"
            folder_img = os.path.join(folder_salida, folder_img_name)
            if not os.path.exists(folder_img): os.mkdir(folder_img)

            name_img = f"pagina_{i + 1}.png"
            image_path = os.path.join(folder_img, name_img)
            image.save(image_path, "PNG")
            image = f"![Diapositiva de la página {i}]({f"{folder_img_name}/{name_img}"})"

            explicacion = extraer_explicacion(image, i, debug=debug,model=MODELS["chat_gemini"])  # Para evitar el error de la primera página
            explicacion_parser = "".join([line.lstrip('> ') for line in explicacion.split("\n")])  # Limpiar la explicación de saltos de línea innecesarios
            file.write(f"{image}\n\n{explicacion_parser}")  # Escribir la explicación en el documento

    # Configuración base del estilo
    print(f"Documento MD generado: {doc_salida}")

def main(limit=None,debug=False):
    FOLDER_PDFS = "PDFs"
    FOLDER_SAVE = "MD"
    if not os.path.exists(FOLDER_PDFS):
        os.mkdir(FOLDER_PDFS)
    if not os.path.exists(FOLDER_SAVE):
        os.mkdir(FOLDER_SAVE)
    for fichero in os.listdir(FOLDER_PDFS):
        if fichero.endswith(".pdf"):
            print(f"Procesando fichero: {fichero}")
            salida_doc = fichero.replace(".pdf", "_salida.docx")
            ruta_salida_doc = os.path.join(FOLDER_SAVE, salida_doc)
            ruta_entrada_pdf = os.path.join(FOLDER_PDFS, fichero)
            crear_doc_con_imagen_y_explicacion(ruta_entrada_pdf, FOLDER_SAVE, debug=debug)
            if limit is not None:
                limit -= 1
                if limit <= 0:
                    break
    print("Proceso completado.")

if __name__ == "__main__":
    main()  # Cambia el número a None para procesar todos los PDFs en la carpeta