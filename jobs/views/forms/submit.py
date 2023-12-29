from rest_framework.generics import CreateAPIView
from jobs.models import Response, Job
from django.shortcuts import render, redirect
from jobs.serializers import ResponseAPISerializer
from rest_framework.parsers import MultiPartParser, FormParser


class SubmitFormView(CreateAPIView):
	queryset = Response.objects.all()
	serializer_class = ResponseAPISerializer
	parser_classes = MultiPartParser, FormParser

	def post(self, request, job_id):
		firstname = request.data.get('firstname')
		surname = request.data.get('surname')
		lastname = request.data.get('lastname')
		e_mail = request.data.get('email')
		phone = request.data.get('phone')
		text = request.data.get('application_text')
		cv = request.FILES.get('cv', False)
		cv.name = f"{firstname}_{lastname}.pdf"
		job = Job.objects.get(hh_id=job_id)
		Response.objects.create(firstname=firstname, surname=surname, text=text,
			lastname=lastname, e_mail=e_mail,
			phone=phone, cv=cv, job=job)
		return redirect("/")