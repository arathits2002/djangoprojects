from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import cartmodel,Account,order
# Create your views here.

@login_required
def addtocart(request,p):
    product=Product.objects.get(name=p)
    u=request.user
    try:
        cart=cartmodel.objects.get(user=u,product=product)
        if(cart.quantity<cart.product.stock):
            cart.quantity+=1
        cart.save()
    except:
        cart=cartmodel.objects.create(product=product,user=u,quantity=1)
        cart.save()
    return redirect('cart:cartview')


@login_required
def cartview(request):
    sum=0
    u=request.user
    try:
        cart=cartmodel.objects.filter(user=u)
        for i in cart:
            sum+=i.quantity*i.product.price


    except:
        pass
    return render(request,'addtocart.html',{'c':cart,'total':sum})

@login_required
def cart_remove(request,p):
    p=Product.objects.get(name=p)
    user=request.user
    try:
        cart=cartmodel.objects.get(user=user,product=p)
        if cart.quantity>1:
            cart.quantity-=1
            cart.save()
        else:
            cart.delete()
    except:
        pass
    return redirect('cart:cartview')


@login_required
def full_remove(request,p):
    p=Product.objects.get(name=p)
    user=request.user
    try:
        cart=cartmodel.objects.get(user=user,product=p)
        cart.delete()
    except:
        pass
    return redirect('cart:cartview')

def orderform(request):
    if(request.method=="POST"):
        a=request.POST['a']
        no=request.POST['no']
        acno=request.POST['acno']
        u=request.user
        cart=cartmodel.objects.filter(user=u)
        total=0
        for i in cart:
            total +=i.quantity*i.product.price
            ac=Account.objects.get(accnum=acno)
            if(ac.amount>=total):
                ac.amount=ac.amount-total
                ac.save()
                for i in cart:
                    o=order.objects.create(user=u,product=i.product,address=a,phone=no,no_of_items=i.quantity,order_status="paid")
                    o.save()
                    i.product.stock=i.product.stock-i.quantity
                    i.product.save()
                cart.delete()
                msg="order placed successfully"
                return render(request, 'orderdetails.html', {'m': msg})
            else:
                msg="Insufficient amount in User account.you cannot place order."
            return render(request,'orderdetails.html',{'m':msg})
    return render(request,'orderform.html')


def orderview(request):
    u=request.user
    o=order.objects.filter(user=u)
    return render(request,'orderview.html',{'o':o})