from django.urls import path
from apps.oee.views import MyAPIView
urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', login, name='login'),
    # path('logout/', logout, name='logout'),
    path('myendpoint/', MyAPIView.as_view(), name='my-api-endpoint'),

]
