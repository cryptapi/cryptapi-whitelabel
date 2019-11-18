from django.urls import path

from . import views

app_name = "index"

urlpatterns = [
    path('', views.index, name='index'),
    path('docs/api.json', views.docs_api_json, name='docs_api_json'),
    path('docs/', views.docs, name='docs'),
    path('get_started/', views.get_started, name='get_started'),
    path('pricing/', views.pricing, name='pricing'),
]
