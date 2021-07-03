import uuid
import os
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
from .ocr import allowed_file ,do_ocrmypdf
from werkzeug.utils import secure_filename
from flask import current_app

bp = Blueprint('main',__name__)

@bp.route('/',methods = ['GET'])
def root():
    return render_template("index.html",title="TexeT")
    

@bp.route('/uploadpdf',methods=['GET'])
def uploadpdf( ):
    return render_template("upload/upload.html")

@bp.route('/scan',methods=['GET'])
def scan():
    return render_template("scan.html",title="TeXeT")

def add_file_to_db(file):
    print(file.filename)

    unique_filename = str(uuid.uuid4())
    upload_filename = unique_filename
    download_filename = unique_filename+"-download"
    task = {
        "input":unique_filename,
        "output":download_filename,
        "isImage":False,
        "status":FileStatus.uploaded.value,
        "origfilename":file.filename
    }
    mongo.db.queue.insert_one(task)
    return unique_filename
@bp.route('/test')
def testdb():
    docs = mongo.db.queue.count()
    return Response(f"count={docs}",200)
def json_resp(msg,error=0,url=""):
    """add the message and return jsonobj as  string"""
    payload = {"message":msg,
        "error":error,
    }

    if url:
        payload["downloadUrl"]=url
    return json.dumps(payload)
from subprocess import PIPE, run
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
            file_uuid  = add_file_to_db(file)   # set the status to upload
            #save the file locally 
            file.save(os.path.join(current_app.instance_path, PDF_UPLOAD_FOLDER, secure_filename(file_uuid+".pdf")))
            run(["cp",os.path.join(current_app.instance_path, PDF_UPLOAD_FOLDER, secure_filename(file_uuid+".pdf")),os.path.join(current_app.instance_path, DOWNLOAD_FOLDER, secure_filename(file_uuid+"-download.pdf"))])            
            download_url = url_for('main.download_pdf',uuid=file_uuid)
            return Response(json_resp("File Uploaded!",0,download_url))
        return Response(json_resp("Some other problem",1), 400, mimetype='application/json')


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
    pass