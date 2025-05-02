import os
from pdf2image import convert_from_path
from models import chat_gpt
from models import chat_gemini
from tqdm import tqdm
import argparse
import pypandoc
import Note2Audio


MODELS = {
    "chat_gpt": chat_gpt,
    "chat_gemini": chat_gemini,
}

def create_index(text_data, debug=False, model=MODELS['chat_gemini']):
    """
    Envía el texto a la API para obtener un índice detallado en español.
    """
    prompt = f"""
    Analiza el siguiente texto y extrae sus aspectos clave:

    {text_data}

    A partir de ese análisis, genera un índice temático detallado utilizando formato **Markdown**, con un máximo de tres niveles jerárquicos de encabezado:

    - Emplea `#`, `##` y `###` para estructurar el índice de forma clara y ordenada.
    - Usa un lenguaje académico, técnico y formal.
    - Evita emojis, expresiones coloquiales o lenguaje informal.

    Ten en cuenta:
    - El tema principal es el texto completo. No debe aparecer como un encabezado de nivel 1.
    - Comienza directamente con títulos representativos de las secciones del contenido.
    - El nivel 1 (`#`) debe representar bloques temáticos principales del texto.
    - Los niveles `##` y `###` deben emplearse para subdivisiones y detalles, respectivamente.
    - Al final de cada encabezado `###`, incluye una lista de puntos clave (temas a tratar) usando viñetas `*`.
    - No incluyas más de 15 titulos de nivel 1 (#).
    - No incluyas más de 5 titulos de nivel 2 (##) por cada título de nivel 1 (#).
    - No incluyas más de 3 titulos de nivel 3 (###) por cada título de nivel 2 (##).

    El objetivo es obtener un índice útil, informativo y bien estructurado que facilite la redacción posterior de apuntes académicos, destacando los temas relevantes bajo cada subapartado.
    """

    
    if debug:
        return """# indice 1
        ## indice 1.1"""
    
    respuesta = model.send_mesage(
        role_user=prompt,
        role_system="Eres un profesor muy bueno en hacer apuntes.",
        debug=debug
    )

    return respuesta if respuesta is not None else "[No se obtuvo respuesta]"


def create_note(text_data, tema, debug=False, model=MODELS['chat_gemini'],n_palabras=1000):
    """
    Envía el texto a la API para obtener un índice detallado en español.
    """
    prompt = f"""
    A partir del siguiente texto de referencia:

    {text_data}

    Redacta apuntes detallados centrados exclusivamente en el siguiente tema: **{tema}**. 

    Sigue estas indicaciones con rigor:

    - Emplea un lenguaje académico, técnico y formal.
    - Evita emojis, expresiones coloquiales o informalidades.
    - Utiliza formato **Markdown**:
    - Comienza con un encabezado de nivel 3 (`###`) correspondiente al título del tema.
    - Estructura el contenido con subencabezados si es necesario (`####`, etc.).
    - Usa listas y viñetas para destacar ideas clave.
    - Aplica **negritas** y *cursivas* para resaltar conceptos importantes.
    - Emplea tablas cuando sea útil para organizar información de forma clara.
    - Incluye ejemplos o analogías para facilitar la comprensión de conceptos complejos.
    - Si es relevante, agrega citas o referencias a modo académico.
    - Mantén la redacción clara, precisa y ordenada.
    - Que no sean más de {n_palabras} palabras.

    El objetivo es generar material didáctico que sirva como apunte profesional, completo y bien estructurado, adecuado para un entorno universitario o técnico.
    """
    
    if debug:
        return """Apunte 1"""
    
    respuesta = model.send_mesage(
        role_system="Eres un profesor muy bueno en hacer apuntes.",
        role_user=prompt,
        debug=debug
    )

    return respuesta if respuesta is not None else "[No se obtuvo respuesta]"


def create_notes(folder_md,debug, limit=None, model=MODELS['chat_gemini'], n_palabras=1000):
    
    limit_clone = limit
    for folder in os.listdir(folder_md):
        for file in os.listdir(os.path.join(folder_md, folder)):
            if file.endswith("salida.md"):
                print(f"Procesando {file}...")
                
                ruta_entrada_md = os.path.join(folder_md, folder, file)

                with open(ruta_entrada_md, "r", encoding="utf8") as f:
                    contenido = f.read()

                index = create_index(contenido, debug=debug, model=model)
                
                list_index = [line.strip().replace('> ','') for line in index.splitlines() if line.strip() != '>']
                
                text_final = ""
                tema = ""
                for i, item in tqdm(enumerate(list_index),total=len(list_index), desc="Generando documento"):
                    if item.startswith("#"):
                        if tema != "":
                            create_note_text = create_note(contenido, tema, debug=debug, model=model,n_palabras=n_palabras)
                            text_final += f"\n\n{create_note_text}"
                            tema = ""
                        
                        if item.count("#") == 3: tema = item
                        else: text_final += f"\n\n{item}"
                        
                    else: 
                        tema += f"\n{item}"

                ruta_entrada_md_note = os.path.join(folder_md, folder, file.replace(".md", "_note_final.md"))
                with open(ruta_entrada_md_note, "w", encoding="utf8") as f:
                    f.write(text_final)
                
                if limit is not None:
                    limit_clone -= 1
                    if limit_clone <= 0:
                        break


    

