from .base import APIEndpoint

from bol.models.shippinglabels import DeliveryOptionList, DeliveryOption, ShippingLabel
from bol.models.processes import ProcessStatus
from bol.models.transports import Transport

class ShippingLabelMethods(APIEndpoint):

    def __init__(self, api):
        super(ShippingLabelMethods, self).__init__(api, "shipping-labels")

    def listOptions(self, order):

        if self.api.demo:
            data = { 'orderItems' : [{'orderItemId' : '2095052647'}]}
        else:
            data = { 'orderItems' : []}
            for item in order.orderItems:
                data['orderItems'].append({'orderItemId' : item.orderItemId })

        url = '{endpoint}/delivery-options'.format(endpoint=self.endpoint)

        status, headers, respJson = self.api.post(url, data)
        if status == 400: return DeliveryOptionList().parseError(respJson)

        return DeliveryOptionList().parse(respJson)

    def get(self, id):

        if self.api.demo: id = 'c628ba4f-f31a-4fac-a6a0-062326d0dbbd'

        url = '{endpoint}/{id}'.format(endpoint=self.endpoint, id=id)
        data = None

        labelHeaders = {
            'Accept' : 'application/vnd.retailer.v5+pdf',
            'Content-Type' : '',
        }

        status, headers, respContent = self.api.get(url, data, labelHeaders)
        if status == 400: return ShippingLabel().parseError(respContent)

        return ShippingLabel().parse(headers, respContent)
    
    def create(self, order, shippingLabelOfferId):

        if self.api.demo:
            data = { 'orderItems' : [{'orderItemId' : '2095052647'}], 'shippingLabelOfferId' : "8f956bfc-fabe-45b4-b0e1-1b52a0896b74"}
        else:
            data = { 'orderItems' : [], 'shippingLabelOfferId' : shippingLabelOfferId}

            for item in order.orderItems:
                data['orderItems'].append({'orderItemId' : item.orderItemId })

        url = self.endpoint

        status, headers, respJson = self.api.post(url, data)
        if status == 400: return ProcessStatus().parseError(respJson)
        
        return ProcessStatus().parse(respJson)