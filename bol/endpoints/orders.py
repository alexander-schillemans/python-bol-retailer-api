from .base import APIEndpoint

from bol.models.orders import OrderList, Order
from bol.models.processes import ProcessStatus

class OrderMethods(APIEndpoint):

    def __init__(self, api):
        super(OrderMethods, self).__init__(api, "orders")

    def list(self, page=1, method='FBR', status='ALL'):

        data = { 'page' : page, 'method' : method, 'status' : status }
        url = self.endpoint

        status, headers, respJson = self.api.get(url, data)
        print(respJson)
        if status == 400: return OrderList().parseError(respJson)

        return OrderList().parse(respJson)

    def get(self, id):

        url = '{endpoint}/{id}'.format(endpoint=self.endpoint, id=id)
        data = None

        status, headers, respJson = self.api.get(url, data)
        if status == 404: return Order().parseError(respJson)

        return Order().parse(respJson)
    
    def cancelItem(self, item, reason):
        data = { 'orderItems' : [{ 'orderItemId' : item.orderItemId, 'reasonCode' : reason }]}

        url = '{endpoint}/cancellation'.format(endpoint=self.endpoint)

        status, headers, respJson = self.api.put(url, data)
        if status == 400: return ProcessStatus().parseError(respJson)
        
        return ProcessStatus().parse(respJson)
    
    def cancel(self, order, reason):

        processStatuses = []

        for item in order.orderItems:
            processStatus = self.cancelItem(item, reason)
            processStatuses.append(processStatus)

        return processStatuses
    
    def shipItem(self, item, shipmentReference=None, shippingLabelId=None, transporterCode=None, trackAndTrace=None):
        data = { 'orderItems' : [{ 'orderItemId' : item.orderItemId }] }

        if shipmentReference: data['shipmentReference'] = shipmentReference
        if shippingLabelId: data['shippingLabelId'] = shippingLabelId
        if transporterCode:
            data['transport'] = { 'transporterCode' : transporterCode }
            if trackAndTrace: data['transport']['trackAndTrace'] = trackAndTrace

        url = '{endpoint}/shipment'.format(endpoint=self.endpoint)
        
        status, headers, respJson = self.api.put(url, data)
        if status == 400: return ProcessStatus().parseError(respJson)

        return ProcessStatus().parse(respJson)

    def ship(self, order, shipmentReference=None, shippingLabelId=None, transporterCode=None, trackAndTrace=None):

        processStatuses = []

        for item in order.orderItems:
            processStatus = self.shipItem(item, shipmentReference, shippingLabelId, transporterCode, trackAndTrace)
            processStatuses.append(processStatus)

        return processStatuses