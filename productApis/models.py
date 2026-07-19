from itertools import product
from django.db import models
import jsonfield
# Create your models here.

# change to pip3 install sqlparse==0.2.4
class ProductData(models.Model):

    product_id = models.CharField(max_length=255)
   
    product_title = models.CharField(max_length=1000)
   
    product_url = models.CharField(max_length=1000)
   
    product_image = models.CharField(max_length= 1000)

# classification
    product_binding = models.CharField(max_length=255, null=True)
    product_group = models.CharField(max_length=255, null=True)
    
# product features
    product_features = jsonfield.JSONField()
    
# product info
    product_height = models.CharField(max_length=255, null=True)
    product_width = models.CharField(max_length=255, null=True)
    product_weight = models.CharField(max_length=255, null=True)
    product_length = models.CharField(max_length=255, null=True)
    product_size = models.CharField(max_length=255, null=True)

# manufacturing details
    product_manufacture_id = models.CharField(max_length=255, null=True)
    product_manufacture_model = models.CharField(max_length=255, null=True)
    product_manufacture_warranty = models.CharField(max_length=255, null=True)

    product_merchant_name = models.CharField(max_length=255, null=True)
    product_price = models.CharField(max_length=255)
    product_discount = models.CharField(max_length=255, null=True)
    product_discount_percentage = models.CharField(max_length=255, null=True)