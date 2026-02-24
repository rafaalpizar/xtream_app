# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY python/ .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose server port
EXPOSE 8080

# Default command (can be overridden)
# By default, run the server
CMD ["python", "server.py"]
