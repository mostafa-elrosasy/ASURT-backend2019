from django.urls import path
from WebsiteSystem import views
from django.conf.urls import url

urlpatterns = [
    path('all/', views.SponsorGetView.as_view()),
    path('', views.SponsorPostView.as_view()),
    path('(?P<pk>[0-9]+)/$', views.SponsorDelView.as_view()),
]

