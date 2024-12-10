from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from myapp import views
import grappelli.urls as grappelli_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('grappelli/', include(grappelli_urls)),
    path('index/', views.dashboard_view, name='index'),  # Correct view
    path('', views.register, name='register'),  # Ensure the register view exists
    path('login/', views.login_view, name='login'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

