from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('index.urls')),
    path('api/', include('proxy.urls')),
    path('admin/', admin.site.urls),
]

handler404 = 'index.views.go_home'
