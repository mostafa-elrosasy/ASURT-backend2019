from django.urls import path
from AuthenticationSystem import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as rest_views
from rest_framework_jwt.views import verify_jwt_token

# from .views import views


urlpatterns = [
<<<<<<< HEAD
    path('register/', views.SignUpList.as_view()),
    path('login/',views.EmailSignInView.as_view()),
    path('social/',views.Social.as_view()),
=======
    path('register/', views.SignUpView.as_view()),
    path('social/',views.SocialSignInView.as_view()),
>>>>>>> 7be1c400f980dfd06fb9d56ad5d878784014b9ef
    path('api-token-auth/', rest_views.obtain_auth_token),
    path('token-verify/',verify_jwt_token),
    path('forgetpassword/',views.ForgetPasswordView),
    path('login/',views.SignInView.as_view()),
    path('changepassword/',views.ChangePasswordView)
]


urlpatterns = format_suffix_patterns(urlpatterns)
