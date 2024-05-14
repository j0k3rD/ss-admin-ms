#!/bin/bash
source .venv/bin/activate
uvicorn main:app --reload --host 192.168.18.4 --port 5000