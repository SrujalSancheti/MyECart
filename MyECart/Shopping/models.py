from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    product_desc = models.CharField(max_length=300)
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    pub_date = models.DateField(blank=True,null=True)
    image = models.ImageField(upload_to="Shopping/images",default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,default="")
    desc = models.CharField(max_length=500,default="")
    phone = models.CharField(max_length=10,default="")

    def __str__(self):
        return "Message By: " + self.name
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=500)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    altphone = models.CharField(max_length=10,default="")
    address = models.CharField(max_length=200,default="")
    state = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    zip_code = models.CharField(max_length=7)
    
    def __str__(self):
        return self.name + " (" +self.phone+")"



class OrderUpdates(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=1000)
    timestamp =models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
