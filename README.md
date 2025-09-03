# 📚 Slides 2 Notes

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Build](https://img.shields.io/badge/build-passing-brightgreen) ![Dependencies](https://img.shields.io/badge/dependencies-managed-success)

> Genera apuntes a partir de tus presentaciones PDF usando modelos de IA generativa.

> Generate clean study notes from PDF slides using Generative AI.

---

## 📑 Índice
1. [Descripción](#descripción)
2. [Instalación rápida](#instalación-rápida)
3. [Uso básico](#uso-básico)
4. [Ejemplos avanzados](#ejemplos-avanzados)
5. [Arquitectura](#arquitectura)
6. [API de comandos](#api-de-comandos)
7. [Contribuir](#contribuir)
8. [Licencia](#licencia)
9. [Contacto](#contacto)
10. [English Quick Guide](#english-quick-guide)

## Descripción
Slides 2 Notes automatiza la creación de apuntes a partir de presentaciones en PDF.
Convierte cada diapositiva en una imagen, la interpreta con modelos como **GPT-4o** o **Gemini 1.5** y genera un documento en Markdown editable.
Posteriormente permite refinar los apuntes, generar versiones extendidas e incluso crear audio a partir de texto.

## Instalación rápida
Consulta la guía completa en [docs/INSTALL.md](docs/INSTALL.md). Resumen:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r extra/requirements.txt
# o bien
pip install -e .
```
Configura tus claves en un archivo `.env`:
```bash
OPENAI_API_KEY="tu_clave"
GOOGLE_API_KEY="tu_clave"
```

## Uso básico
Convierte todas las presentaciones del directorio `PDFs` en notas Markdown:
```bash
python Slides2Notes.py --folder_pdfs extra/PDFs --folder_save extra/MD --md2docx
```
Refina los apuntes generados y crea versiones temáticas:
```bash
python Notes2Notes.py --debug --limit 1 --md2docx
```
Convierte un apunte en audio:
```bash
python Note2Audio.py --file extra/MD/proyecto_salida_note_final.md
```

## Ejemplos avanzados
- Procesar un único PDF con DPI personalizado y salida a PDF:
```bash
python Slides2Notes.py -l 1 --dpi 300 --md2pdf
```
- Ejecutar la tubería completa:
```bash
python AllInOne.py
```

## Arquitectura
Ver la descripción detallada en [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Resumen:
```
PDFs → Slides2Notes → Markdown
Markdown → Notes2Notes → Apuntes extendidos
Apuntes → Note2Audio → MP3
```
Los modelos de IA se aíslan en `models/` para facilitar la integración con diferentes proveedores.

## API de comandos
Se exponen interfaces de línea de comandos para cada módulo principal. Consulta [docs/API.md](docs/API.md) para todos los parámetros disponibles.

## Contribuir
Las guías de estilo, issues y PRs se detallan en [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

## Licencia
Este proyecto está disponible bajo la licencia [MIT](LICENSE).

## Contacto
¿Dudas o sugerencias? Abre un issue o escríbenos a **opensource@example.com**.

## English Quick Guide
Slides 2 Notes automatically turns PDF slides into study notes using GPT-4o or Gemini. Install with `pip install -e .`, set your API keys in a `.env` file and run the CLI tools:
- `Slides2Notes.py` converts slides to Markdown.
- `Notes2Notes.py` expands notes.
- `Note2Audio.py` generates MP3 audio.
Contributions and issues are welcome!
