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
	# queryset = Response.objects.all()

	def post(self, request):
		# import pdb; pdb.set_trace()
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


	# def post(self, request):
	# 	# requests.post('http://localhost:8000/api/v1/locations/', data={'n_seats': 32, 'name': "Test"}, files={'photo': io.getvalue()})
	# 	loc_name = request.data.get('name')
	# 	photo = request.FILES.get('photo', False)
	# 	n_seats = int(request.data.get('n_seats'))
	# 	owner_id = request.user
	# 	locations_cnt = len(Location.objects.filter(owner_id=owner_id).all())
	# 	# photo_extension = photo.name.split('.')[-1]
	# 	photo.name = f"{owner_id}_{locations_cnt}.jpg"
	# 	Location.objects.create(name=loc_name, photo=photo, n_seats=n_seats, owner_id=owner_id)
	# 	return redirect("/dashboard", status=status.HTTP_200_OK)


	# def post(self, request):
	# 	# requests.post('http://localhost:8000/api/v1/locations/', data={'n_seats': 32, 'name': "Test"}, files={'photo': io.getvalue()})
	# 	loc_name = request.data.get('name')
	# 	photo = request.FILES.get('photo', False)
	# 	n_seats = int(request.data.get('n_seats'))
	# 	owner_id = request.user
	# 	locations_cnt = len(Location.objects.filter(owner_id=owner_id).all())
	# 	# photo_extension = photo.name.split('.')[-1]
	# 	photo.name = f"{owner_id}_{locations_cnt}.jpg"
	# 	Location.objects.create(name=loc_name, photo=photo, n_seats=n_seats, owner_id=owner_id)
	# 	return redirect("/dashboard", status=status.HTTP_200_OK)

	# def delete(self, request, id):
	# 	# requests.delete('http://localhost:8000/api/v1/locations/10')
	# 	loc_id = int(id)
	# 	try:
	# 		obj = Location.objects.get(id=loc_id)
	# 		obj.delete()
	# 		return HttpResponse('Location deleted', status=status.HTTP_200_OK)		
	# 	except:
	# 		msg = {'msg': 'not found error'}
	# 		return HttpResponse(msg, status.HTTP_404_NOT_FOUND)