FROM n8nio/n8n:latest

USER root

# Install Python, pip, and system packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev gcc \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libglib2.0-dev \
    && python3 -m pip install --no-cache-dir opencv-python PyMuPDF

# Copy your cropping script into the image
COPY dashed_crop.py /data/scripts/dashed_crop.py

USER node
