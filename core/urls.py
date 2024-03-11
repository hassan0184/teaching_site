from django.urls import path
from .views import HomePageView,save_contact,save_booking


urlpatterns = [

    
    path('', HomePageView.as_view(), name='home'),
    path('save_contact', save_contact, name='save_contact'),
    path('save_booking/', save_booking, name='save_booking'),


]
