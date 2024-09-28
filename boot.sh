#!/bin/bash

# Esperar 10 segundos
sleep 10

# Activar el entorno virtual
source .venv/bin/activate

# Iniciar la aplicación
uvicorn src.main:app --reload --host 0.0.0.0 --port 5001
