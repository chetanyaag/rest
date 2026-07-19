from email import message
import django
import requests
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import *
from .searializers import *
import subprocess
import pymongo
import requests
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.condition import Condition
from paapi5_python_sdk.models.get_items_request import GetItemsRequest
from paapi5_python_sdk.models.get_items_resource import GetItemsResource
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.rest import ApiException
from datetime import datetime as dt
from rest_framework.views import APIView
import json

from .messageMethod import *

con = pymongo.MongoClient("localhost", 27017)
db = con['NazAf']
col = db['product']
token_collection = db['token']



#############################################
#### Functions


def create_and_get_token(field, value):
    tkn = token_collection.find_one({field:value})
    format_data = "%d/%m/%y %H:%M:%S.%f"
    # check the token
    if tkn :
        # check if token is expired
        that_time = dt.strptime(tkn['tkn'], format_data)
        now_time = dt.now()
        delta_time = now_time - that_time
        if delta_time.days >1:
            # we are deleteing the oken we can also update the token
            token_collection.delete_one({field:value})
            now = dt.now()
            new_entry={}
            new_entry["user_name"] = tkn['user_name']
            new_entry["time"] = now.strftime(format_data)
            new_entry["tkn"] = now.strftime(format_data)
            token_collection.insert_one(new_entry)
            return new_entry['tkn']
        else:
            return tkn['tkn']
    else:
        if field != "user_name":
            return "nil"
        now = dt.now()
        new_entry={}
        new_entry["user_name"] = value
        new_entry["time"] = now.strftime(format_data)
        new_entry["tkn"] = now.strftime(format_data)
        token_collection.insert_one(new_entry)
        return new_entry['tkn']



def extract_the_asin(link):
    if "dp/" in link:
        array = link.split("dp/")
        asin = ""
        for a in array[1]:
            if a.isalnum():
                asin = asin +a
            else:
                break
        return asin  

    elif "/gp/product/" in link:
        array = link.split("/gp/product/")  
        asin = ""
        for a in array[1]:
            if a.isalnum():
                asin = asin +a
            else:
                break
        return asin 
    elif "field-asin=" in link:

        array = link.split("field-asin=")
        asin =""
        for a in array[1]:
            if a.isalnum():
                asin = asin +a
            else:
                break
        return asin         
    else:
        return link    
###############################################






# Create your views here.

@api_view(['GET'])
def home(request):
    link = request.GET.get('link')
    if link:
        with open('res.txt', 'w') as f:
            f.write(link)
    return Response({"message":"Invalid Link"})    


@api_view(['GET'])
def getProductData(request):
    data = request.GET.get('asin')

    pro = col.find_one({"product_id": str(data)})
    if pro is not None:
        pro.pop('_id')
        return Response({'status':200, 'data':pro})
    else:
        return Response({"status":404, 'data':""})


# This api take the asin and give download the data on database

@api_view(['POST'])
def addAProduct(request):

    asin = request.data['asin']
    try:
        if '.' in asin:
            res = requests.get(asin)
            asin = res.url

    except:
        print("thinking the process")

        # asin = 
    asin = extract_the_asin(asin)
    item_ids = [asin]

    # check whether asin is a link 
        # if link than extract the asin
            # if asin is not found return 403
    
# personal data do not share with any one
    access_key = ""
    secret_key = ""
    partner_tag = "bestdeal0013-21"
    host = "webservices.amazon.in"
    region = "eu-west-1"
    default_api = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )
