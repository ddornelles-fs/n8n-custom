FROM node:20-bullseye

# Set working directory
WORKDIR /app

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev gcc \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libglib2.0-dev \
    libgl1 \
    && python3 -m pip install --no-cache-dir opencv-python PyMuPDF

# Install n8n globally
RUN npm install -g n8n

# Create required folders
RUN mkdir -p /data/scripts /data/output

# Copy script into container
COPY ./n8n-scripts/dashed_crop.py /data/scripts/dashed_crop.py

# Set correct permissions just in case
RUN chmod +x /data/scripts/dashed_crop.py

# Expose n8n port
EXPOSE 5678

# Run n8n
CMD ["n8n"]
