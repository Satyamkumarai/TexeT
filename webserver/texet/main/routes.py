import uuid
import os
from subprocess import PIPE, run
from texet.main.constants import FileStatus
from texet.settings import DOWNLOAD_FOLDER,PDF_UPLOAD_FOLDER,IMAGE_UPLOAD_FOLDER
from bson.objectid import  ObjectId
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    Response,
    json,
    send_from_directory)
from texet.extensions import mongo                  #The mongo client!
from texet.main.utils import allowed_file ,do_ocrmypdf , json_resp ,add_file_to_db
from werkzeug.utils import secure_filename
from flask import current_app

bp = Blueprint('main',__name__)



@bp.route('/',methods = ['GET'])
def root():
    return render_template("index.html",title="TexeT")





@bp.route('/uploadpdf',methods=['GET'])
def uploadpdf( ):
    return render_template("upload/upload.html")





#Scan Html Page
@bp.route('/scan',methods=['GET'])
def scan():
    return render_template("scan/scan.html",title="TeXeT")







#Testing Data base 
@bp.route('/test')
def testdb():
    docs = mongo.db.queue.count()
    return Response(f"count={docs}",200)







#Pdf Download 
@bp.route("/pdf/download/<uuid>" ,methods=['GET'])
def download_pdf(uuid):
    work_doc = mongo.db.queue.find_one({"input":uuid})
    if work_doc:
        status = work_doc.get('status')
        if status == FileStatus.uploaded.value:
            return "Server Busy wait till your file gets processed !"
        elif status == FileStatus.success.value:
            return  send_from_directory(os.path.join(current_app.instance_path, DOWNLOAD_FOLDER),str(work_doc['output'])+".pdf")
        else :
            return status
    return Response(json_resp("File Not Found!",1),404,mimetype="application/json")







@bp.route("/pdf/upload",methods=['POST'])
def process_pdf():
    if request.method == "POST":
        if "file" not in request.files:
            return Response(json_resp("No file in POST",1), 400, mimetype='application/json')
        file = request.files["file"]
        if file.filename == "":
            return Response(json_resp("Empty filename",1), 400, mimetype='application/json')
        if not allowed_file(file.filename):
            return Response(json_resp("Invalid filename",1), 400, mimetype='application/json')
        if file and allowed_file(file.filename):

            #I am not checking if the file already exists cuz the possibility of that being the case is low (since we have a 128 bit random number)
            #Create a random uuid for the file 
            file_uuid = str(uuid.uuid4())   

            #save the file locally 
            local_save_dir = os.path.join(current_app.instance_path, PDF_UPLOAD_FOLDER)
            local_filename = os.path.join(local_save_dir, secure_filename(file_uuid+".pdf"))
            file.save(local_filename)
            print("Saving the file to %s " % local_filename)  #DEBUG

            #set the data for the queeue
            task = {
                "input":file_uuid,
                "output":file_uuid+"-download",
                "isImage":False,
                "status":FileStatus.uploaded.value
            }



            # upload the task to the db queue 
            mongo.db.queue.insert_one(task) #DEBUG
            print("Uploaded Task to DB",task)
            # run(["cp",os.path.join(current_app.instance_path, PDF_UPLOAD_FOLDER, secure_filename(file_uuid+".pdf")),os.path.join(current_app.instance_path, DOWNLOAD_FOLDER, secure_filename(file_uuid+"-download.pdf"))])            
            #return the download Url
            download_url = url_for('main.download_pdf',uuid=file_uuid)
            print(f"Returning Download url:{download_url}")
            return Response(json_resp("File Uploaded!",0,download_url))

        return Response(json_resp("Some other problem",1), 400, mimetype='application/json')









# Handling Uploading images
@bp.route("/images/upload",methods=['POST'])
def upload_images():
    if request.method == 'POST':
        if "images" not in request.files:
            return Response(json_resp("No images in POST",1), 400, mimetype='application/json')
        filelist  = request.files.getlist('images')
        print("The image List :",filelist)  #DEBUG
        #make sure that all the files are right if any of them are not return error resp
        for file in filelist:
            if file :
                if file.filename == "":
                    return Response(json_resp("Empty filename",1), 400, mimetype='application/json')
                if not allowed_file(file.filename,image=True):
                    return Response(json_resp("Invalid filename",1), 400, mimetype='application/json')
            else:
                print("EMPTY FILE ? ")  #DEBUG
                print(file )#DEBUG
                return Response(json_resp("Empty file !",1), 400, mimetype='application/json')
        #For Each file 
        folder_uuid = str(uuid.uuid4())
        #Create the folder ..
        local_save_dir  = os.path.join(current_app.instance_path,IMAGE_UPLOAD_FOLDER)
        local_save_dir  = os.path.join (local_save_dir,folder_uuid)
        print("Saving the file in %s dir "%local_save_dir) #DEBUG

        #again not bothering about exising folders in that name since they are not likely to occur
        os.makedirs(local_save_dir,  exist_ok=True)

        #For each file in the  local dir
        for count,file in enumerate( filelist,1):               #the images will be save as <uuid><count>.<ext>
            #save the file 
            file_ext = file.filename.rsplit(".", 1)[1].lower()
            local_save_filename =    secure_filename(folder_uuid+str(count)+f".{file_ext}")
            local_save_filename_full = os.path.join(local_save_dir,local_save_filename)
            file.save(local_save_filename_full)
            print(f"Saving -- \t {local_save_filename}") #DEBUG

        #once all the files have been saved upload the task to the image queue
        image_task = {
                "input":folder_uuid,                        #The input is the folder containting the image files
                "output":folder_uuid,                       #the output is the pdf file name that will be futher processed...
                "isImage":True,                             #this means that the task is and image_processing one ..
                "status":FileStatus.uploaded.value,
                "numOfImages":count
            }

        #upload the task
        mongo.db.queue.insert_one(image_task)
        print("Task uploaded to DB ",image_task) #DEBUG

        #return the download URL

        download_url = url_for('main.download_pdf',uuid=folder_uuid)
        print("Returned Download UUID %s ",download_url)  #DEBUG
        return Response(json_resp("File Uploaded!",0,download_url))


