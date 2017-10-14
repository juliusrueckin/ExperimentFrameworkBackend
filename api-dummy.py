from bottle import request, response
from bottle import post, get, put, delete
import re, json 

namepattern = re.compile(r'^[a-zA-Z\d]{1,64}$')
_names = set(["Julius"])

@post('/names')
def creation_handler():
	'''Handles name creation'''
	try:
		# parse input data
		try:
			data = request.json
		except:
			raise ValueError

		if data is None:
			raise ValueError

		# extract and validate name
		try:
			if namepattern.match(data['name']) is None:
				raise ValueError
			name = data['name']
		except (TypeError, KeyError):
			raise ValueError

		# check for existence
		if name in _names:
			raise KeyError

	except ValueError:
		# if bad request data, return 400 Bad Request
		response.status = 400
		return

	except KeyError:
		# if name already exists, return 409 Conflict
		response.status = 409
		return

	# add name
	_names.add(name)

	# return 200 Success
	response.headers['Content-Type'] = 'application/json'
	return json.dumps({'name': name})

@get('/names')
def listing_handler():
    '''Handles name listing'''
    
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'names': list(_names)})

@put('/names/<oldname>')
def update_handler(oldname):
    '''Handles name updates'''

    try:
        # parse input data
        try:
        	data = json.loads(request.body.read().decode("utf-8"))
        except:
            raise ValueError

        # extract and validate new name
        try:
            if namepattern.match(data['name']) is None:
                raise ValueError
            newname = data['name']
        except(TypeError, KeyError):
            raise ValueError

        # check if updated name exists
        if oldname not in _names:
            raise KeyError(404)

        # check if new name exists
        if newname in _names:
            raise KeyError(409)

    except ValueError:
        response.status = 400
        return
    except KeyError as e:
        response.status = e.args[0]
        return

    # add new name and remove old name
    _names.remove(oldname)
    _names.add(newname)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'name': newname})

@delete('/names/<name>')
def delete_handler(name):
    '''Handles name deletions'''

    try:
        # Check if name exists
        if name not in _names:
            raise KeyError
    except KeyError:
        response.status = 404
        return

    # Remove name
    _names.remove(name)
    return