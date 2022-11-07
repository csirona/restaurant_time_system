from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #add core.urls
    path('',include('core.urls'))
]
