from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list_view, name = "post_list_view"),
    url(r'^listpost/$', views.PostListView.as_view(), name = "post_list_view"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/$',
        views.post_detail_view,
        name='post_detail_view'
    ),
    url(r'^(?P<post_id>\d+)/shareform/$', views.ShareFormView.as_view(),name='share_post'),
]
