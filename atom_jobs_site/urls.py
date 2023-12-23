"""
URL configuration for atom_jobs_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from jobs.views.send_resume import SendResumeView
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views
from jobs.views.api import JobAPIView, JobSearchAPIView
from jobs.views.pages.job import JobPageView
from jobs.views.jobboard import JobboardView
from jobs.views.forms.submit import SubmitFormView
# from jobs.views.send_resume import SendResumeView
from django.conf import settings
# from jobs import views
from jobs.views import views
# from atom_jobs.views.send_resume import SendResumeView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('search/', include('haystack.urls')),
    path('api/jobs/', JobAPIView.as_view()),
    path('api/jobs/search/', JobSearchAPIView.as_view()),
    path('jobs/<int:job_id>', JobPageView.as_view()),
    path('submit/<int:job_id>', SubmitFormView.as_view(), name='submit'),
    path('jobboard/', JobboardView.as_view()),
    # re_path(r'^jobs/', include(('urls', 'jobs'),namespace='jobs')),
    # re_path(r'^search/$', views.post_search, name='post_search'),
    # re_path(r'^$', views.JobListView.as_view(), name='job_list'),
    re_path(r'^$', views.job_list, name='job_list'),
    # path('sendresume/', views.SendResumeView.as_view()),
]



# from django.contrib import admin
# from django.conf.urls import include
# from django.urls import path, include, re_path


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('search/', include('haystack.urls')),
#     re_path(r'^jobs/', include(('jobs.urls','jobs'),namespace='jobs.urls',)),
# ]
# #    re_path(r'^jobs/', include(('jobs.urls','jobs'),namespace='jobs.urls',)),