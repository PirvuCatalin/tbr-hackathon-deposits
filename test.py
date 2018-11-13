import requests
import json
from classes import *
import qrcode
from qrGenerator import *

qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

initial_url = 'https://thebestrunsap2018z3d3pet6df.hana.ondemand.com\
/ro/sap/hackathon/team08/service.xsodata/'

Activity_url = initial_url + "Activity?$format=json"
Article_url = initial_url + "Article?$format=json"

TransportationNetwork_url = initial_url + "TransportationNetwork?$format=json"
Stock_url = initial_url + "Stock?$format=json"
StockRule_url = initial_url + "StockRule?$format=json"
StorageArea_url = initial_url + "StorageArea?$format=json"

url = 'https://thebestrunsap2018z3d3pet6df.hana.ondemand.com\
/ro/sap/hackathon/team08/service.xsodata/Article?$format=json'
payload = {'TIMESTAMP': '/Date(1474823911255)/', 'VALUE': '100000'}
headers = {"Content-type": 'application/json;charset=utf-8'}
auth = 'TEAM08_USER', '08TheBestRunSap@2018!'

Activity_json = requests.get(Activity_url, data=json.dumps(payload), headers=headers, auth=auth)
Article_json = requests.get(Article_url, data=json.dumps(payload), headers=headers, auth=auth)
TransportationNetwork_json = requests.get(TransportationNetwork_url, data=json.dumps(payload), headers=headers, auth=auth)
Stock_json = requests.get(Stock_url, data=json.dumps(payload), headers=headers, auth=auth)
StockRule_json = requests.get(StockRule_url, data=json.dumps(payload), headers=headers, auth=auth)
StorageArea_json = requests.get(StorageArea_url, data=json.dumps(payload), headers=headers, auth=auth)

Activity_json = Activity_json.json()
Article_json = Article_json.json()
TransportationNetwork_json = TransportationNetwork_json.json()
Stock_json = Stock_json.json()
StockRule_json = StockRule_json.json()
StorageArea_json = StorageArea_json.json()

Articles_dict = {}
Transportation_dict = {}
Stock_dict = {}
StockRule_dict = {}
StorageArea_dict = {}

# Store the articles
for article in Article_json['d']['results']:
    code = article['Code']
    palletWeight = article['PalletWeight']
    palletQuantity = article['PalletQuantity']
    palletVolume = article['PalletVolume']
    singleUnitWeight = article['SingleUnitWeight']
    singleUnitVolume = article['SingleUnitVolume']
    Articles_dict[code] = Article(code, palletQuantity, singleUnitWeight, palletWeight, singleUnitVolume, palletVolume)

# Store the transport times
for transportation in TransportationNetwork_json['d']['results']:
    dict_key = transportation['DestinationAreaCode'] + ":" + transportation['SourceAreaCode']
    Transportation_dict[dict_key] = transportation['MoveTime']

# store the stock
for stock in Stock_json['d']['results']:
    stock_area_a = stock['StockAreaA']
    stock_area_b = stock['StockAreaB']
    stock_area_c = stock['StockAreaC']
    code = stock['ArticleCode']
    Stock_dict[code] = Stock(code, stock_area_a, stock_area_b, stock_area_c)

# store the stock rules
for stockRule in StockRule_json['d']['results']:
    maxCapacity = stockRule['MaxCapacity']
    code = stockRule['ArticleCode']
    storageAreaCode = stockRule['StorageAreaCode']
    maxQuantity = stockRule['MaxQuantity']
    minQuantity = stockRule['MinQuantity']
    StockRule_dict[code] = StockRule(code, storageAreaCode, minQuantity, maxQuantity, maxCapacity)

# store the areas
for area in StorageArea_json['d']['results']:
    code = area['Code']
    maxWeight = area['MaxWeight']
    maxVolume = area['MaxVolume']
    capacity = area['Capacity']
    my_area = area['Area']
    StorageArea_dict[code] = StorageArea(code, my_area, capacity, maxWeight, maxVolume)

#img = generateQrCode('A002', 0.002, 0.2)
#img.show()

numberOfItems = 1
sum = 0

Delivery_url = initial_url + "Delivery?$top=" + str(numberOfItems) + "&$skip=" + str(sum) + "&$format=json"

Delivery_json = requests.get(Delivery_url, data=json.dumps(payload), headers=headers, auth=auth)
Delivery_json = Delivery_json.json()

while True:

    command = input()

    if command == "get":
        delivery_time = 0
        time = Delivery_json['d']['results'][0]['Time']
        quantity = Delivery_json['d']['results'][0]['QuantitySingleUnits']
        code = Delivery_json['d']['results'][0]['ArticleCode']
        type = Delivery_json['d']['results'][0]['Type']

        single = quantity % Articles_dict[code].pallet_quantity
        pallets = int(quantity / Articles_dict[code].pallet_quantity) * Articles_dict[code].pallet_quantity

        if type == 'OUT':
            print("We have to deliver " + str(quantity) + " of " + code)
            print("Initial stocks are: ")
            print("In A: " + str(Stock_dict[code].stock_area_a))
            print("In B: " + str(Stock_dict[code].stock_area_b))
            print("In C: " + str(Stock_dict[code].stock_area_c))
            to_deliver = 0

            if single > Stock_dict[code].stock_area_a:
                if single > Stock_dict[code].stock_area_b:
                    if single > Stock_dict[code].stock_area_c:
                        delivery_time += 75 + 24 * 60
                        Stock_dict[code].stock_area_c -= single
                    else:
                        delivery_time += 75
                        Stock_dict[code].stock_area_c -= single
                else:
                    delivery_time += 15
                    Stock_dict[code].stock_area_b -= single
            else:
                Stock_dict[code].stock_area_a -= single
            if pallets > Stock_dict[code].stock_area_c and delivery_time < 76:
                delivery_time = 75 + 24 * 60
                Stock_dict[code].stock_area_c -= pallets
            else:
                Stock_dict[code].stock_area_c -= pallets

            print("Product delivered in " + str(delivery_time))
        else:
            print("We have to store " + str(quantity) + " of " + code)
            print("Initial stocks are: ")
            print("In A: " + str(Stock_dict[code].stock_area_a))
            print("In B: " + str(Stock_dict[code].stock_area_b))
            print("In C: " + str(Stock_dict[code].stock_area_c))


        sum += numberOfItems
        Delivery_url = initial_url + "Delivery?$top=" + str(numberOfItems) + "&$skip=" + str(sum) + "&$format=json"
        Delivery_json = requests.get(Delivery_url, data=json.dumps(payload), headers=headers, auth=auth)
        Delivery_json = Delivery_json.json()

    if command == "qr":
        for (key, element) in Articles_dict.items():
            print(element.code)
            img = generateQrCode(element.code, element.single_unit_weight, element.single_unit_volume)
            title = element.code + ".jpg"
            img.save(title)