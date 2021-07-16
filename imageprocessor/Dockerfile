FROM jbarlow83/ocrmypdf:latest
WORKDIR /fileprocessor
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install python3-distutils -y 
RUN apt-get install ca-certificates -y
RUN pip install -r requirements.txt 
COPY  . .
ENTRYPOINT [ "python3" ]

CMD ["main.py"]
