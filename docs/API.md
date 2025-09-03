# 📖 API de comandos

## Slides2Notes
Convierte PDFs en archivos Markdown.

```bash
python Slides2Notes.py [-l LIMIT] [--dpi DPI] [--md2docx] [--md2pdf] [--folder_pdfs RUTA] [--folder_save RUTA]
```

### Parámetros principales
| Opción | Descripción | Valor por defecto |
|--------|-------------|------------------|
| `-l`, `--limit` | Número máximo de PDFs a procesar | `None` |
| `--dpi` | Resolución de las imágenes | `200` |
| `--md2docx` | Genera un DOCX adicional | `False` |
| `--md2pdf` | Genera un PDF adicional | `False` |
| `--folder_pdfs` | Carpeta de entrada | `PDFs` |
| `--folder_save` | Carpeta de salida Markdown | `MD` |

## Notes2Notes
Genera apuntes extendidos desde Markdown.
```bash
python Notes2Notes.py [--limit N] [--n_palabras N] [--md2docx]
```

| Opción | Descripción | Defecto |
|--------|-------------|---------|
| `--limit` | Procesa solo N documentos | `1` |
| `--n_palabras` | Máximo de palabras por tema | `1000` |
| `--md2docx` | Exporta a DOCX | `False` |
| `--save_mp3` | Genera audio a partir del Markdown | `False` |

## Note2Audio
Convierte un archivo Markdown en audio MP3.
```bash
python Note2Audio.py --file RUTA --audio_folder audio [--play_song]
```

| Opción | Descripción | Defecto |
|--------|-------------|---------|
| `--file` | Archivo Markdown de entrada | `MD/ejemplo.md` |
| `--audio_folder` | Carpeta de salida | `audio` |
| `--play_song` | Reproduce el audio al finalizar | `False` |

## Interfaces de los modelos
Tanto `chat_gpt` como `chat_gemini` exponen:
- `send_image(image, role_user, role_system, debug=False)`
- `send_mesage(role_user, role_system, debug=False)`

---
## English summary
CLI entry points: `Slides2Notes.py` for PDFs → Markdown, `Notes2Notes.py` to create detailed notes, and `Note2Audio.py` for text-to-speech. Each script provides flags for limits, output formats and model selection.
