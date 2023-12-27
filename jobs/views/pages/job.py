from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from jobs.models import Job
from django.contrib.auth.mixins import LoginRequiredMixin

class JobPageView(View):
	template_name = 'pages/job.html'

	def get(self, request, job_id):
		job = Job.objects.get(hh_id=str(job_id))
		# import pdb; pdb.set_trace()
		return render(request=request, template_name=self.template_name, context={
			'job_id': job_id,
			'name': job.name,
			'city': job.city,
			'street': job.street,
			'requirements': job.requirements,
			'responsibility': job.responsibility,
			'schedule': job.schedule,
			'prof_roles': job.prof_roles,
			'experience': job.experience,
			'url': job.url,
			'description': job.description,
			'languages': job.languages
			})