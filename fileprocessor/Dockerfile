# Latest version seems to use ubunutu which has problems with the apt-get update because of some bug (gpg key error)
# https://stackoverflow.com/questions/66319610/gpg-error-in-ubuntu-21-04-after-second-apt-get-update-during-docker-build
FROM jbarlow83/ocrmypdf:v11.0.0  
WORKDIR /fileprocessor
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install python3-distutils -y 
RUN apt-get install ca-certificates -y
RUN pip install -r requirements.txt 
COPY  . .

ENTRYPOINT [ "python3" ]

CMD ["main.py"]
