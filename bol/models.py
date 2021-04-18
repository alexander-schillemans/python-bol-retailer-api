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


class BaseModel:

    def parse(self, json):
        for key, value in json.items():
            try:
                attr = getattr(self, key)
                setattr(self, key, value)
            except AttributeError:
                continue
        
        return self

class ObjectListModel:

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


class OrderList(ObjectListModel):
    
    @property
    def orders(self):
        return self.list

    def parse(self, json):
        if 'orders' in json:
            for order in json['orders']:
                orderObj = Order().parse(order)
                self.addToList(orderObj)
        
        return self


class Order(ObjectListModel):

    def __init__(self, 
        orderId=None, 
        billingDetails=None,
        shipmentDetails=None,
    ):
        super(Order, self).__init__(list=[])

        self.orderId = orderId
        self.billingDetails = billingDetails if billingDetails else CustomerDetails()
        self.shipmentDetails = shipmentDetails if shipmentDetails else CustomerDetails()

    @property
    def orderItems(self):
        return self.list

    def parse(self, json):
        
        self.orderId = json['orderId'] if 'orderId' in json else None

        if 'orderItems' in json:
            for item in json['orderItems']:

                # Check if item already exists in list, if so, update
                # Else, create new one and add
                existingItem = self.getItemIndex('orderItemId', item['orderItemId'])

                if existingItem:
                    self.orderItems[index] = self.orderItems[index].parse(item)
                else:
                    orderItem = OrderItem().parse(item)
                    self.addToList(orderItem)

        if 'billingDetails' in json:
            self.billingDetails.parse(json['billingDetails'])

        if 'shipmentDetails' in json:
            self.shipmentDetails.parse(json['shipmentDetails'])

        return self

class OrderItem(BaseModel):

    def __init__(self, 
        orderItemId=None, 
        ean=None, 
        quantity=None, 
        quantityShipped=None, 
        quantityCancelled=None,
        cancellationRequest=None,
        title=None, 
        unitPrice=None, 
        comission=None
    ):

        self.orderItemId = orderItemId
        self.cancellationRequest = cancellationRequest
        self.ean = ean
        self.title = title
        self.quantity = quantity
        self.quantityShipped = quantityShipped
        self.quantityCancelled = quantityCancelled
        self.unitPrice = unitPrice
        self.comission = comission


class CustomerDetails(BaseModel):

    def __init__(self, 
        firstName=None, 
        surname=None, 
        streetName=None, 
        houseNumber=None, 
        houseNumberExtension=None, 
        extraAdressInformation=None, 
        zipCode=None,
        city=None,
        countryCode=None,
        email=None,
        company=None,
        vatNumber=None,
        kvkNumber=None,
        orderReference=None
    ):

        self.firstName = firstName
        self.surname = surname
        self.streetName = streetName
        self.houseNumber = houseNumber
        self.houseNumberExtension = houseNumberExtension
        self.extraAdressInformation = extraAdressInformation
        self.zipCode = zipCode
        self.city = city
        self.countryCode = countryCode
        self.email = email
        self.company = company
        self.vatNumber = vatNumber
        self.kvkNumber = kvkNumber
        self.orderReference = orderReference