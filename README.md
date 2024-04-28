# LucidDreamsTest


#### Docker-compose<a name="docker"></a>
___
Before using docker, you must be Docker Desktop running.
<br/> 
In directory with docker-compose.yml need run.
<br/>
The FastAPI application will be run after DB is ready to connect.
```
docker-compose up --build
```

For stop container, you need use `Ctrl+C` or 
```
docker-compose stop
```

For renewal him, you need run
```
docker-compose up
```

For delete containers with volumes and images, you need to run
```
docker-compose down --volumes --rmi local
```

<br>
<br>

Go to OpenAPI<a name="go_to_site"></a>
---
Next, follow the path http://localhost:8000/docs
<br>
