from django.urls import path
from WebsiteSystem import views
from django.conf.urls import url

urlpatterns = [
    path('', views.SponsorView.as_view()),
]

