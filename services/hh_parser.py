import requests
import json
import time
import os, os.path
import math
import pandas as pd
from dataclasses import dataclass
from whoosh import index
from whoosh.fields import Schema, ID, TEXT



@dataclass
class Vacation:
	id: str
	name: str
	city: str
	street: str
	requirements: str
	responsibility: str
	schedule: str
	prof_roles: list
	experience: str
	url: str
	desc_vac: str
	language_dict: dict



def check_existence_key(structure, key_name):
	if structure[key_name] is not None:
		return structure[key_name]
	return ' '

def getVacations(employer_id=5912977, pause=0.33):
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
	time.sleep(pause)
	for i in range(pages + 1):
		params = {'page': i, "per_page": per_page, 'employer_id': employer_id}
		response = requests.get(url, params=params)
		response.raise_for_status()
		data = response.json()
		for vacation in data['items']:
			if vacation['type']['id'] == 'open' and vacation['archived'] == False:
				vac_id = check_existence_key(vacation, 'id')
				vac_name = check_existence_key(vacation, 'id')
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
				vac = Vacation(id=vac_id, name=vac_name, city=vac_city, \
						street=vac_street, requirements=requirements, \
						responsibility=responsibility, schedule=schedule, \
						prof_roles=profes_roles, experience=experience, \
						url=url_hh, desc_vac=description, \
						language_dict=languages
						)
				time.sleep(pause)
				vacations.append(vac)
	return vacations						


if __name__ == '__main__':
	if not os.path.exists('indexdir'):
		os.mkdir('indexdir')
		schema = Schema(id = ID(unique=True), name=TEXT, city=TEXT, \
			street=TEXT, requirements=TEXT, responsibility=TEXT, \
			schedule=TEXT, prof_roles=TEXT, experience=TEXT,\
			url=TEXT, desc_vac=TEXT, language_dict=TEXT)
		ix = index.create_in('indexdir', schema)
	vacations = getVacations()
	# print(vacations)
	ix = index.open_dir('indexdir')
	for vacation in vacations:
		print(vacation)
		writer = ix.writer()
		languages = vacation.language_dict
		str_languages = json.dumps(languages, ensure_ascii=False)
		prof_roles = vacation.prof_roles
		str_prof_roles = json.dumps(prof_roles, ensure_ascii=False)
		experience = vacation.experience
		vac_id = vacation.id
		vac_name = vacation.name
		city = vacation.city
		street = vacation.street
		requirements = vacation.requirements
		responsibility = vacation.responsibility
		schedule = vacation.schedule
		url = vacation.url
		desc_vac = vacation.desc_vac
		writer.add_document(name=vac_name, id=vac_id, city=city, \
			street=street, requirements=requirements, responsibility=responsibility, \
			schedule=schedule, prof_roles=str_prof_roles, experience=experience, \
			url=url, desc_vac=desc_vac, language_dict=str_languages)
	writer.commit()