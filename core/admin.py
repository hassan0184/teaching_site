from django.contrib import admin
from .models import Service,Contact,Booking

class ServiceAdmin(admin.ModelAdmin):
    list_display=['id','title','price','duration','created_at','updated_at']

class ContactAdmin(admin.ModelAdmin):
    list_display=['id','name','email','created_at']

class BookingAdmin(admin.ModelAdmin):
    list_display=['id','name','email','service','date','time']



admin.site.register(Service,ServiceAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Booking,BookingAdmin)