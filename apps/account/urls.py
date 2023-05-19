from django.urls import path
from .views import AccountListAPIView, AccountRUDApiView, RegisterAPIView, LoginAPIView, MyAccountAPIView


urlpatterns = [
    path('list/', AccountListAPIView.as_view()),
    path('detail/<int:pk>/', AccountRUDApiView.as_view()),
    path('my_account/', MyAccountAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]