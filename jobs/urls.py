from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # url(r'^$', views.post_list, name='post_list'),
    # url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
    #     r'(?P<post>[-\w]+)/$',
    #     views.post_detail,
    #     name='post_detail'),
    re_path(r'^$', views.job_list, name='job_list'),
    re_path(r'^$', views.JobListView.as_view(), name='job_list'),
    # re_path(r'^jobs/', include(('jobs.urls', 'jobs'),namespace='jobs')),
    # re_path(r'^search/$', views.post_search, name='post_search'),
]
# url(r'^reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),