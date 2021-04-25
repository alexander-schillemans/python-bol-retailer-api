
#==============[HELPER FUNCTIONS]=================#

def getIndexWithValue(list, attribute, value):

    for index, obj in enumerate(list):
        if hasattr(obj, attribute):
            if getattr(obj, attribute) == value:
                return index
                break
    
    return None

def getObjectWithValue(list, attribute, value):

    for index, obj in enumerate(list):
        if hasattr(obj, attribute):
            if getattr(obj, attribute) == value:
                return obj
                break
    
    return None


#==============[BASE MODELS]=================#

class BaseModel:

    def parse(self, json):
        for key, value in json.items():
            try:
                attr = getattr(self, key)
                setattr(self, key, value)
            except AttributeError:
                continue
        
        return self
    
    def parseError(self, json):

        from .errors import Error
        
        self.hasError = True
        self.error = Error().parse(json)

        return self


class ObjectListModel(BaseModel):

    def __init__(self, list=[]):

        self.list = list

    def addToList(self, item):
        self.list.append(item)
        return self.list
    
    def removeFromList(self, item):
        self.list.remove(item)
        return self.list

    def getItemIndex(self, attribute, value):
        index = getIndexWithValue(self.list, attribute, value)
        return index
    
    def getItemObject(self, attribute, value):
        object = getObjectWithValue(self.list, attribute, value)
        return object