from rest_framework import serializers
from .models import Job, Response
import json

class JobSerializer(serializers.ModelSerializer):
	lang = serializers.SerializerMethodField('languages')
	profess_roles = serializers.SerializerMethodField('prof_roles')
	
	class Meta:
		model = Job
		fields = ('hh_id', 'name', 'city', 'street', 'requirements', 'responsibility', \
			'schedule', 'profess_roles', 'experience', 'url', 'description', 'lang')

	def languages(self, instance):
		# import pdb; pdb.set_trace()
		return json.loads(instance.languages)

	def prof_roles(self, instance):
		# import pdb; pdb.set_trace()
		return json.loads(instance.prof_roles)

class ResponseAPISerializer(serializers.ModelSerializer):
	class Meta:
		model = Response
		fields = ('name', 'surname','lastname', 'e_mail', 'phone', 'text', 'job', 'cv')