from django.contrib import admin
from cart.models import cartmodel,order,Account
# Register your models here.
admin.site.register(cartmodel)
admin.site.register(order)
admin.site.register(Account)