FROM python:latest
WORKDIR /cleaner
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install python3-distutils -y 
RUN apt-get install ca-certificates -y
RUN python3 -m pip install --upgrade pip 
RUN pip install -r requirements.txt 
RUN pip uninstall pymongo bson -y
RUN pip install pymongo
COPY  . .
ENTRYPOINT [ "python3" ]

CMD ["main.py"]
