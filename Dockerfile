FROM python:3.9-slim

WORKDIR /app

# First copy only requirements to cache them in docker layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip freeze > installed_versions.txt  # For debugging

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]