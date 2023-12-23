from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import  login_required
# Create your views here.


def allcategories(request):
    b=Category.objects.all()
    return render(request,'category.html',{'b':b})


def allproducts(request,p):
    c=Category.objects.get(name=p)
    p=Product.objects.filter(category=c)
    return render(request,'allproducts.html',{'c':c,'p':p})


def productdetails(request,p):
    p=Product.objects.get(name=p)
    return render(request,'productdetails.html',{'p':p})

def user_register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        e=request.POST['e']
        if(p==cp):
            u=User.objects.create_user(username=u,password=p,email=e)
            u.save()
            return redirect('shop:category')
        else:
            return HttpResponse("Password not matching")
    return render(request,'register.html')

def user_login(request):
    if(request.method=="POST"):
        username=request.POST['u']
        password=request.POST['p']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('shop:category')
        else:
            messages.error(request,'Invalid credentials')
    return render(request,'login.html')

@login_required
def user_logout(request):
    logout(request)
    return user_login(request)