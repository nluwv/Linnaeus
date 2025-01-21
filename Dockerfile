FROM python:3.12-slim-bookworm
RUN apt-get update && \
    apt-get upgrade && \
    apt-get install -y git
WORKDIR /app
COPY . .
RUN pip3 install -r requirements_clean.txt

EXPOSE 5000	