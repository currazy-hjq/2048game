from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^show$',views.scorelistview),
    url(r'^add$',views.addlistview),
    url(r'^init$',views.initview),
]