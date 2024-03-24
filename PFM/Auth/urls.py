
from django.contrib import admin
from django.urls import path , include
from Auth.views import LoginView, RegisterView , UpdateInformation , GetUserDetails

admin.autodiscover()
app_name = 'Auth'


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update-user/', UpdateInformation.as_view(), name='update_user'),
    path('get-user-details/', GetUserDetails.as_view(), name='get_user_details')
]
