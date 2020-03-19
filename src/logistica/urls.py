from django.conf.urls import url
from . import classviews

urlpatterns = [
    url(
        r'^production/$',
        classviews.ProductionLC.as_view(),
        name='production_list_create',
    ),
    url(
        r'^production/<int:id>/$',
        classviews.ProductionRUD.as_view(),
        name='production_retrieve_update_delete',
    ),
]
