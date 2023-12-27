from django.db.models import Q 
from rest_framework import mixins, viewsets 
from haystack.query import SearchQuerySet
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jobs.models import Job
from django.views.generic import ListView
import os, os.path
from whoosh import index, qparser

class SearchResultsView(ListView):

    model = Job

    template_name = 'search_results.html'

    def get_queryset(self):

        query = self.request.GET.get('q')

        object_list = Job.objects.filter(Q(name__icontains=query) | Q(requirements__icontains=query)\
         | Q(prof_roles__icontains=query))
        return object_list


def post_search(request):
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Job).load_all()
            # count total results
            total_results = results.count()
    return render(request,
                  'search/search.html',
                  {'form': form,
                   'cd': cd,
                   'results': results,
                   'total_results': total_results})


class JobListView(ListView):
    queryset = Job.objects.all()
    context_object_name = 'jobs'
    paginate_by = 20
    template_name = 'job/list.html'


def job_list(request):
    object_list = Job.objects.all()
    paginator = Paginator(object_list, JobListView.paginate_by)
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        jobs = paginator.page(paginator.num_pages)
    return render(request,
                  'job/list.html',
                  {'page': page,
                   'jobs': jobs})
