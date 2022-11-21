from django.contrib import admin
from .models import Person,Expenses,Comment,Ip
admin.site.register(Person)
admin.site.register(Expenses)
admin.site.register(Comment)
admin.site.register(Ip)
# Register your models here.
