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
```bash
docker volume create portainer_data
```

```bash
docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```