#################################################
    get_items_resource = [
    GetItemsResource.IMAGES_PRIMARY_LARGE,
    GetItemsResource.ITEMINFO_CONTENTINFO,
    GetItemsResource.ITEMINFO_CLASSIFICATIONS,
    GetItemsResource.ITEMINFO_FEATURES,
    GetItemsResource.ITEMINFO_MANUFACTUREINFO,
    GetItemsResource.ITEMINFO_PRODUCTINFO,
    GetItemsResource.ITEMINFO_TECHNICALINFO,
    GetItemsResource.ITEMINFO_TITLE,
    GetItemsResource.OFFERS_LISTINGS_ISBUYBOXWINNER,
    GetItemsResource.OFFERS_LISTINGS_MERCHANTINFO,
    GetItemsResource.OFFERS_LISTINGS_PRICE,
    GetItemsResource.OFFERS_SUMMARIES_LOWESTPRICE,
    ]

    try:
        get_items_request = GetItemsRequest(
            partner_tag=partner_tag,
            partner_type=PartnerType.ASSOCIATES,
            marketplace="www.amazon.in",
            condition=Condition.NEW,
            item_ids=item_ids,
            resources=get_items_resource,
        )
    except ValueError as exception:
        print("Error in forming GetItemsRequest: ", exception)
        return Response({"message":exception})   
c
    try:
        response = default_api.get_items(get_items_request)

        return Response({"message":404})
#   product
    try:
        item = response.items_result.items[0]

        product_title = item.item_info.title.display_value

        product_image = item.images.primary.large.url

        product_url = item.detail_page_url

    except Exception as e:
        print(e)
        return Response({"message":404})    

    try:
        product_binding = item.item_info.classifications.binding.display_value
    except:
        product_binding = None

    try:
        product_group = item.item_info.classifications.product_group.display_value
    except:
        product_group = None

    try:
        product_features = item.item_info.features.display_values
    except:
        product_features = None

    try:
        product_height = item.item_info.product_info.item_dimensions.height.display_value
    except:
        product_height = None
    try:
        product_length = item.item_info.product_info.item_dimensions.length.display_value
    except:
        product_length = None
    try:    
        product_weight = item.item_info.product_info.item_dimensions.weight.display_value
    except:
        product_weight = None
    try:    
        product_width = item.item_info.product_info.item_dimensions.width.display_value
    except:
        product_width = None
    try:
        product_size = item.item_info.product_info.size.display_value
    except:
        product_size = None

    try:
        product_manufacture_id = item.item_info.manufacture_info.item_part_number.display_value
    except:
        product_manufacture_id = None

    try:    
        product_manufacture_model = item.item_info.manufacture_info.model.display_value
    except:
        product_manufacture_model = None
    try:
        product_manufacture_warranty = item.item_info.manufacture_info.warranty.display_value
    except:
        product_manufacture_warranty = None

    try:
        product_merchant_name = item.offers.listings[0].merchant_info.name
    except:
        product_merchant_name = None

    try:
        product_price = item.offers.listings[0].price.amount
    except:
        product_price = None
    try:    
        product_discount = item.offers.listings[0].price.savings.amount
    except:
        product_discount = None
    try:    
        product_discount_percentage = item.offers.listings[0].price.savings.percentage
    except:
        product_discount_percentage = None

    product = {}


    product["product_title"] = product_title
    product["product_url"] = product_url
    product["product_image"] = product_image
    product["product_binding"] = product_binding
    product["product_group"] = product_group
    product["product_features"] = product_features
    product["product_height"] = product_height
    product["product_weight"] = product_weight
    product["product_width"] = product_width
    product["product_length"] = product_length
    product["product_size"] = product_size
    product["product_manufacture_id"] = product_manufacture_id
    product["product_manufacture_model"] = product_manufacture_model
    product["product_manufacture_warranty"] = product_manufacture_warranty
    product["product_merchant_name"] = product_merchant_name
    product["product_price"] = product_price
    product["product_discount"] = product_discount
    product["product_discount_percentage"] = product_discount_percentage

    update_check = col.find_one({'product_id':asin})

    if update_check:
        col.update_one({'product_id':asin},{"$set":product})
    else:    
        product["product_id"] = asin
        col.insert_one(product)

    return Response({"message":200, "asin":asin})    






@api_view(['POST'])
def check_user(request):
    user_name = request.data['username']
    password = request.data['password']

    user = authenticate(username=user_name, password=password)
    if user is not None:

        tkn = create_and_get_token("user_name",user_name)

        return Response({"status":200, "message":tkn})
    else:
        return Response({"status":404, "message":""})    


