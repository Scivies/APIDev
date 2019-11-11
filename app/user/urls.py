from django.urls import path
from user import views
"""Which app do we create the URL from"""

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    ]
