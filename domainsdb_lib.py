

import requests, json
from urllib.parse import urlencode

domainsdb_v1_api = "https://api.domainsdb.info/v1/"


def query_domainsdb_domains (query_dict):
	"""
		Query https://domainsdb.info with a GET request to the end_point
		using the query information in the query_dict argument.

		Supported key-value pairs include (all values are converted to str):

			api_key:	API key to use.
			domain:		contained in the domain name
			zone:		zone to search in, such as com, info, biz
			country:	Hosting country
			isDead:		Include domains that are dead, or not.
						Not setting this parameter gathers both,
						with two requests
			limit:		Number of domains per page, defaults to 250

		Not yet implemented key-values, available by domainsdb.info's API:
			A, NS, CNAME, MX, TXT: value would be included in the cooresponding record.

		**NOTE**
				Without an api_key, the API only allows the first 50 results, or 100
				if isDead is not set, as we then get two queries.
	"""
	also_check_dead = False
	if ("isDead" not in query_dict.keys ()):
		query_dict['isDead'] = 0
		also_check_dead = True

	if ("limit" not in query_dict.keys ()):
		query_dict['limit'] = 250

	no_api_key = False
	if ("api_key" not in query_dict.keys ()):
		no_api_key = True

	query_string = urlencode (query_dict)
	records = []

	records_received = query_dict['limit']
	while (records_received == query_dict['limit']):
		get_r = requests.get (domainsdb_v1_api + "domains/search" + "?" + query_string)
		if (get_r.status_code == 200):
			data_r = json.loads (get_r.text)
			records += data_r['domains']
			records_received = len (data_r['domains'])
		elif (get_r.status_code == 404):
			records += [] # to not skip no_api_key check
		else:
			return [get_r.status_code, get_r]
		if (no_api_key): 
			break

	if (also_check_dead): # This code block is ideally set into a function, to remove duplicate code.
		query_dict['isDead'] = 1
		query_string = urlencode (query_dict)

		records_received = query_dict['limit']
		while (records_received == query_dict['limit']):
			get_r = requests.get (domainsdb_v1_api + "domains/search" + "?" + query_string)
			if (get_r.status_code == 200):
				data_r = json.loads (get_r.text)
				records += data_r['domains']
				records_received = len (data_r['domains'])
			elif (get_r.status_code == 404):
				records += [] # to not skip no_api_key check
			else:
				return [get_r.status_code, get_r]
			if (no_api_key): 
				break
	return [200, records]

