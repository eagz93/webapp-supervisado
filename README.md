# App NPL - Despliegue en Streamlit

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Desplegar en Streamlit Community Cloud

1. Sube este proyecto a GitHub.
2. En Streamlit Cloud crea una nueva app conectando el repositorio.
3. Configura como archivo principal:

```text
streamlit_app.py
```

4. Streamlit instalará automáticamente dependencias desde `requirements.txt`.

## Estructura importante

- `streamlit_app.py`: punto de entrada para Cloud.
- `app/app.py`: app principal.
- `app/dashboard.py`: dashboard alternativo.
- `models/*.pkl`: artefactos del modelo necesarios en producción.
