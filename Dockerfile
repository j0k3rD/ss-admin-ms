ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid ${UID} \
    appuser

# Instalando dependencias
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=/requirements/dev.txt,target=/src/requirements.txt \
    python -m pip install -r requirements.txt

COPY . .

# Copiar el script boot.sh
COPY boot.sh /usr/local/bin/boot.sh
RUN chmod +x /usr/local/bin/boot.sh

EXPOSE 5001

# Cambiar el comando por defecto
CMD ["/usr/local/bin/boot.sh"]
