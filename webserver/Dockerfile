FROM python:latest
WORKDIR /webserver
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install python3-distutils -y 
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt 
RUN pip uninstall bson pymongo -y 
RUN pip install pymongo 
COPY . . 
EXPOSE 3000
# CMD ["python3","-m" , "flask","run","--host=0.0.0.0"]
ENTRYPOINT [ "gunicorn" ]
CMD ["-b","0.0.0.0:3000" ,"texet:create_app(False)"]
