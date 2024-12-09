from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
   # path('dashboard/', views.dashboard, name='dashboard'),  # Add your dashboard route
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Login route
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Logout route
]
