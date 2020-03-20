from django.conf.urls import url
from . import classviews

urlpatterns = [
    url(
        r'^producer/$',
        classviews.ProducerLC.as_view(),
        name='producer_list_create',
    ),
    url(
        r'^producer/(?P<pk>\d+)/$',
        classviews.ProducerRUD.as_view(),
        name='producer_retrieve_update_delete',
    ),
]
