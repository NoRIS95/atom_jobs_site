from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):

	class Meta:
		model = Job
		fields = ('hh_id', 'name', 'city', 'street', 'requirements', 'responsibility', \
			'schedule', 'prof_roles', 'experience', 'url', 'description'. 'languages')