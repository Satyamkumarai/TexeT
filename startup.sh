file="../processes.tmp"
touch $file 
cd webserver/
source env/bin/activate
flask run -h 0.0.0.0 &
echo kill -9 $!>>$file
deactivate 
cd ../fileprocessor 
source env/bin/activate
python main.py&
echo kill -9 $!>>$file
deactivate 
cd ../cleaner
source env/bin/activate
python main.py&
echo kill -9 $!>>$file
deactivate 
cd ../imageprocessor
source env/bin/activate
python main.py&
echo kill -9 $!>>$file
echo rm \$0>>$file
deactivate

