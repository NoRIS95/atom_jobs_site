from haystack import indexes
from .models import Job


class JobIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.EdgeNgramField(document=True, use_template=True)
	hh_id = indexes.CharField(model_attr='hh_id')
	name = indexes.CharField(model_attr="name")
	city = indexes.CharField(model_attr="city")
	street = indexes.CharField(model_attr="street")
	requirements = indexes.CharField(model_attr='requirements')
	responsibility = indexes.CharField(model_attr='responsibility')
	schedule = indexes.CharField(model_attr="schedule")
	prof_roles = indexes.CharField(model_attr="prof_roles")
	experience = indexes.CharField(model_attr="experience")
	url = indexes.CharField(model_attr="url")
	description = indexes.CharField(model_attr="description")
	languages = indexes.CharField(model_attr="languages")

	class Meta: 
		model = Job
		fields = 'hh_id, name, city, street, requirements, responsibility, schedule, prof_roles, experience, url, description, languages'.split(', ')
	
	def get_model(self):
		return Job

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.all()