from texet.settings import DOWNLOAD_FOLDER,PDF_UPLOAD_FOLDER,IMAGE_UPLOAD_FOLDER
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