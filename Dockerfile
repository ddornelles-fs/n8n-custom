# Use the full official n8n image with all nodes preinstalled
FROM n8nio/n8n:1.94.0

# Install system packages for your script
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev gcc \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libglib2.0-dev \
    && python3 -m pip install --no-cache-dir opencv-python PyMuPDF

# Copy your Python script into the container
COPY dashed_crop.py /data/scripts/dashed_crop.py

# Ensure persistent data storage
VOLUME ["/home/node/.n8n"]

# Set environment variables
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=securepassword
ENV N8N_HOST=0.0.0.0
ENV WEBHOOK_URL=http://localhost:5678

# Switch back to the node user for security
USER node
