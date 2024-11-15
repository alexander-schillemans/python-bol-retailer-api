# python-bol-retailer-api
Wrapper for the bol.com Retailer API (v10)


## Breaking changes

v1.0.0 has breaking changes compared to v0.5.5
- When shipping an order or item using ```api.orders.shipItem``` or ```api.orders.ship```, shipmentReference is **required** and has to be passed as the second argument to the function.


    ```
        api.orders.shipItem(item, shipmentReference, transporterCode=api.transporters.GLS, trackAndTrace='XXXXXX')
        api.orders.ship(order, shipmentReference, transporterCode=api.transporters.UPS, trackAndTrace='XXXXXX')
    ```

## Install
This package is published on PyPi: https://pypi.org/project/python-bol-retailer-api/

Install with pip

    pip install python-bol-retailer-api
    
    
## Usage

Usage at this point is minimal. I will extend this package as I go and as I need.

Current usage is limited to Orders, Processes and ShippingLabels.

### Create connection
You will need a Client ID and Client Secret generated by Bol. Generate these here: https://partner.bol.com/sdd/settings.html#!/services/api

Create a new API connection

    from bol.api import BolAPI
    api = BolAPI(clientId, clientSecret)

Access token is automatically stored for later use. In the event that an access token is expired, a new access token will be requested and the initial request will be resend. This should ensure that the connection is never cut off.

The API keeps in account the rate limits that bol.com apply. In the event that the rate limit is almost exhausted within a timeframe, the API will stall until a new timeframe with new rate limits is available.

### Orders

#### Get all orders

By default all orders will be returned

    orderlist = api.orders.list()

You can specify the method and status yourself. Standard method is FBR and standard status is ALL.

    orderlist = api.orders.list(method='FBB', status='OPEN')

This will return an OrderList object.
You can loop over the orders like so:

    for order in orderlist.orders:
        print(order.orderId)
 
 Each order contains a list of OrderItem objects:
 
     for item in order.orderItems:
          print(item.orderItemId)
          
#### Get specific order

To get more info about an order, you can get the specific details of an order by its ID.

    order = api.orders.get(id)

This will return an Order object.
          
#### Ship an order

There are two ways to ship an order: you either ship an item of the order, or you ship the whole order at once.
When shipping an item, an OrderItem object is expected. When shipping an order, an Order object is expected.
shipmentReference is required as of v7.
Optionally you can add shippingLabelId, transporterCode and trackAndTrace. Consult the Bol documentation to know what is expected.

There is a list of transportercodes that you can use.

    api.orders.shipItem(item, shipmentReference, transporterCode=api.transporters.GLS, trackAndTrace='XXXXXX')
    api.orders.ship(order, shipmentReference, transporterCode=api.transporters.UPS, trackAndTrace='XXXXXX')
   
#### Cancel an order

There are two ways to cancel an order: you either cancel an item of the order, or you cancel the whole order at once.
when cancelling an item, an OrderItem object is expected. When cancelling an order, an Order object is expected.
A cancellation expects a reason for the cancellation. There is a list of reasons that you can use.

    api.orders.cancelItem(item, reason=api.reasons.OUT_OF_STOCK)
    api.orders.cancel(order, reason=api.reasons.NOT_AVAIL_IN_TIME)
    
### Processes

You can retrieve the status and additional information of a process by its ID.

    proc = api.processes.get(id)

    print(proc.processStatusId)
    print(proc.entityId)
    ...

### ShippingLabels

You can request a shipping label for an order. First, retrieve all the available options for the order. Choose an option and create a shipping label from it.

    order = api.orders.get(id)

    # 1: Retrieve all options
    shippingOptions = api.shippingLabels.listOptions(order)

    for option in shippingOptions.options:
        print(option.shippingLabelOfferId)
        ...

    # 2: Choose an option and create a label for it by using its shippingLabelOfferId
    # This return a process, because the API is asynchronous
    label = api.shippingLabels.create(order, option.shippingLabelOfferId)
    print(label.processStatusId)

Once the label has been created, you can get the label PDF by using its ID. Before retrieving the label PDF, you need to be sure that the process that is responsible for this has finished and the status has been set to 'SUCCESS'.

    process = api.process.get(label.processStatusId)
    if process.status == 'SUCCESS':
        shippingLabelId = process.entityId
        shippingLabel = api.shippingLabels.get(shippingLabelId)

        fs = FileSystemStorage()
        with TemporaryFile() as f:
            f.write(shippingLabel.labelBytes)
            resultFile = File(f)
            file = fs.save('my_shipping_label.pdf', resultFile)