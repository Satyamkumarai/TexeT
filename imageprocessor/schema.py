from settings import DOWNLOAD_FOLDER,PDF_UPLOAD_FOLDER,IMAGE_UPLOAD_FOLDER
from datetime import datetime
from bson import ObjectId
import uuid
class Task:
    """
    This class contains the attributes necessary for a  task
    """
    def __init__(self,image:bool)->None:
        self._id = ObjectId()                       #create a custom Object Id
        self.startTime = None                       
        self.endTime = None
        self.createdOn = datetime.utcnow()          # set the created Date 
        self.image = image                          # set the type of doc (image or pdf)
        self.error = False
        self.taskData = TaskData(self)
    def to_dict(self)->dict:
        """returns a dictonary """
        d  =  vars(self)
        d['taskData']= ObjectId(self.taskData._id)
        return d
    def __repr__(self):
        return repr(self._id)
    @classmethod
    def pdf_task_from_image_task_dict(cls,old_image_task:dict,old_image_task_data:dict):
        new_task = Task(False)  #new pdf task
        new_task_data = new_task.taskData

        #copy in the old output to new input and uuid
        new_task_data.input = old_image_task_data.get('output',"")
        new_task_data.uuid = old_image_task_data.get('uuid',"")
        return new_task
        




class TaskData:
    """
    This class contains the file name and path for the task
        By default Upload file = UPLOAD_FOLDER/<uuid>.<ext>
        By default Download file = DOWNLOAD_FOLDER/<uuid>-download.<ext>
    """
    def __init__(self,task:Task):
        #create a custom Object Id 
        self._id = ObjectId()
        #link to original task
        self.task = ObjectId(task._id)
        # type of storage/ task
        self.image = task.image
        # Create a custom uuid 
        self.uuid = str(uuid.uuid4())
        #This delete the taskdata 
        self.deleted = None
        #set input and output depending on the type of doc
        if self.image :
            self.input = IMAGE_UPLOAD_FOLDER
            self.output = PDF_UPLOAD_FOLDER
        else:
            self.input = PDF_UPLOAD_FOLDER
            self.output = DOWNLOAD_FOLDER
    def to_dict(self)->dict:
        """returns a dictionary"""
        return vars(self)
    def __repr__(self):
        return repr(self._id)
    def image_data_to_pdf_data(self,image_data):
        pdf_data = image_data.copy()
        pdf_data['_id']=ObjectId()
        pdf_data['image']= False
        pdf_data['input'] = image_data['output']
        pdf_data['output'] = DOWNLOAD_FOLDER
        pdf_data['deleted'] = None
        return pdf_data
        # It still points to the old task and has the old uuid 
        # only the paths are changed.. a
        # and _id so that the new data is a fresh one ( doesnot conflict with old one while inserting )
        