"""RT_Website_19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from rest_framework_jwt.views import verify_jwt_token
<<<<<<< HEAD

from AuthenticationSystem import urls as ASystem
=======
from AuthenticationSystem import views
from AuthenticationSystem import urls as AuthenticationSystem
>>>>>>> 7be1c400f980dfd06fb9d56ad5d878784014b9ef
from ProfileSystem import urls as ProfileSystem


urlpatterns = [
    path('', include(ASystem)),
    path('token-verify/', verify_jwt_token),
<<<<<<< HEAD
    path('admin/', admin.site.urls)
=======
    path('admin/', admin.site.urls),
    path('register/', views.SignUpView.as_view()),
    path('signin/', views.SignInView.as_view()),
    path('user-exist/', views.UserExist.as_view()),

    path('/', include(AuthenticationSystem)),
>>>>>>> 7be1c400f980dfd06fb9d56ad5d878784014b9ef
    # path('api/Profile/', include(ProfileSystem)),
]
