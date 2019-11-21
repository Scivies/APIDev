from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

#Create Default router that will generate the view set.
#Router automatically performs the actions for the urls
#Example: /api/receipe/tags/

router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
