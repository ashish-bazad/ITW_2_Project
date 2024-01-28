from django.contrib import admin
from .models import User, Profile, Items, toSell, Purchased, Lost, Sold

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Items)
admin.site.register(toSell)
admin.site.register(Purchased)
admin.site.register(Lost)
admin.site.register(Sold)