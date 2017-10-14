from bottle import request, response
from bottle import post, get, put, delete
import re, json
from experiment_series import ExperimentSeries

@post('/start_experiment')
def start_experiment():
	#starts new experiment series
	try:
		# parse input data
		try:
			data = request.json
			print(data)
		except:
			raise ValueError

		if data is None:
			raise ValueError

		#check whether input data includes amount of repetitions and basic config file
		if 'basicConfigFilePath' not in data.keys() or 'repetitions' not in data.keys():
			raise ValueError('config file path and amount of repetitions required as parameters')

	except ValueError:
		# if bad request data, return 400 Bad Request
		response.status = 400
		return

	except KeyError:
		# if name already exists, return 409 Conflict
		response.status = 409
		return
	
	ExperimentSeries(data['repetitions'], data['basicConfigFilePath'])
    
	# return 200 Success
	response.headers['Content-Type'] = 'application/json'
	return json.dumps({'started': True})