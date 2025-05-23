FROM public.ecr.aws/docker/library/python:3.9-slim

WORKDIR /app

# Install production WSGI server
RUN pip install waitress

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["waitress-serve", "--port=8080", "app:app"]