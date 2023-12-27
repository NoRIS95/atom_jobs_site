from rest_framework import generics
from django.shortcuts import render, redirect
# from .forms import NewUserForm
from django.contrib.auth import login
from django.conf import settings
from django.contrib import messages
from jobs.models import Job, Response
from django.contrib.auth.models import User
from jobs.serializers import JobSerializer, ResponseAPISerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from dateutil.parser import parse as parse_date
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
# Create your views here.
from django.http import HttpResponse
import json
from haystack.query import SearchQuerySet, SQ

class JobAPIView(generics.ListAPIView):
	queryset = Job.objects.all()
	serializer_class = JobSerializer

	def get(self, request):
		# requests.get('http://localhost:8000/api/v1/locations/')
		queryset = Job.objects.all()
		return Response(JobSerializer(queryset, many=True, context={'request': request}).data,
			status=status.HTTP_200_OK)

class JobSearchAPIView(generics.ListAPIView):
	serializer_class = JobSerializer

	def get(self, request):
		# requests.get('http://localhost:8000/api/v1/locations/')
		queryset = self.get_queryset()
		return Response(JobSerializer(queryset, many=True, context={'request': request}).data,
			status=status.HTTP_200_OK)

	def get_queryset(self):
		query = self.request.GET.get('q', '')
		return SearchQuerySet().models(Job).filter(SQ(name=query) |\
			SQ(requirements=query) |\
			SQ(responsibility=query) |\
			SQ(prof_roles=query) |\
			SQ(description=query)).load_all()

class ResponseAPIView(generics.RetrieveUpdateDestroyAPIView, CreateModelMixin, LoginRequiredMixin):
	serializer_class = ResponseAPISerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		name = request.data.get('name')
		surname = request.data.get('surname')
		lastname = request.data.get('lastname')
		e_mail = request.data.get('e_mail')
		phone = request.data.get('phone')
		cv = request.FILES.get('cv', False)
		cv.name = f"{surname}_{name}.pdf"
		Response.objects.create(name=name, surname=surname, lastname=lastname, e_mail=e_mail, phone=phone)
		return redirect("/jobboard", status=status.HTTP_200_OK)