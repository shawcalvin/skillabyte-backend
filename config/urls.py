"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from .admin import admin_site, super_admin_site

base_path = 'api/v1'

urlpatterns = [
    path(f'{base_path}/auth/', include("api.auth.urls")),
    path(f'{base_path}/users/', include("api.users.urls")),
    path(f'{base_path}/organizations/', include("api.organizations.urls")),
    path(f'{base_path}/courses/', include("api.courses.urls")),
    path(f'{base_path}/ratings/', include("api.ratings.urls")),
    path(f'{base_path}/modules/', include("api.modules.urls")),
    path(f'{base_path}/payments/', include("api.payments.urls")),
    path(f'{base_path}/content/quizzes/', include("api.content.quizzes.urls")),
    path(f'{base_path}/content/chatbots/', include("api.content.chatbots.urls")),
    path('admin/', admin_site.urls),
    path('superadmin/', super_admin_site.urls),
]
