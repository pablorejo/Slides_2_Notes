# Introducción
Este programa creará anotaciones y explicaciones sobre diapositivas en PDF y las guardará en fichero markdown para poder editarse y será tarea del usuario pasarlo a PDF o no.

# Uso
Para usar la herramienta tendremos que seguir los siguientes pasos:

1. Creamos un fichero .env en donde guardaremos las claves de Chat GPT o de Gemini fichero '.env' y dentro ponemos lo siguiente.
```bash
OPENAI_API_KEY=TU_CLAVE_AQUÍ
GOOGLE_API_KEY=TU_CLAVE_AQUÍ
```

2. Tenemos que tener instalado Python 3 y además instalar las dependencias necesarias con PIP:
```bash
pip install -r requirements.txt
```

3. A continuación solo necesitamos ejecutar el programa con el siguiente comando para obtener más información:
```bash
python .\Slides2Notes.py --help
```
