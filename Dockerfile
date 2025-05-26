# Use official n8n image (Alpine-based)
FROM n8nio/n8n:1.94.0

# Switch to root to install system dependencies
USER root

# Install dependencies with apk (Alpine's package manager)
RUN apk update && apk add --no-cache \
    python3 py3-pip python3-dev gcc musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    glib-dev libxrender libxext libsm \
    && pip3 install --no-cache-dir opencv-python PyMuPDF

# Copy your Python script into the container
COPY dashed_crop.py /data/scripts/dashed_crop.py

# Set environment variables
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=securepassword
ENV N8N_HOST=0.0.0.0
ENV WEBHOOK_URL=http://localhost:5678

# Expose default port and persist data
EXPOSE 5678
VOLUME ["/home/node/.n8n"]

# Switch back to node user for runtime
USER node
