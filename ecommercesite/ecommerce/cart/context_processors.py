from cart.models import cartmodel


def product_count(request):
    item_count=0
    if request.user.is_authenticated:
        u=request.user
        try:
            cart=cartmodel.objects.filter(user=u)
            for i in cart:
                item_count=item_count+i.quantity
        except:
            item_count=0
    return {'count':item_count}


