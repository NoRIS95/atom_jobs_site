from django.core.management.base import BaseCommand, CommandError

import requests
import json
import time
import os, sys
import math
import pickle
from jobs.models import Job
import django

def check_existence_key(structure, key_name):
	if structure[key_name] is not None:
		return structure[key_name]
	return ' '

EMPLOYER_ID = 5912977

def getVacations(employer_id=5912977, request_pause_seconds=0.33):
	url = 'https://api.hh.ru/vacancies'
	params = {'employer_id': employer_id}
	response = requests.get(url, params)
	response.raise_for_status()
	data = response.json()
	###
	vacations = []
	found = data['found']
	###
	per_page = data['per_page']
	pages = math.ceil(found/per_page)
	time.sleep(request_pause_seconds)
	for i in range(pages + 1):
		params = {'page': i, "per_page": per_page, 'employer_id': employer_id}
		response = requests.get(url, params=params)
		response.raise_for_status()
		data = response.json()
		for vacation in data['items']:
			if vacation['type']['id'] == 'open' and vacation['archived'] == False:
				vac_id = check_existence_key(vacation, 'id')
				vac_name = check_existence_key(vacation, 'name')
				vac_address = check_existence_key(vacation, 'address')
				profes_roles = []
				vac_city = ' '
				vac_street = ' '
				schedule = ' '
				experience = ' '
				description = ' '
				if vac_address != ' ':
					vac_street = check_existence_key(vac_address, 'street')
					vac_city = check_existence_key(vac_address, 'city')
				snippet = check_existence_key(vacation, 'snippet')
				if snippet != ' ':
					requirements = check_existence_key(snippet, 'requirement')
					responsibility = check_existence_key(snippet, 'responsibility')
				schedule_info = check_existence_key(vacation, 'schedule')
				if schedule_info != ' ':
					schedule = check_existence_key(schedule_info, 'id')
					prof_roles = check_existence_key(vacation, 'professional_roles')
					if prof_roles != ' ':
						for role in prof_roles:
							role_name = check_existence_key(role, 'name')
							if role_name != ' ':
								profes_roles.append(role_name)
					exp_info = check_existence_key(vacation, 'experience')
					if exp_info != ' ':
						experience = check_existence_key(exp_info, 'name')
					url_hh = check_existence_key(vacation, 'alternate_url')
					url_desc = check_existence_key(vacation, 'url')
					if url_desc != ' ':
						response_desc = requests.get(url_desc)
						response_desc.raise_for_status()
						data_desc = response_desc.json()
						languages = {}
						description = check_existence_key(data_desc, 'description')
						langs = check_existence_key(data_desc, 'languages')
						if langs != ' ':
							for i in langs:
								lan_info = check_existence_key(i, 'name')
								if lan_info != ' ':
									languages[lan_info] = ' '
									lan_lev_info = check_existence_key(i, 'level')
									if lan_lev_info != ' ':
										lev_name = check_existence_key(lan_lev_info, 'name')
										if lev_name != ' ':
											languages[lan_info] = lev_name
					###
					###
					###
				vac = Job(hh_id=vac_id, name=vac_name, city=vac_city, \
						street=vac_street, requirements=requirements, \
						responsibility=responsibility, schedule=schedule, \
						prof_roles=json.dumps(profes_roles, ensure_ascii=False),
						experience=experience, \
						url=url_hh, description=description, \
						languages=json.dumps(languages, ensure_ascii=False)
						)
				vacations.append(vac)
		time.sleep(request_pause_seconds)
	return vacations						


class Command(BaseCommand):
	help = 'Parse and save hh jobs to db'

	def handle(self, *args, **kwargs):
		parser_jobs = getVacations()
		# with open('vacations.pkl', 'wb') as f:
		# 	pickle.dump(vacations, f)
		# with open('vacations.pkl', 'rb') as f:
		# 	parser_jobs = pickle.load(f)
		db_jobs = Job.objects.all()
		db_job_ids = {job.hh_id for job in db_jobs}
		parser_job_ids = {job.hh_id for job in parser_jobs}

		jobs_to_remove = [job for job in db_jobs if job.hh_id not in parser_job_ids] # вакансии, которых уже нет на HH
		jobs_to_add = [job for job in parser_jobs if job.hh_id not in db_job_ids] # вакансии, которых нет в базе
		# TODO хорошо бы ещё остальные вакансии из базы обновлять в соотвествии с их актуальным описанием на hh
		for job in jobs_to_remove:
			job.delete()

		for job in jobs_to_add:
			job.save()