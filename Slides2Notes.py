import os
from pdf2image import convert_from_path
import chat_gpt  # Asegúrate de que chat_gpt.py esté en el mismo directorio o en el PYTHONPATH
import chat_gemini
from tqdm import tqdm
import argparse

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


def crear_doc_con_imagen_y_explicacion(
    pdf_entrada,
    folder_salida,
    debug=False,
    model=MODELS['chat_gemini'],
    dpi=200):
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
            image_text = f"![Diapositiva de la página {i}]({f"{folder_img_name}/{name_img}"})"

            explicacion = extraer_explicacion(image, i, debug=debug,model=MODELS["chat_gemini"])  # Para evitar el error de la primera página
            explicacion_parser = "\n".join([line.lstrip('> ') for line in explicacion.split("\n")])  # Limpiar la explicación de saltos de línea innecesarios
            file.write(f"{image_text}\n{explicacion_parser}\n\n")  # Escribir la explicación en el documento

    # Configuración base del estilo
    print(f"Documento MD generado: {doc_salida}")

def main(
    limit=None,
    debug=False,
    folder_pdfs="PDFs",
    folder_save="MD",
    model=MODELS['chat_gemini'],
    dpi=200):


    if not os.path.exists(folder_pdfs): os.mkdir(folder_pdfs)
    if not os.path.exists(folder_save): os.mkdir(folder_save)

    for fichero in os.listdir(folder_pdfs):
        if fichero.endswith(".pdf"):
            print(f"Procesando fichero: {fichero}")
            ruta_entrada_pdf = os.path.join(folder_pdfs, fichero)
            crear_doc_con_imagen_y_explicacion(ruta_entrada_pdf,
                                               folder_save,
                                               debug=debug,
                                               model=model,
                                               dpi=dpi)
            if limit is not None:
                limit -= 1
                if limit <= 0:
                    break
    print("Proceso completado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de documentos a partir de PDFs")
    parser.add_argument('-l', '--limit', type=int, default=None, help="Número máximo de PDFs a procesar")
    parser.add_argument('-d', '--debug', action='store_true', help="Activar modo de depuración")
    parser.add_argument('-f', '--folder_pdfs', type=str, default="PDFs", help="Carpeta de entrada con PDFs")
    parser.add_argument('-s', '--folder_save', type=str, default="MD", help="Carpeta de salida para documentos generados")
    parser.add_argument('-dpi', '--dpi', type=int, default=200, help="DPI para la conversión de PDF a imagen")
    parser.add_argument('-m', '--model', type=str, choices=MODELS.keys(), default='chat_gemini', help="Modelo a utilizar para la generación de contenido")

    args = parser.parse_args()

    limit = args.limit if args.limit is not None else None
    folder_pdfs = args.folder_pdfs if args.folder_pdfs else "PDFs"
    folder_save = args.folder_save if args.folder_save else "MD"
    dpi = args.dpi if args.dpi else 200
    model = MODELS[args.model] if args.model else MODELS['chat_gemini']
    debug = args.debug if args.debug else False

    main(limit=limit,
         debug=debug,
         folder_pdfs=folder_pdfs,
         folder_save=folder_save,
         model=model,
         dpi=dpi)