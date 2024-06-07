#!/bin/bash
uvicorn src.main:app --reload --host 172.27.191.61 --port 5000
source .venv/bin/activate

