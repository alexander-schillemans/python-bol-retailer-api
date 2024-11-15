import base64
import requests
import json
import time

from . import config
from .cachehandler import CacheHandler

from .constants.reasons import *
from .constants.transporters import *

from .endpoints.orders import OrderMethods
from .endpoints.shippinglabels import ShippingLabelMethods
from .endpoints.processes import ProcessMethods


class BolAPI:

    def __init__(self, clientId, clientSecret, demo=False):

        self.clientId = clientId
        self.clientSecret = clientSecret
        self.demo = demo
        self.headers = {
            'Accept' : 'application/vnd.retailer.v10+json',
            'Content-Type' : 'application/vnd.retailer.v10+json',
        }


        self.baseUrl = config.DEMO_URL if demo else config.BASE_URL
        self.sharedUrl = config.SHARED_DEMO_URL if demo else config.SHARED_URL
        self.cacheHandler = CacheHandler()

        self.rateLimitRemaining = None
        self.rateLimitReset = None

        self.orders = OrderMethods(self)
        self.shippingLabels = ShippingLabelMethods(self)
        self.processes = ProcessMethods(self)

        self.reasons = Reasons()
        self.transporters = Transporters()
    
    def setTokenHeader(self, token):
        bearerStr = 'Bearer {token}'.format(token=token)
        self.headers.update({'Authorization' : bearerStr})

    def checkHeaderTokens(self):

        # If no authorization header is found, we need to include the token
        if 'Authorization' not in self.headers:
            
            # Check if we have a token stored in cache, if not, acquire one
            # If we do, set it in the header
            cachedAccessToken = self.cacheHandler.getCache(self.clientId)
            if cachedAccessToken is None:
                self.acquireAccessToken()
            else:
                self.setTokenHeader(cachedAccessToken)

    def acquireAccessToken(self):

        credentialsString = '{clientId}:{clientSecret}'.format(clientId=self.clientId, clientSecret=self.clientSecret)
        encodedBytes = base64.b64encode(credentialsString.encode('utf-8'))
        encodedString = str(encodedBytes, 'utf-8')

        credentialsHeader = {
            'Accept' : 'application/json',
            'Authorization' : 'Basic {encodedString}'.format(encodedString=encodedString)
        }

        req = requests.post(config.AUTH_URL, data=None, headers=credentialsHeader)
      
        status = req.status_code
        response = req.json()

        if status == 200:
            accessToken = response['access_token']
            self.cacheHandler.setCache(self.clientId, accessToken)
            self.setTokenHeader(accessToken)

            return accessToken

    def checkRateLimits(self, response):
        headers = response.headers

        if 'X-RateLimit-Remaining' in headers:
            self.rateLimitRemaining = int(headers['X-RateLimit-Remaining'])
        else:
            self.rateLimitRemaining = 2
        
        if 'X-RateLimit-Reset' in headers:
            self.rateLimitReset = int(headers['X-RateLimit-Reset'])
        
        # If we only have one request or less remaining, delay until the limit is reset
        if self.rateLimitRemaining <= 1:
            currentMil = time.time() * 1000
            waitingMil = self.rateLimitReset - currentMil
            if waitingMil <= 0: waitingMil = 1000

            time.sleep(waitingMil/1000)

    def doRequest(self, method, url, data=None, headers=None, overwriteURL=False):
        
        if headers:
            mergedHeaders = self.headers.copy()
            mergedHeaders.update(headers)
            headers = mergedHeaders
        else: headers = self.headers

        if overwriteURL:
            reqUrl = url
        else:
            reqUrl = '{base}/{url}'.format(base=self.baseUrl, url=url)

        if method == 'GET':
            response = requests.get(reqUrl, params=data, headers=headers)
        elif method == 'POST':
            response = requests.post(reqUrl, data=json.dumps(data), headers=headers)
        elif method == 'PUT':
            response = requests.put(reqUrl, data=json.dumps(data), headers=headers)

        return response


    def request(self, method, url, data=None, headers=None, overwriteURL=False):
        
        # Check the headers for appropriate tokens before we make a request
        self.checkHeaderTokens()

        # Make the request
        response = self.doRequest(method, url, data, headers, overwriteURL)
        
        # Check if request has been carried out
        # If request has been blocked due to token expiration, get a new one and redo the request
        if response.status_code == 401:
            self.acquireAccessToken()

            response = self.doRequest(method, url, data, headers)

        # Check the rate remaining, delay if necessary
        self.checkRateLimits(response)

        if 'json' in response.headers['Content-Type']:
            respContent = response.json()
        elif 'pdf' in response.headers['Content-Type']:
            respContent = response.content
        
        return response.status_code, response.headers, respContent
    
    def get(self, url, data=None, headers=None, overwriteURL=False):
        status, headers, response = self.request('GET', url, data, headers, overwriteURL)
        return status, headers, response
    
    def post(self, url, data=None, headers=None, overwriteURL=False):
        status, headers, response = self.request('POST', url, data, headers, overwriteURL)
        return status, headers, response
    
    def put(self, url, data=None, headers=None, overwriteURL=False):
        status, headers, response = self.request('PUT', url, data, headers, overwriteURL)
        return status, headers, response