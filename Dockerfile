FROM node:18-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev gcc \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libglib2.0-dev

RUN python3 -m pip install --no-cache-dir opencv-python PyMuPDF

RUN npm install -g n8n@1.94.0

ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=securepassword
ENV N8N_HOST=0.0.0.0
ENV WEBHOOK_URL=https://n8n-custom-9a5c.onrender.com

EXPOSE 5678

CMD ["n8n"]
