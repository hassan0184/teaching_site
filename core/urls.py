from django.urls import path
# from .views import HomePageView,save_contact,save_booking,process_payment,payment_execute,payment_cancel

from .views import HomePageView,save_contact,save_booking,create_payment,payment_execute,payment_cancel


urlpatterns = [

    
    path('', HomePageView.as_view(), name='home'),
    path('save_contact', save_contact, name='save_contact'),
    path('save_booking/', save_booking, name='save_booking'),
    path('create_payment/', create_payment, name='create_payment'),
    path('payment/execute/', payment_execute, name='payment_execute'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),


]
