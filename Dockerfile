FROM alpine:latest
FROM python:3.10

WORKDIR /app

# copying requirement.txt file to the container
COPY './requirements.txt' .

# install the package mentioned in requirements.txt
RUN pip install -r requirements.txt

COPY . . 

EXPOSE 5000

ENTRYPOINT ["python", "estart.py"]


