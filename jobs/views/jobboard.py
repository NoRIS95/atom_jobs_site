from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from jobs.models import Job
from django.contrib.auth.mixins import LoginRequiredMixin

class JobboardView(View, LoginRequiredMixin):
	template_name = 'pages/jobboard.html'

	def get(self, request):
		jobs = Job.objects.all()
		return render(request=request, template_name=self.template_name,
			context={"jobs": jobs})