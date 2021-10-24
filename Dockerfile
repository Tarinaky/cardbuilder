FROM python:3.10-bullseye

RUN apt-get update && apt-get install -y \
		libsdl2-dev=2.0.14+dfsg2-3 \
		libsdl2-ttf-dev=2.0.15+dfsg1-1 \
		libsdl2-mixer-dev=2.0.4+dfsg1-3 \
		libsdl2-image-dev=2.0.5+dfsg1-2 \
		libportmidi-dev=1:217-6

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD ./py /app

WORKDIR /app
ENTRYPOINT ["python3", "app.py"]
