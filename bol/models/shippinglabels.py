from .base import ObjectListModel, BaseModel

from .transports import Transport

class ShippingLabel(BaseModel):

    def __init__(self,
        transport=None,
        labelBytes=None
    ):

        self.transport = transport if transport else Transport()
        self.labelBytes = labelBytes

        self.hasError = False
        self.error = None
    
    def parse(self, headers, content):
        if 'X-Track-And-Trace-Code' in headers:
            self.transport.trackAndTrace = headers['X-Track-And-Trace-Code']
        
        if 'X-Transporter-Code' in headers:
            self.transport.transporterCode = headers['X-Transporter-Code']
        
        self.labelBytes = content

        return self

class DeliveryOptionList(ObjectListModel):

    def __init__(self):
        super(DeliveryOptionList, self).__init__(list=[])

        self.hasError = False
        self.error = None

    @property
    def options(self):
        return self.list

    def parse(self, json):
        if 'deliveryOptions' in json:
            for deliveryOption in json['deliveryOptions']:
                deliveryOptionObj = DeliveryOption().parse(deliveryOption)
                self.addToList(deliveryOptionObj)
        
        return self

class DeliveryOption(BaseModel):

    LABELTYPE_PARCEL = "PARCEL"
    LABELTYPE_MAILBOX = "MAILBOX"
    LABELTYPE_MAILBOX_LIGHT = "MAILBOX_LIGHT"

    def __init__(self,
        shippingLabelOfferId=None,
        validUntilDate=None,
        transporterCode=None,
        labelType=None,
        labelPrice=None,
        packageRestrictions=None,
        handoverDetails=None,
    ):

        self.shippingLabelOfferId = shippingLabelOfferId
        self.validUntilDate = validUntilDate
        self.transporterCode = transporterCode
        self.labelType = labelType
        self.labelPrice = labelPrice if labelPrice else LabelPrice()
        self.packageRestrictions = packageRestrictions if packageRestrictions else PackageRestrictions()
        self.handoverDetails = handoverDetails if handoverDetails else HandoverDetails()

        self.hasError = False
        self.error = None
    
    def parse(self, json):
        super(DeliveryOption, self).parse(json)

        if 'labelPrice' in json:
            self.labelPrice = LabelPrice().parse(json['labelPrice'])

        if 'packageRestrictions' in json:
            self.packageRestrictions = PackageRestrictions().parse(json['packageRestrictions'])
        
        if 'handoverDetails' in json:
            self.handoverDetails = HandoverDetails().parse(json['handoverDetails'])

        return self


class LabelPrice(BaseModel):

    def __init__(self,
        totalPrice=None
    ):

        self.totalPrice = totalPrice

        self.hasError = False
        self.error = None


class PackageRestrictions(BaseModel):

    def __init__(self,
        maxWeight=None,
        maxDimensions=None
    ):
        
        self.maxWeight = maxWeight
        self.maxDimensions = maxDimensions

        self.hasError = False
        self.error = None

class HandoverDetails(BaseModel):

    COLLECTIONMETHOD_DROP_OFF = "DROP_OFF"
    COLLECTIONMETHOD_PICK_UP = "PICK_UP"

    def __init__(self,
        meetsCustomerExpectation=None,
        latestHandoverDateTime=None,
        collectionMethod=None
    ):

        self.meetsCustomerExpectation = meetsCustomerExpectation
        self.latestHandoverDateTime = latestHandoverDateTime
        self.collectionMethod = collectionMethod

        self.hasError = False
        self.error = None