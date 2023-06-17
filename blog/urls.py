"""iblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import home,category,about,catagor,blog,post_details, create_user, acco
from . import views
from django.contrib.auth import views as auth_views
from django.urls import include, path
from .views import create_blog_view
from django.urls import path
from .views import delete_blog_view,update_post_view


urlpatterns = [
    path('about/', about),
    path('blog/', blog),
    path('home/', home),
    path('', home),
    path('category/', catagor),
    path('blog/<slug:url>/', post_details, name='post_details'),
    path('category/<slug:url>',category),
    path('search/', views.search_results, name='search_results'),
    path('create-user/', views.create_user, name='create_user'),
    path('signup/', views.create_user, name='create_user'),
    path('accounts/signup/', views.create_user, name='create_user'),
    path('acco/', acco, name='acco'),
    path('accounts/acco/', acco, name='acco'),
    path('accounts/', acco, name='acco'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),  # Include authentication-related URLs
    path('accounts/profile/', views.profile_view, name='profile'),  # Define URL pattern for profile view
    path('create-blog/', create_blog_view, name='create_blog'),

    # Other URL patterns
    path('delete-post/<int:post_id>/', delete_blog_view, name='delete_post'),
    path('update-post/<int:post_id>/', update_post_view, name='update_post'),
    path('logout/', views.logout_view, name='logout'),
]

