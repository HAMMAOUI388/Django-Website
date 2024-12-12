from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from myapp import views
import grappelli.urls as grappelli_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('grappelli/', include(grappelli_urls)),

    path('index/', views.dashboard_view, name='index'),
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('index/', views.dashboard_view, name='dashboard'),

]
