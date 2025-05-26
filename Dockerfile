# Use the official full n8n image with all nodes preinstalled
FROM n8nio/n8n:1.94.0

# Switch to root to install python + system deps
USER root

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev gcc \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libglib2.0-dev

RUN python3 -m pip install --no-cache-dir opencv-python PyMuPDF

# Copy your cropping script
COPY dashed_crop.py /data/scripts/dashed_crop.py

# Switch back to node user
USER node

# Set env variables (set in Render dashboard or here)
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=securepassword
ENV N8N_HOST=0.0.0.0
ENV WEBHOOK_URL=https://n8n-custom-9a5c.onrender.com   # Replace with your actual public URL

EXPOSE 5678

# Start n8n
CMD ["n8n"]
