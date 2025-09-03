# 🤝 Guía de contribución

Gracias por tu interés en mejorar **Slides 2 Notes**.

## Cómo empezar
1. Haz un fork del repositorio y clónalo.
2. Crea una rama descriptiva a partir de `main`.
3. Asegúrate de que los cambios pasan las comprobaciones:
   ```bash
   python -m py_compile *.py models/*.py
   ```
4. Envía un Pull Request describiendo claramente el problema resuelto o la mejora propuesta.

## Estilo de código
- Sigue la [PEP8](https://peps.python.org/pep-0008/).
- Usa `black` y `isort` si haces cambios en el código.
- Incluye docstrings en español.

## Reportar errores
Abre un issue con:
- Pasos para reproducir.
- Comportamiento esperado vs. obtenido.
- Información de entorno.

## Sugerir características
Utiliza la etiqueta `enhancement` en los issues y explica el caso de uso.

## Código de conducta
Se espera una comunicación respetuosa. Las conductas abusivas resultarán en la expulsión del proyecto.

---
## English summary
Fork the repo, create a branch, run `python -m py_compile *.py models/*.py`, and open a PR. Follow PEP8 and provide clear issue reports or feature requests.
