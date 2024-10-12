# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.10

FROM python:${PYTHON_VERSION}-slim

LABEL fly_launch_runtime="flask"

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y nodejs npm
RUN npm install tailwindcss
RUN npx tailwindcss -i ./src/styles.css -o ./static/styles.css

EXPOSE 8080

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
