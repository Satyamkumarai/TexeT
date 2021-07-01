import uuid
from texet.main.constants import FileStatus
from bson.objectid import  ObjectId
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    Response,
    json)
from texet.extensions import mongo                  #The mongo client!
from .ocr import allowed_file ,do_ocrmypdf

bp = Blueprint('main',__name__)

@bp.route('/',methods = ['GET'])
def root():
    return render_template("index.html",title="TexeT")
    

@bp.route('/uploadpdf',methods=['GET'])
def uploadpdf():
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
    download_url = url_for('main.download_pdf',uuid=unique_filename)
    return download_url
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
            
            url  = add_file_to_db(file)   # set the status to upload
            return Response(json_resp("File Uploaded!",0,url))
        return Response(json_resp("Some other problem",1), 400, mimetype='application/json')


@bp.route("/pdf/download/<uuid>" ,methods=['GET'])
def download_pdf(uuid):
    work_doc = mongo.db.queue.find_one({"input":uuid})
    if work_doc:
        status = work_doc.get('status')
        if status == FileStatus.uploaded.value:
            return "Server Busy wait till your file gets processed !"
        else :
            return status
    return Response(json_resp("File Not Found!",1),404,mimetype="application/json")
    pass