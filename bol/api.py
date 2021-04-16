import base64
import requests
import json
import time

import config as config
from cache import CacheHandler
from models import OrderList, Order

class APIEndpoint:

    def __init__(self, api, endpoint):

        self.api = api
        self.endpoint = endpoint
    

class OrderMethods(APIEndpoint):

    def __init__(self, api):
        super(OrderMethods, self).__init__(api, "orders")

    def list(self, page=1, method='FBR', status='ALL'):

        data = { 'page' : page, 'method' : method, 'status' : status }
        url = self.endpoint

        status, respJson = self.api.get(url, data)
        return OrderList().parse(respJson)

    def get(self, id):

        url = '{endpoint}/{id}'.format(endpoint=self.endpoint, id=id)
        data = None

        status, respJson = self.api.get(url, data)
        return Order().parse(respJson)

class BolAPI:

    def __init__(self, clientId, clientSecret, demo=False):

        self.clientId = clientId
        self.clientSecret = clientSecret
        self.headers = {
            'Accept' : 'application/vnd.retailer.v5+json',
        }

        self.baseUrl = config.DEMO_URL if demo else config.BASE_URL
        self.cacheHandler = CacheHandler()

        self.rateLimitRemaining = None
        self.rateLimitReset = None

        self.orders = OrderMethods(self)
    
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
        
        if 'X-RateLimit-Reset' in headers:
            self.rateLimitReset = int(headers['X-RateLimit-Reset'])


        # If we only have one request or less remaining, delay until the limit is reset
        if self.rateLimitRemaining <= 1:
            currentMil = time.time() * 1000
            waitingMil = self.rateLimitReset - currentMil

            time.sleep(waitingMil/1000)

    def doRequest(self, method, url, data=None, headers=None):

        if headers: headers.update(self.headers)
        else: headers = self.headers

        reqUrl = '{base}/{url}'.format(base=self.baseUrl, url=url)

        if method == 'GET':
            response = requests.get(reqUrl, params=data, headers=headers)
        elif method == 'POST':
            response = requests.post(reqUrl, data=json.dumps(data), headers=headers)
        
        return response


    def request(self, method, url, data=None, headers=None):
        
        # Check the headers for appropriate tokens before we make a request
        self.checkHeaderTokens()

        # Make the request
        response = self.doRequest(method, url, data, headers)
        
        # Check if request has been carried out
        # If request has been blocked due to token expiration, get a new one and redo the request
        if response.status_code == 401:
            self.acquireAccessToken()

            response = self.doRequest(method, url, data, headers)
        
        # Check the rate remaining, delay if necessary
        self.checkRateLimits(response)
        
        return response.status_code, response.json()
    
    def get(self, url, data=None, headers=None):
        status, response = self.request('GET', url, data, headers)
        return status, response
    
    def post(self, url, data=None, headers=None):
        status, response = self.request('POST', url, data, headers)
        return status, response