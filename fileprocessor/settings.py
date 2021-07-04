#this file contains secrets and env variables
from os import getenv,path
from dotenv import load_dotenv

#load the env
load_dotenv()

#set them variables (don't need the yet )
# SECRET_KEY = getenv('SECRET_KEY')

username = getenv('DB_ADMIN_USER')

password = getenv('DB_ADMIN_PASS')

dbname = getenv('DB_NAME')

# admin_access_key = getenv('ADMIN_ACCESS_KEY')

PDF_UPLOAD_FOLDER = getenv('PDF_UPLOAD_FOLDER')
IMAGE_UPLOAD_FOLDER = getenv('IMAGE_UPLOAD_FOLDER')
DOWNLOAD_FOLDER = getenv('DOWNLOAD_FOLDER')
#Handling defaults..
if PDF_UPLOAD_FOLDER == None:
    PDF_UPLOAD_FOLDER = "uploaded/pdf"
if IMAGE_UPLOAD_FOLDER == None:
    IMAGE_UPLOAD_FOLDER = "uploaded/image"