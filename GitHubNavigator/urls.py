from django.conf.urls import url, include
from django.contrib import admin
from navigator import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^navigator/', include('navigator.urls', namespace='navigator'))
]
