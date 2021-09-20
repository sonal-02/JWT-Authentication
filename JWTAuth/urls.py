from django.urls import path
from .views import SignUp, Login
from .curd import ListCreateUserView, UpdateRetrieveDeleteUser

urlpatterns = [

    # Authentication urls
    path('signup/', SignUp.as_view(), name='sign_up'),
    path('login/', Login.as_view(), name='login'),

    # CURD urls
    path('list_create/', ListCreateUserView.as_view(), name='list'),
    path('update_retrieve_delete/<int:pk>/', UpdateRetrieveDeleteUser.as_view(), name='create'),

]
