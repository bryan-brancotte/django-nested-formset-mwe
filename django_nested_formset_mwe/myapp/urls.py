from django.conf.urls import url
from django.urls import reverse
from django.views.generic import RedirectView

from . import views

app_name = 'myapp'
urlpatterns = [
    url(r'^promotion/(?P<pk>\d+)/edit$', views.PromotionUpdateView.as_view(), name='promotion-edit'),
    url(r'^promotion/(?P<pk>\d+)/$', views.PromotionDetailView.as_view(), name='promotion-detail'),
    url(r'^promotion/create/$', views.PromotionCreateView.as_view(), name='promotion-create'),
    url(r'^promotion/$', views.PromotionListView.as_view(), name='promotion-list'),
    url(r'^$', RedirectView.as_view(url='promotion/', permanent=False), name='index')
]
