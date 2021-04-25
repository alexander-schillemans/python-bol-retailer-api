from .base import ObjectListModel, BaseModel

from .transports import Transport

class OrderList(ObjectListModel):
    
    def __init__(self):
        super(OrderList, self).__init__(list=[])

        self.errors = False

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
        self.errors = False

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

class OrderShipment(ObjectListModel):

    def __init__(self,
        shipmentReference=None,
        shippingLabelId=None,
        transport=None
    ):

        super(OrderShipment, self).init__(list=[])

        self.shipmentReference = shipmentReference
        self.shippingLabelId= shippingLabelId
        self.transport = transport if transport else Transport()
        self.errors = False
    
    @property
    def orderItems(self):
        return self.list

class OrderItem(BaseModel):

    def __init__(self, 
        orderItemId=None,
        ean=None,
        title=None,
        quantity=None, 
        quantityShipped=None, 
        quantityCancelled=None,
        cancellationRequest=None,
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
        self.errors = False

    def parse(self, json):
        super(OrderItem, self).parse(json)

        if 'product' in json:
            self.ean = json['product']['ean']
            self.title = json['product']['title']
        
        return self

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
        self.errors = False