From python:3.8.3

RUN pip install cherrypy imageio 
WORKDIR = /usr/src/
COPY see/ ./see
COPY server.py ./server.py

EXPOSE 8080

ENTRYPOINT ["python", "server.py"]