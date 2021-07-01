#this file contains secrets and env variables
from os import getenv,path
from dotenv import load_dotenv

#load the env
load_dotenv()

#set them variables (don't need the yet )
SECRET_KEY = getenv('SECRET_KEY')

username = getenv('DB_ADMIN_USER')

password = getenv('DB_ADMIN_PASS')

dbname = getenv('DB_NAME')

admin_access_key = getenv('ADMIN_ACCESS_KEY')

#init firebase settings
# firebase_config = {
#     'apiKey':getenv('FIREBASE_APIKEY'),
#     'authDomain':getenv('FIREBASE_AUTHDOMAIN'),
#     'projectId':getenv('FIREBASE_PROJECTID'),
#     'storageBucket':getenv('FIREBASE_STORAGEBUCKET'),
#     'messagingSenderId':getenv('FIREBASE_MESSAGINGSENDERID'),
#     'appId':getenv('FIREBASE_APPID'),
#     'measurementId':getenv('FIREBASE_MEASUREMENTID'),
#     'databaseURL':None,
#     'serviceAccount':path.abspath(getenv('FIREBASE_SERVICE_ACCOUNT_JSON_PATH'))
# }
# ALLOWED_POSTER_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif','bmp','svg'}