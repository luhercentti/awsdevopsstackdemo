FROM public.ecr.aws/docker/library/python:3.9-slim

WORKDIR /app

# Install production dependencies
RUN pip install waitress gunicorn

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-create log directory
RUN mkdir -p /var/log/app

EXPOSE 8080

# Use both waitress and gunicorn for maximum reliability
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8080 --workers 2 --threads 4 --access-logfile - --error-logfile - app:app & waitress-serve --port=8080 app:app"]