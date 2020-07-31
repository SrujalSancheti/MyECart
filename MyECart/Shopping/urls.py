from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="Home"),
    path('search/', views.search, name="Search"),
    path('about/',views.about,name="AboutUs"),
    path('contact/',views.contact,name="ContactUs"),
    path('tracker/',views.tracker,name="TrackingStatus"),
    path('product/<int:myid>',views.product,name="Product"),
    path('checkout/',views.checkout,name="Checkout"),
    path('signup', views.handleSignUp , name = "handleSignUp"),
    path('login', views.handlelogin , name = "handlelogin"),
    path('logout', views.handlelogout , name = "handlelogout"),
    path('handlerequest/',views.handlerequest,name="HandleRequest"),
]