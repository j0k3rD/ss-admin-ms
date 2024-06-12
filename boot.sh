#!/bin/bash
uvicorn src.main:app --reload --host 192.168.18.4 --port 5000
source .venv/bin/activate

