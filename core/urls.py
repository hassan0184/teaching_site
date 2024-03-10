from django.urls import path
from .views import HomePageView,save_contact


urlpatterns = [

    
    path('', HomePageView.as_view(), name='home'),
    path('save_contact', save_contact, name='save_contact'),

]
