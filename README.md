# radio_mining

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
docker exec -it radio bash
```
