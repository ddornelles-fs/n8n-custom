FROM node:20-bullseye

WORKDIR /app

# Install Python and required libraries
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev gcc \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libglib2.0-dev \
    libgl1 \
    && python3 -m pip install --no-cache-dir opencv-python PyMuPDF

# Install n8n globally
RUN npm install -g n8n

# Copy your Python script from ./data/scripts to /data/scripts inside container
COPY data/scripts/dashed_crop.py /data/scripts/dashed_crop.py

# Make sure the output folder exists
RUN mkdir -p /data/output

EXPOSE 5678
CMD ["n8n"]