@api_view(['POST'])
def check_tkn(request):
    tkn = request.data['tkn']
    tkn2 = create_and_get_token("tkn", tkn)

    if tkn ==tkn2:
        return Response({"status":200, "message": tkn})
    else:
        return Response({"status":404, "message": ""})   


@api_view(['GET'])
def get_current_deals(request):

    nine_product_data=[]
    for pro in col.find().limit(10).sort([('$natural',-1)]):
       product={}
       product['product_id'] = pro['product_id']
       product["product_image"] = pro["product_image"]
       product["product_title"] = pro["product_title"]
       product["product_price"] = pro["product_price"]
       nine_product_data.append(product)

    return Response({'message':200, 'product_data':nine_product_data})   


@api_view(['POST'])
def create_user(request):
    data = request.data
    username = data['username']
    password = data['password']
    tkn = data['tkn']

    # check if token is from admin or not
    token_object = token_collection.find_one({'tkn':tkn})
    if token_object:
        if token_object['user_name'] != 'admin':
            return Response({"status":503, "message":"Only authorised User is allowed to create new user"})
    else:
        return Response({"status":503, "message":"Only authorised User is allowed to create new user1"})


    if username and password:
        # check already exits
        user_avial_status = User.objects.filter(username = username).exists()
        if user_avial_status:
            print("user already exits create another or update")
            return Response({'status':503, 'message':'user already exits'})

        else:
            # lets create new user
            user = User.objects.create_user(username = username, password= str(password))
            # create the token for the new user
            print(create_and_get_token("user_name", username))
            return Response({'status':200, 'message':'new user is created'})
    else:
        return Response({'status':404, 'message':'One of the field is misssing or empty'})

@api_view(['POST'])
def change_user_password(request):
    data = request.data
    tkn = data['tkn']
    user = data['user']
    pwrd = data['pwrd']
    # check token
    if tkn:
        token_check = token_collection.find_one({"tkn":tkn})
        if token_check:
            if token_check['user_name']=='admin':
                usr = User.objects.filter(username=user)
                if usr and user!='admin':
                    usr = User.objects.get(username=user)
                    usr.set_password(pwrd)
                    usr.save()
                    return Response({'status':200, 'message':'Password is changed'})
            else:
                return Response({"status":503, "message":"Unauthorized User"})

    return Response({'status':503, 'message':'Unauthorzied Users'})

@api_view(['POST'])
def check_admin(request):
    data = request.data
    tkn = data['tkn']    
    if tkn:
        # check admin
        token_check = token_collection.find_one({'tkn':tkn})
        if token_check:
            if token_check['user_name'] == 'admin':
                return Response({'status':200})
            else:
                return Response({'status':503, 'message':token_check['user_name']})    
        else:
            return Response({'status':404})        
    else:
        return Response({'status':404})    

@api_view(['Get'])
def get_users(request):
    users = User.objects.all()
    userss = []
    for usr in users:
        userss.append(usr.username)
    return Response({'status':200, 'message':userss})




class Webhook(APIView):

    def get(self, request):
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        chal = request.query_params.get("hub.challenge")
        if mode and token:
            with open('n.txt', 'w') as f:
                f.write(chal)
            return HttpResponse(chal)
        else:
            return HttpResponse(400)

    def post(self, request):
        data = request.data
        if data:
            changes = data['entry'][0]['changes'][0]
            field = changes['field']
            if field == 'messages':
                value = changes['value']
                message = value['messages'][0]
                number = message['from']
                message_text = message['text']['body']
                wa_id = value['contacts'][0]['wa_id']
                # print(wa_id,"\n",message_text,"\n")\
                return_message = conversation(number, message_text)
                send_message(number, return_message)
                return HttpResponse(return_message)
                # if message_text == "hello":
                #     send_message(wa_id)

            return HttpResponse(200)
        else:
            return HttpResponse(400)

