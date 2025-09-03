# 🛠️ Instalación

Esta guía describe varios métodos para instalar **Slides 2 Notes**.

## Requisitos previos
- Python 3.10 o superior
- [Poppler](https://poppler.freedesktop.org/) para `pdf2image`
- Claves de API para OpenAI y/o Google Gemini

## 1. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

## 2. Variables de entorno
Crea un archivo `.env` en la raíz del proyecto:
```bash
OPENAI_API_KEY=tu_clave
GOOGLE_API_KEY=tu_clave
```

## 3. Instalación con requirements.txt
```bash
pip install -r extra/requirements.txt
```

## 4. Instalación como paquete
El repositorio incluye un `pyproject.toml` mínimo que permite instalar el proyecto como paquete editable:
```bash
pip install -e .
```

## 5. Instalación con pip (publicación futura)
Cuando el paquete esté disponible en PyPI:
```bash
pip install slides2notes
```

## 6. Verificación
Compila los módulos para asegurarte de que las dependencias están correctamente instaladas:
```bash
python -m py_compile *.py models/*.py
```

---
## English summary
Steps: create a virtualenv, set `OPENAI_API_KEY`/`GOOGLE_API_KEY` in a `.env` file, install dependencies with `pip install -r extra/requirements.txt` or `pip install -e .`, and verify with `python -m py_compile`.
