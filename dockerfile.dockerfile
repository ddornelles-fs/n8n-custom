FROM n8nio/n8n:latest

USER root

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && pip3 install opencv-python pymupdf

USER node
