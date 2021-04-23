from .base import ObjectListModel, BaseModel

class ProcessStatus(ObjectListModel):

    STATUS_PENDING = "PENDING"
    STATUS_SUCCESS = "SUCCESS"
    STATUS_FAILURE = "FAILURE"
    STATUS_TIMEOUT = "TIMEOUT"

    def __init__(self, 
        processStatusId=None,
        entityId=None,
        eventType=None,
        description=None,
        status=None,
        errorMessage=None,
        createTimestamp=None,
    ):

        super(ProcessStatus, self).__init__(list=[])

        self.processStatusId = processStatusId
        self.entityId = entityId
        self.eventType = eventType
        self.description = description
        self.status = status
        self.errorMessage = errorMessage
        self.createTimestamp = createTimestamp

    @property
    def links(self):
        return self.list
    
    def parse(self, json):
        super(ProcessStatus, self).parse(json)
        
        if 'links' in json:
            for link in json['links']:

                link = ProcessLink().parse(link)
                self.addToList(link)
        
        return self


class ProcessLink(BaseModel):

    def __init__(self,
        rel=None,
        href=None,
        method=None
    ):

        self.rel = rel
        self.href = href
        self.method = method