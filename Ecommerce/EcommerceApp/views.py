from django.shortcuts import render,HttpResponse,redirect
from.models import Product,CartItem,Order
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from .forms import createUserForm,AddProduct
from django.contrib import messages
import random
import razorpay


# Create your views here.
def index(req):
    product = Product.objects.all()
    context={}
    context['products']=product
    return render(req,"index.html",context)

def details(req,pid):
    products=Product.objects.get(wid=pid)
    context={'products':products}
    
    return render(req,'details.html',context)

def cart(req):
    if req.user.is_authenticated :
      allproducts=CartItem.objects.filter(user=req.user)
    else:
        return render(req,"login.html")
    context={}
    context['cart_items']=allproducts
    total_price=0
    
    for x in allproducts:
        total_price += (x.product.price*x.quantity)
        context['total']= total_price
        length= len(allproducts)
        context['item']= length
    return render(req,'cart.html',context)

def Addcart(req,pid):
    products=Product.objects.get(wid=pid)
    user=req.user if req.user.is_authenticated else None
    print(products)
    if user:
       cart_item,created=CartItem.objects.get_or_create(product=products,user=user)
       print(cart_item,created)
    else:
        return redirect("/loginuser")
      #cart_item,created=CartItem.objects.get_or_create(product=products)

    if not created:
        cart_item.quantity += 1
    else :
        cart_item.quantity = 1
    cart_item.save()
   
    return redirect("/cart")

""" def remove(req,pid):
    m= CartItem.objects.get(wid=pid)
    print(m)
    m.delete()
    return redirect("/cart") """

def remove(req,pid):
    print("id to be deleted",pid)
    products=Product.objects.get(wid=pid    )
    #return HttpResponse(f"Pid is {pid}")
    m = CartItem.objects.filter(product=products)
    
    m.delete()
    return redirect("/cart")

def search(req):
    pro=req.POST['q']
    if not pro:
        result=Product.objects.all()
    else:
        result=Product.objects.filter(
             Q(product_name__icontains=pro)|
            Q(price__icontains=pro)
        )
    return render (req,"search.html",{'result':result , 'query':pro})

def range(req):
    if req.method == 'GET':
        return redirect("/")
    else:
        r1 =req.POST.get("min")
        r2 =req.POST.get("max")
        print(r1,r2)
        # return HttpResponse(f"min:{r1} max:{r2}")
        if r1 is not None and r2 is not None and r1 != "" and r2 != "":
            queryset= Product.prod.get_price_range(r1,r2)
            print(queryset)
            context={'products':queryset}
            return render (req,"index.html",context)
        
def watchList(req):
    queryset= Product.prod.Watch_list()
    print(queryset)
    context={'products':queryset}
    return render (req,"index.html",context)

def laptopList(req):
    queryset= Product.prod.laptop_list()
    print(queryset)
    context={'products':queryset}
    return render (req,"index.html",context)

def mobileList(req):
    queryset= Product.prod.mobile_list()
    print(queryset)
    context={'products':queryset}
    return render (req,"index.html",context)

def sort(req):
    queryset=Product.objects.all().order_by("price")
    
    context={'products':queryset}
    return render (req,"index.html",context)

def sort2(req):
    queryset=Product.objects.all().order_by("-price")
    queryset=Product.prod.price_order()
    context={'products':queryset}
    return render (req,"index.html",context)

def updateqty(req,uval,pid):
    products= Product.objects.get(wid=pid)
    user=req.user
    c = CartItem.objects.filter(product=products,user=user)
    if uval == 1:
        a=c[0].quantity +1
        c.update(quantity=a)
        print(c[0].quantity)
    else:
        a=c[0].quantity -1
        c.update(quantity=a)
        print(c[0].quantity)
    return redirect("/cart")

def register(req):
    form = createUserForm()
    if req.method == "POST":
        form= createUserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req,("user created successfully"))
            return redirect("/login")
        else:
            messages.error(req,"INcorrect Password format")
    context = {'form':form}
    return render(req,"register.html",context)

def loginuser(req):
    if req.method == "POST":
        username=req.POST["username"]
        password=req.POST["password"]
        user = authenticate(req,username=username,password=password)
        if user is not None:
            login(req,user)
            messages.success(req,("you have been loged in !!!!!"))
            return redirect('/')
        else:
            messages.error(req,"incorrect username or password")
            return redirect("/loginuser")
    else:
       return render(req,"login.html")

def logoutuser(req):

    logout(req)
    messages.success(req,("you have logout successfully"))
    return redirect("/")


def vieworder(req):
    c=CartItem.objects.filter(user=req.user)
    # oid=random.randrange(1000,9999)
    # for x in c:
    #     Order.objects.create(order_id=oid,product_id=x.product.wid, user=req.user , quantity=x.quantity)
    # orders= Order.objects.filter(user=req.user,is_completed=False)
    context={}
    context['cart_items']=c
    total_price=0
    for x in c:
        total_price += (x.product.price*x.quantity)
        context['total']= total_price
        length= len(c)
        context['item']= length
    return render(req,'vieworder.html',context)


def payment(req): 
    c=CartItem.objects.filter(user=req.user)
    oid=random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id=oid,product_id=x.product.wid, user=req.user , quantity=x.quantity)
    orders= Order.objects.filter(user=req.user,is_completed=False)
    total_price=0
    for x in orders:
        total_price += (x.product.price*x.quantity) 
        oid= x.order_id
    client = razorpay.Client(auth=("rzp_test_hniIgjM02jCx7q","86o0FtQ5zs0lASE8nohaIsiy"))
    data={
  "amount": total_price*100,
  "currency": "INR",
  "receipt": "oid",
    }
    pay= client.order.create(data=data)
    c.delete()
    orders.update(is_completed=True)
    return render (req,"payment.html",pay)

def insertProduct(req):
    if req.user.is_authenticated:
        user=req.user
        if req.method =="GET":
            form=AddProduct()
            return render (req,"insertprod.html",{'form':form})
        else :
          form =AddProduct(req.POST,req.FILES or None)
          if form.is_valid():
              form.save()
              messages.success(req,("product entered successfully"))
              return redirect("/")
          else:
            messages.error(req,"incorrect data")
            return render(req,"insertProd.html",{"form":form})
    else:
        return redirect("loginuser/")
    

