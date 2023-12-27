from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from jobs.models import Response
from django.contrib.auth.mixins import LoginRequiredMixin

class SendResumeView(View, LoginRequiredMixin):
	template_name = 'job/send_resume.html'

	def get(self, request):
		return render(request=request, template_name=self.template_name)