# 🚀 Uso de Slides 2 Notes

## 1. Convertir diapositivas en apuntes
Coloca tus PDFs en `extra/PDFs` y ejecuta:
```bash
python Slides2Notes.py --folder_pdfs extra/PDFs --folder_save extra/MD
```
Opciones comunes:
| Opción | Descripción |
|--------|-------------|
| `-l`, `--limit` | Número máximo de PDFs a procesar |
| `--dpi` | Resolución de las imágenes generadas |
| `--md2docx` / `--md2pdf` | Exportar el resultado a DOCX o PDF |

## 2. Refinar apuntes existentes
Si ya tienes archivos Markdown generados, puedes ampliarlos tema por tema:
```bash
python Notes2Notes.py --folder_md extra/MD --md2docx
```
Parámetros útiles:
- `--limit`: procesa solo un número determinado de documentos.
- `--n_palabras`: controla la extensión de cada apunte.

## 3. Convertir texto a audio
```bash
python Note2Audio.py --file extra/MD/tema_salida_note_final.md --audio_folder audio
```
Añade `--play_song` para reproducir el audio automáticamente.

## 4. Tubería completa
```bash
python AllInOne.py
```
Este script ejecuta `Slides2Notes` y `Notes2Notes` con opciones recomendadas.

---
## English summary
Run `Slides2Notes.py` to turn PDFs into Markdown notes, `Notes2Notes.py` to enrich them, `Note2Audio.py` to get MP3 files, and `AllInOne.py` to execute the full pipeline.
