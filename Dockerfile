FROM python:3.11-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "flask", "--app" , "sandbox", "run", "--host=0.0.0.0"]
