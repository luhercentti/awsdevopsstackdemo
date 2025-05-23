FROM public.ecr.aws/docker/library/python:3.9-slim

WORKDIR /app

# Install only gunicorn (remove waitress)
RUN pip install gunicorn

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# Use only gunicorn with optimized settings
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "app:app"]