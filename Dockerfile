FROM node:18-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV and PyMuPDF
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev gcc \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libglib2.0-dev \
    && python3 -m pip install --no-cache-dir opencv-python PyMuPDF

# Install n8n with all nodes including Dropbox Trigger
RUN npm install -g n8n@1.94.0

# Enable dev/community nodes
ENV N8N_ENABLE_NODE_DEV=true

# Copy your cropping script
COPY dashed_crop.py /data/scripts/dashed_crop.py

# Create data volume
RUN mkdir -p /home/node/.n8n
VOLUME ["/home/node/.n8n"]

# Set environment variables
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=securepassword
ENV N8N_HOST=0.0.0.0
ENV WEBHOOK_URL=http://localhost:5678

EXPOSE 5678

# Start n8n
CMD ["n8n"]
