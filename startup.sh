cd webserver/
source env/bin/activate
flask run &
deactivate 
cd ../fileprocessor 
source env/bin/activate
python main.py&
deactivate 
cd ../cleaner
source env/bin/activate
python main.py&
deactivate 
cd ../imageprocessor
source env/bin/activate
python main.py&
deactivate

