from django.urls import path

from . import views

app_name = "proxy"

urlpatterns = [
    path('<str:coin>/create/', views.create, name='create'),
    path('<str:coin>/logs/', views.logs, name='logs'),
    path('callback/<str:request_id>/<str:nonce>/', views.callback, name='callback'),
]
