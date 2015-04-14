import requests
from datetime import datetime

def get(pv, start_time, end_time):
	base_url = 'http://facet-archapp.slac.stanford.edu/retrieval/data/getData.json'
	time_format = "%Y-%m-%dT%H:%M:%S.000Z" #This assumes the dates are supplied in UTC.
	response = requests.get(base_url, { 'pv': pv, 'from': start_time.strftime(time_format), 'to': end_time.strftime(time_format) })
	return response.json()
	
def get_mean_and_std(pv, start_time, end_time):
	data = get(pv, start_time, end_time)
	sum = 0
	count = len(data[0]['data'])
	for datapoint in data[0]['data']:
		sum = sum + datapoint['val']
	average = sum / count
	std = 0
	for datapoint in data[0]['data']:
		std = std + (datapoint['val'] - average)**2
	std = sqrt(std/count)
	return (average, std)