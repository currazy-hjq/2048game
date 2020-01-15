from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^play$',views.GameConsoleView.as_view()),
    url(r'^$',views.mapview),
    url(r'^init$',views.initview),
]

