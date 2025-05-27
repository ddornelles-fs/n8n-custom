FROM node:20-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev gcc \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libglib2.0-dev \
    libgl1 \
    && python3 -m pip install --no-cache-dir opencv-python PyMuPDF

RUN npm install -g n8n

COPY data/scripts/dashed_crop.py /data/scripts/dashed_crop.py
COPY ./n8n-scripts /data/scripts
RUN mkdir -p /data/output


EXPOSE 5678
CMD ["n8n"]
