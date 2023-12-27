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
		name = request.data.get('name')
		surname = request.data.get('surname')
		lastname = request.data.get('lastname')
		e_mail = request.data.get('e_mail')
		phone = request.data.get('phone')
		text = request.data.get('text')
		cv = request.FILES.get('cv', False)
		cv.name = f"{surname}_{name}.pdf"
		job = Job.objects.get(hh_id=job_id)
		Response.objects.create(name=name, surname=surname, lastname=lastname, e_mail=e_mail, phone=phone, job=job)
		return redirect("/jobboard")