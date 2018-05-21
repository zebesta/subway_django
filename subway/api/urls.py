from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^train/$', views.train, name='train')
]
