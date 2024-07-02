from django.urls import path

from api.views import CreateUserView

urlpatterns = [
    path('user/', CreateUserView.as_view(), name='create-user'),
]
