from django.urls import path
from . import views
from .views import stk_push
from .views import message_mail


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout_view'),
    path('book/', views.book, name='book'),
    path('amenities/', views.amenities, name='amenities'),
    path('rates/', views.rates, name='rates'),
    path('contact/', views.contact, name='contact'),   
    path("stkpush/",stk_push, name="stkpush"),
    path("message/",message_mail, name="message_mail"),
    path("gallery/",views.gallery, name="gallery"),
    path("rooms/",views.rooms, name="rooms"),
    path("visit/",views.visit, name="visit")
]