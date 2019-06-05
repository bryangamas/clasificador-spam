from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('clasificadorSpam/', include('clasificadorSpam.urls')),
    path('admin/', admin.site.urls)
]
