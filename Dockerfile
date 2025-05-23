FROM public.ecr.aws/docker/library/python:3.9-slim

WORKDIR /app

# Install production server
RUN pip install gunicorn

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# Use only Gunicorn with proper worker configuration
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]