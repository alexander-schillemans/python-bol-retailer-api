from .base import ObjectListModel, BaseModel

class Error(ObjectListModel):

    def __init__(self,
        type=None,
        title=None,
        status=None,
        detail=None,
        host=None,
        instance=None,
    ):

        super(Error, self).__init__(list=[])

        self.errors = True
        self.type = type
        self.title = title
        self.status = status
        self.detail = detail
        self.host = host
        self.instance = instance
    
    @property
    def violations(self):
        return self.list
    
    def parse(self, json):
        
        super(Error, self).parse(json)

        if 'violations' in json:
            for violation in json['violations']:
                violation = Violation().parse(violation)
                self.addToList(violation)

        return self

class Violation(BaseModel):

    def __init__(self,
        name=None,
        reason=None
    ):
        self.errors = True
        self.name = name
        self.reason = reason