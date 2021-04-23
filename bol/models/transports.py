from .base import BaseModel

class Transport(BaseModel):

    def __init__(self,
        transporterCode=None,
        trackAndTrace=None
    ):

        self.transporterCode = transporterCode
        self.trackAndTrace = trackAndTrace