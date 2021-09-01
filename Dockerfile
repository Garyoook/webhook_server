FROM python:3.8-alpine

WORKDIR '/srv/minieye/webhook_massage_server/'

COPY webhook_server.py ./

RUN pip install requests

CMD ["python3", "webhook_server.py"]