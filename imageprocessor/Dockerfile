FROM python:latest
WORKDIR /imageprocessor
COPY requirements.txt requirements.txt
RUN apt-get update
# RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install python3-opencv -y
# RUN apt-get install python3-distutils -y 
# RUN apt-get install ca-certificates -y
RUN python3 -m pip install --upgrade pip 
RUN pip install -r requirements.txt 
#COPY  ./convert.py .
#COPY  ./page_extractor .
#COPY  ./main.py .
#COPY  ./schema.py .
#COPY ./settings.py .
#COPY ./.env .
COPY . . 
ENTRYPOINT [ "python3" ]

CMD ["main.py"]
