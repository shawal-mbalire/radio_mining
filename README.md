# radio_mining

Clone download the dockerfile

```bash
wget https://raw.githubusercontent.com/shawal-mbalire/radio_mining/main/Dockerfile
```

Build the container from the dockerfile

```bash
docker build -t containerradio:v1 .
```

Start the container 

```bash
docker run -t -d --name radiomining containerradio:v1
```

connect to the docker container to run commands inside it

```bash
docker exec -it radiomining bash
```