def convertir_md_a_docx(md_file, output_file):
    """
    Convierte un archivo Markdown a DOCX utilizando pypandoc.
    """
    try:
        pypandoc.convert_file(md_file, 'docx', outputfile=output_file)
        print(f"Documento DOCX generado: {output_file}")
    except Exception as e:
        print(f"Error al convertir a DOCX: {e}")


    
def main(
        folder_md=os.path.join('extra',"MD"),
        debug=False,
        limit=1,
        model=MODELS['chat_gemini'],
        folder_docs = os.path.join('extra',"docs"),
        save_mp3 = False,
        skipProcessing = False,
        md2pdf = False,
        md2docx = False):
    
    
    if not skipProcessing:
        create_notes(
            folder_md=folder_md,
            debug=debug,
            limit=limit,
            model=model)
    
    
    if md2docx:
        if not os.path.exists(folder_docs): os.mkdir(folder_docs)

        for folder in os.listdir(folder_md):
            for file in os.listdir(os.path.join(folder_md, folder)):
                if file.endswith("note_final.md"):
                    print(f"Convirtiendo {file} a DOCX...")
                    
                    ruta_entrada_md = os.path.join(folder_md, folder, file)
                    with open(ruta_entrada_md, "r", encoding="utf8") as f:
                        contenido = f.read()

                    
                    contenido = contenido.replace("img/", f"{folder}/img/")
                    ruta_entrada_md_tmp = os.path.join(folder_md, folder, file.replace(".md", "_tmp.md"))
                    with open(ruta_entrada_md_tmp, "w", encoding="utf8") as f:
                        f.write(contenido)


                    ruta_salida_docx = os.path.join(folder_docs, file.replace(".md", ".docx"))
                    convertir_md_a_docx(ruta_entrada_md, ruta_salida_docx)
                    
                    if save_mp3: 
                        Note2Audio.main(file=ruta_entrada_md_tmp,
                        audio_folder="audio",
                        play_song=False)
                
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de documentos a partir de PDFs")
    parser.add_argument('-l', '--limit', type=int, default=None, help="Número máximo de PDFs a procesar")
    parser.add_argument('-d', '--debug', action='store_true', help="Activar modo de depuración")
    parser.add_argument('-f', '--folder_pdfs', type=str, default="PDFs", help="Carpeta de entrada con PDFs")
    parser.add_argument('-s', '--folder_md', type=str, default="MD", help="Carpeta de salida para documentos generados")
    parser.add_argument('-m', '--model', type=str, choices=MODELS.keys(), default='chat_gemini', help="Modelo a utilizar para la generación de contenido")
    
    parser.add_argument('--skipProcessing', action='store_true', help="Si se desea omitir el procesamiento de los PDFs")
    parser.add_argument('--md2pdf', action='store_true', help="Si se desea convertir el archivo a PDF después de generarlo")
    parser.add_argument('--md2docx', action='store_true', help="Si se desea convertir el archivo a DOCX después de generarlo")
    parser.add_argument('--docs_folder', type=str, default="docs", help="Carpeta de salida para documentos generados")
    parser.add_argument('--save_mp3', action='store_true', help="Booleano para crear el audio de los apuntes generados")
    
    args = parser.parse_args()

    limit = args.limit if args.limit is not None else None
    folder_pdfs = args.folder_pdfs if args.folder_pdfs else os.path.join('extra',"PDFs")
    folder_md = args.folder_md if args.folder_md else os.path.join('extra',"MD")
    dpi = args.dpi if args.dpi else 200
    model = MODELS[args.model] if args.model else MODELS['chat_gemini']
    debug = args.debug if args.debug else False

    skipProcessing = args.skipProcessing if args.skipProcessing else False
    md2pdf = args.md2pdf if args.md2pdf else False
    md2docx = args.md2docx if args.md2docx else False
    docs_folder = args.docs_folder if args.docs_folder else os.path.join('extra',"docs")
    
    main(
        folder_md=os.path.join('extra',"MD"),
        debug=False,
        limit=1,
        model=model,
        folder_docs = docs_folder,
        md2docx= md2docx,
        md2pdf= md2pdf,
        save_mp3 = False)