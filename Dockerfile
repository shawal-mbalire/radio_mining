FROM python:3.8-slim
WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y git ffmpeg && \
    rm -rf /var/lib/apt/lists/*  # Clean up

    RUN git clone https://github.com/Marconi-Lab/radio_mining.git .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["bash"]
