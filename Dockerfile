FROM python:3.11-slim
WORKDIR /app
EXPOSE 8000
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir pipx==1.7.1 && pipx install --global poetry==1.8.3
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    poetry install --no-root --no-cache
COPY . .
CMD ["python", "main.py"]
