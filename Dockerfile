FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a simple web server to satisfy Cloud Run's requirements
RUN echo 'import os, http.server, socketserver, threading, time\n\
from celery_app import app\n\
\n\
def start_server():\n\
    port = int(os.environ.get("PORT", 8080))\n\
    handler = http.server.SimpleHTTPRequestHandler\n\
    with socketserver.TCPServer(("", port), handler) as httpd:\n\
        print(f"Serving at port {port}")\n\
        httpd.serve_forever()\n\
\n\
def start_celery():\n\
    print("Starting Celery worker")\n\
    app.worker_main([\n\
        "worker",\n\
        "--loglevel=info",\n\
        "-P", "eventlet",\n\
        "--concurrency=4",\n\
        "--prefetch-multiplier=1",\n\
    ])\n\
\n\
if __name__ == "__main__":\n\
    # Start HTTP server in a separate thread\n\
    server_thread = threading.Thread(target=start_server, daemon=True)\n\
    server_thread.start()\n\
    \n\
    # Start Celery worker in the main thread\n\
    start_celery()\n\
' > run_combined.py

# Expose the port
EXPOSE 8080

# Command to run the service
CMD ["python", "run_combined.py"]