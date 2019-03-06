from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as rest_views

# from .views import views


urlpatterns = [
    path('register/', views.SignUpList.as_view()),
    path('login/',views.EmailSignInView.as_view()),
    path('social/',views.SocialSignInView.as_view()),
    path('api-token-auth/', rest_views.obtain_auth_token),
    path('forgetpassword/',views.ForgetPasswordView),
    path('changepassword/',views.ChangePasswordView)
]


urlpatterns = format_suffix_patterns(urlpatterns)
