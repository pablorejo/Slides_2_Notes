import os
from pdf2image import convert_from_path
from models import chat_gpt
from models import chat_gemini
from tqdm import tqdm
import argparse
import pypandoc

MODELS = {
    "chat_gpt": chat_gpt,
    "chat_gemini": chat_gemini,
}

def extraer_explicacion(image, debug=False, model=MODELS['chat_gemini']):
    """
    Envía la imagen a la API para obtener una explicación detallada en español.
    """
    prompt = """Genera apuntes a partir del contenido.
    Utiliza un lenguaje académico y formal, evitando emojis y expresiones coloquiales.
    Aplica formato Markdown para estructurar el texto (títulos, listas, negritas, etc.).
    Incluye al inicio un resumen breve y conciso, separado por una línea '---', que indique claramente el tema principal.
    No menciones la palabra "diapositiva" ni describas la imagen o estructura visual, solo redacta los conceptos clave como si fueran apuntes de estudio.
    No incluyas conclusión final.
    """

    respuesta = model.send_image(
        image=image,
        role_system="Eres un profesor muy bueno en hacer apuntes.",
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

            explicacion = extraer_explicacion(image, debug=debug,model=MODELS["chat_gemini"])  # Para evitar el error de la primera página
            explicacion_parser = "\n".join([line.lstrip('> ') for line in explicacion.split("\n")])  # Limpiar la explicación de saltos de línea innecesarios
            file.write(f"{image_text}\n{explicacion_parser}\n\n")  # Escribir la explicación en el documento

    # Configuración base del estilo
    print(f"Documento MD generado: {doc_salida}")

def convertir_md_a_docx(md_file, output_file):
    """
    Convierte un archivo Markdown a DOCX utilizando pypandoc.
    """
    try:
        pypandoc.convert_file(md_file, 'docx', outputfile=output_file)
        print(f"Documento DOCX generado: {output_file}")
    except Exception as e:
        print(f"Error al convertir a DOCX: {e}")

def convertir_md_a_pdf(md_file, output_file):
    """
    Convierte un archivo Markdown a PDF utilizando pypandoc.
    """
    try:
        pypandoc.convert_file(md_file, 'pdf', outputfile=output_file)
        print(f"Documento PDF generado: {output_file}")
    except Exception as e:
        print(f"Error al convertir a PDF: {e}")


def create_md(
    limit: int=None,
    debug=False,
    folder_pdfs="PDFs",
    folder_save="MD",
    model=MODELS['chat_gemini'],
    dpi=200):


    if not os.path.exists(folder_pdfs): os.mkdir(folder_pdfs)
    if not os.path.exists(folder_save): os.mkdir(folder_save)
    limit_clone = limit
    for fichero in os.listdir(folder_pdfs):
        if fichero.endswith(".pdf"):
            print(f"Procesando fichero: {fichero}")
            ruta_entrada_pdf = os.path.join(folder_pdfs, fichero)
            crear_doc_con_imagen_y_explicacion(ruta_entrada_pdf,
                                               folder_save,
                                               debug=debug,
                                               model=model,
                                               dpi=dpi)
            if limit_clone is not None:
                limit_clone -= 1
                if limit_clone <= 0:
                    break
    print("Proceso completado.")


def main(limit=None,
        debug=False,
        folder_pdfs="PDFs",
        folder_md="MD",
        model=MODELS['chat_gemini'],
        dpi=200,
        md2pdf=False,
        md2docx=False,
        skipProcessing=False,
        docs_folder="docs",
    ):
    


    if not skipProcessing:
        create_md(limit=limit,
            debug=debug,
            folder_pdfs=folder_pdfs,
            folder_md=folder_md,
            model=model,
            dpi=dpi
            )
    
    if md2docx:
        limit_clone = limit
        for folder in os.listdir(folder_md):
            for file in os.listdir(os.path.join(folder_md,folder)):
                if file.endswith("salida.md"):
                    print(f"Convirtiendo {file} a DOCX...")
                    
                    ruta_entrada_md = os.path.join(folder_md, folder, file)
                    with open(ruta_entrada_md, "r", encoding="utf8") as f:
                        contenido = f.read()

                    contenido = contenido.replace("img/", f"{folder_md}/{folder}/img/")
                    ruta_entrada_md_tmp = os.path.join(folder_md, folder, file.replace(".md", "_tmp.md"))
                    with open(ruta_entrada_md_tmp, "w", encoding="utf8") as f:
                        f.write(contenido)


                    ruta_salida_docx = os.path.join(docs_folder, file.replace(".md", ".docx"))
                    convertir_md_a_docx(ruta_entrada_md_tmp, ruta_salida_docx)
                    os.remove(ruta_entrada_md_tmp)  # Eliminar el archivo temporal

                    if limit is not None:
                        limit_clone -= 1
                        if limit_clone <= 0:
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
    
    parser.add_argument('--skipProcessing', action='store_true', help="Si se desea omitir el procesamiento de los PDFs")
    parser.add_argument('--md2pdf', action='store_true', help="Si se desea convertir el archivo a PDF después de generarlo")
    parser.add_argument('--md2docx', action='store_true', help="Si se desea convertir el archivo a DOCX después de generarlo")
    parser.add_argument('--docs_folder', type=str, default="docs", help="Carpeta de salida para documentos generados")
    args = parser.parse_args()

    limit = args.limit if args.limit is not None else None
    folder_pdfs = args.folder_pdfs if args.folder_pdfs else os.path.join('extra',"PDFs")
    folder_save = args.folder_save if args.folder_save else os.path.join('extra',"MD")
    dpi = args.dpi if args.dpi else 200
    model = MODELS[args.model] if args.model else MODELS['chat_gemini']
    debug = args.debug if args.debug else False

    skipProcessing = args.skipProcessing if args.skipProcessing else False
    md2pdf = args.md2pdf if args.md2pdf else False
    md2docx = args.md2docx if args.md2docx else False
    docs_folder = args.docs_folder if args.docs_folder else os.path.join('extra',"docs")
    
    main(limit,
        debug,
        folder_pdfs,
        folder_save,
        model,
        dpi,
        md2pdf,
        md2docx,
        skipProcessing,
        docs_folder
        )
    
