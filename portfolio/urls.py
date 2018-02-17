from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^customer/$', views.customer_list, name='customer_list'),
    url(r'^customer/(?P<pk>\d+)/delete/$', views.customer_delete, name='customer_delete'),
    url(r'^customer/(?P<pk>\d+)/edit/$', views.customer_edit, name='customer_edit'),
    url(r'^customer/(?P<pk>\d+)/portfolio/$', views.portfolio, name='portfolio'),
    url(r'^stock/$', views.stock_list, name='stock_list'),
    url(r'^stock/(?P<pk>\d+)/delete/$', views.stock_delete, name='stock_delete'),
    url(r'^stock/(?P<pk>\d+)/edit/$', views.stock_edit, name='stock_edit'),
    url(r'^stock/create/$', views.stock_new, name='stock_new'),

    url(r'^investment/$', views.investment_list, name='investment_list'),
    url(r'^investment/(?P<pk>\d+)/delete/$', views.investment_delete, name='investment_delete'),
    url(r'^investment/(?P<pk>\d+)/edit/$', views.investment_edit, name='investment_edit'),
    url(r'^investment/create/$', views.investment_add, name='investment_add'),

    url(r'^currency/$', views.currency_list, name='currency_list'),
    url(r'^currency/(?P<pk>\d+)/delete/$', views.currency_delete, name='currency_delete'),
    url(r'^currency/(?P<pk>\d+)/edit/$', views.currency_edit, name='currency_edit'),
    url(r'^currency/create/$', views.currency_new, name='currency_new'),

    url(r'^customers_json/', views.CustomerList.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
