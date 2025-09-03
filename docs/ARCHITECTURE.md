# 🏗️ Arquitectura

Slides 2 Notes se organiza en módulos independientes que forman una cadena de procesamiento:

```
PDFs ──▶ Slides2Notes ──▶ Markdown ──▶ Notes2Notes ──▶ Apuntes ──▶ Note2Audio ──▶ MP3
```

## Directorios principales
| Carpeta | Rol |
|--------|-----|
| `extra/` | Recursos de ejemplo, requisitos y PDFs de prueba |
| `models/` | Adaptadores para distintos proveedores de IA (OpenAI, Gemini) |
| `docs/` | Documentación del proyecto |

## Módulos
- **Slides2Notes.py**: convierte cada PDF en un conjunto de imágenes, obtiene una explicación mediante IA y genera un Markdown.
- **Notes2Notes.py**: a partir de los Markdown generados crea índices y apuntes extendidos.
- **Note2Audio.py**: transforma notas en archivos de audio usando `edge_tts`.
- **AllInOne.py**: ejecuta el flujo completo con una configuración básica.

## Modelo de IA
Los clientes de modelos se encuentran en `models/` y exponen una interfaz común:
- `send_image(image, role_user, role_system, debug)`
- `send_mesage(role_user, role_system, debug)`

## Flujo de datos
1. **Ingesta**: PDFs colocados en `extra/PDFs`.
2. **Conversión**: `Slides2Notes` genera Markdown en `extra/MD`.
3. **Refinamiento**: `Notes2Notes` procesa esos Markdown y produce archivos `*_note_final.md`.
4. **Exportación**: conversión opcional a DOCX/PDF y audio.

---
## English summary
Modular pipeline: PDFs → `Slides2Notes` → Markdown → `Notes2Notes` → rich notes → `Note2Audio` → MP3. Models are abstracted in `models/` for easy provider swapping.
