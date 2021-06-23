FROM python:3.8-slim-buster
WORKDIR /texet
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt 
COPY  . .
EXPOSE 3000
CMD ["python3","-m" , "flask","run","--host=0.0.0.0"]
