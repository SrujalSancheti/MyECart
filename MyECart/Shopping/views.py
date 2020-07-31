from django.shortcuts import render,redirect
from .models import Product,Contact,Order,OrderUpdates
from math import ceil  #Used in index Function
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .paytm import Checksum

# Create your views here.
MERCHANT_KEY = 'XwwL5_Jd7u8RzDyK';

# Create your views here.
def index(request):
    products = Product.objects.all()
    # n = len(products)
    # nSlides = n//4 + ceil((n/4) - (n//4))
    # params ={'products':products,'range':range(1,nSlides),'no_of_slides':nSlides }
    allprods=[]
    catProds = Product.objects.values('category','id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(products)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allprods.append([prod,range(1,nSlides),nSlides])
   # allprods =[[products,range(1,nSlides),nSlides ],
           #     [products,range(1,nSlides),nSlides ]]
    params = {'allprods':allprods}
    return render(request,'Shopping/index.html',params)

def searchMatch(query,item):
    if query in item.product_desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allprods = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prods = [item for item in prodtemp if searchMatch(query,item) ]
        n = len(prods)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prods) != 0:
            allprods.append([prods, range(1, nSlides), nSlides])
    params = {'allprods': allprods}
    if len(allprods) == 0 or len(query)<4:
        params = {'msg':"Enter Proper Product name"}
    return render(request, 'Shopping/search.html', params)

def about(request):
    return render(request,'Shopping/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('message','')
        contact = Contact(name = name, phone=phone,email=email, desc=desc)
        contact.save()
        messages.success(request ,"Message sent successfully. The concerned team will conatntact you soon.")
    return render(request,'Shopping/contact.html')

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId','')
        email = request.POST.get('emailt','')
        try:
            order = Order.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update =OrderUpdates.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemJson":order[0].item_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitems"}')
        except Exception:
            return HttpResponse('{"status":"error"}')
    return render(request,'Shopping/tracker.html')

def product(request,myid):
    product = Product.objects.filter(id = myid)
    return render(request,'Shopping/product.html',{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        itemsJson = request.POST.get('itemsJson','')
        amount = request.POST.get('amount','')
        name = request.POST.get('inputName','')
        email = request.POST.get('inputEmail','')
        address = request.POST.get('inputAddress','') + " " + request.POST.get('inputAddress2','')
        phone = request.POST.get('inputPhone','')
        altphone = request.POST.get('inputAltPhone','')
        state = request.POST.get('inputState','')
        city = request.POST.get('inputCity','')
        zip_code = request.POST.get('inputZip','')
        order = Order(item_json=itemsJson, name=name, phone=phone, altphone=altphone, email=email, address=address, state=state, city=city, zip_code=zip_code,amount=amount)
        order.save()
        
        update = OrderUpdates(order_id = order.order_id , update_desc = "Your order is Successfully Placed")
        update.save()
        
        thank = True
        id = order.order_id;
        #return render(request, 'shop/checkout.html', {'thank' :thank,'id':id})
        # Request payment to transfer the amount to your account after after payment by user
        param_dict={
            'MID':'KIFXMA81089636385516',
            'ORDER_ID':str(order.order_id),
            'TXN_AMOUNT':str(amount),
            'CUST_ID':email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/Shopping/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'Shopping/paytm.html',{'param_dict':param_dict})
    return render(request, 'Shopping/checkout.html')


#Authentication API's
def handleSignUp(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2  = request.POST['pass2']
        
        # Check for erroeneous  inputs
        if len(username)>20:
            messages.error(request,"Username must be under 20 characters")
            return redirect('Home')

        if not username.isalnum():
            messages.error(request,"Username Should only contain letters and numbers")
            return redirect('Home')
        
        if pass1 != pass2:
            messages.error(request,"Passwords didn't match")
            return redirect('Home')
        
        if len(pass1)<5:
            messages.error(request,"Lenght of password should be greater than 5")
            return redirect('Home')
        
        # Create User
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Account has been successfully created")
        return redirect('Home')
    else:
        return HttpResponse("404 - Not Found")
    
def handlelogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('Home')
        else:
            messages.error(request,"Invalid Credentials, please try again")
            return redirect('Home')
    return HttpResponse("404 - Not Found")
            
def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('Home')


@csrf_exempt
def handlerequest(request):
    #Patym will send post request here
    forms = request.POST
    response_dict = {}
    for i in forms.keys():
        response_dict[i]=forms[i]
        if i == 'CHECKSUMHASH':
            checksum = forms[i]
    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Payment Successful')
        else:
            print('Payment Unsuccessful because of'+response_dict['RESPMSG'])
    return render(request,'Shopping/paymentstatus.html', {'response':response_dict})
