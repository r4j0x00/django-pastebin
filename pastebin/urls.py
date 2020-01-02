from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from .pastebin import views

urlpatterns = [
    path('',views.main),
    path('<name>',views.paste),
    path('raw/<name>',views.raw),
    path('dl/<name>',views.download),
    #path('admin/', admin.site.urls),
]
