from texet.settings import DOWNLOAD_FOLDER,PDF_UPLOAD_FOLDER,IMAGE_UPLOAD_FOLDER
from datetime import datetime

class Task:
    """A task Class to make it easier to upload and get document 
        By default Upload file = UPLOAD_FOLDER/<uuid>.<ext>
        By default Download file = DOWNLOAD_FOLDER/<uuid>-download.<ext>
    """


    def __init__(self,uuid:str,image:bool)->None:
        self.startTime = None
        self.endTime = None
        self.createdOn = datetime.utcnow()
        self.image = image
        self.uuid = uuid
        self.error = False
        if image :
            self.input = IMAGE_UPLOAD_FOLDER
            self.output = PDF_UPLOAD_FOLDER
        else:
            self.input = PDF_UPLOAD_FOLDER
            self.output = DOWNLOAD_FOLDER
    def to_dict(self)->dict:
        """returns a dictonary """
        return vars(self)


