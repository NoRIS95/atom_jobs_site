from __future__ import unicode_literals
from django.db import models

def resume_file_path(instance, filename):
	return f'resumes/{instance.job.hh_id}/{filename}'

# Create your models here.
class Job(models.Model):
	hh_id = models.CharField(max_length=60)
	name = models.CharField(max_length=80)
	city = models.CharField(max_length=30)
	street = models.CharField(max_length=30)
	requirements = models.TextField()
	responsibility = models.TextField()
	schedule = models.CharField(max_length=30)
	prof_roles = models.TextField()
	experience = models.CharField(max_length=10)
	url = models.CharField(max_length=5000)
	description =  models.TextField()
	languages = models.TextField()
	def save(self, *args, **kwargs):
		return super(Job, self).save(*args, **kwargs)
	def __unicode__(self):
		return "{}:{}".format(self.name, self.city)

class Response(models.Model):
	firstname = models.CharField(max_length=20, null=True)
	surname = models.CharField(max_length=30, null=True)
	lastname = models.CharField(max_length=30, null=True)
	e_mail = models.CharField(max_length=60, null=True)
	phone = models.CharField(max_length=60, null=True)
	text = models.TextField()
	job = models.ForeignKey(Job, on_delete=models.CASCADE)
	cv = models.FileField(upload_to=resume_file_path)