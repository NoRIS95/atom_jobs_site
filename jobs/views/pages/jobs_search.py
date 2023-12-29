from django.db.models import Q 
from rest_framework import mixins, viewsets 
from haystack.query import SearchQuerySet, SQ
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jobs.models import Job
from django.views.generic import ListView
import os, os.path

class SearchResultsView(ListView):

    model = Job

    template_name = 'search_results.html'

    def get_queryset(self):

        query = self.request.GET.get('q')

        object_list = Job.objects.filter(Q(name__icontains=query) | Q(requirements__icontains=query)\
         | Q(prof_roles__icontains=query))
        return object_list