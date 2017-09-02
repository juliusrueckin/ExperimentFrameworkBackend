import bottle
from bottle import route, run, request, template, static_file, post, get
from bubblesort_test_series import BubbleSortExpSeries
import os
import json
import shutil

base_path = os.path.abspath(os.path.dirname(__file__))
view_path = os.path.join(base_path, 'views')
bottle.TEMPLATE_PATH.insert(0, view_path)

@route('/')
@route('/index')
@route('/home')
def home(name='World'):
    return template('index')

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=os.path.join(base_path, 'static'))


@post('/createFiles')
def do_createFiles():
    exp_repetitions = 3

    basicConf = request.params.get('basicConfObj')
    basicConfJSON = json.loads(basicConf)

    conf_dir = basicConfJSON['title'] + 'Configs'
    config_path = os.path.join(base_path, conf_dir)

    basicConfPath = config_path + '/basicConfFile.json'

    timeoutConf = request.params.get('timeoutConfObj')
    timeoutConfJSON = json.loads(timeoutConf)
    timeoutConfPath = config_path + '/timeoutConfFile.json'

    slackNotifierConf = request.params.get('slackNotifierConfObj')
    slackNotifierConfJSON = json.loads(slackNotifierConf)
    slackNotifierConfPath = config_path + '/slackNotifierConfFile.json'

    mailNotifierConf = request.params.get('mailNotifierConfObj')
    mailNotifierConfJSON = json.loads(mailNotifierConf)
    mailNotifierConfPath = config_path + '/mailNotifierConfFile.json'

    telegramNotifierConf = request.params.get('telegramNotifierConfObj')
    telegramNotifierConfJSON = json.loads(telegramNotifierConf)
    telegramNotifierConfPath = config_path + '/telegramNotifierConfFile.json'

    if not os.path.exists(config_path):
        os.makedirs(config_path)

    with open(basicConfPath, 'w+') as outfile:
    	outfile.write(str(basicConf))

    with open(timeoutConfPath, 'w+') as outfile:
    	outfile.write(str(timeoutConf))

    with open(slackNotifierConfPath, 'w+') as outfile:
    	outfile.write(str(slackNotifierConf))

    with open(telegramNotifierConfPath, 'w+') as outfile:
    	outfile.write(str(telegramNotifierConf))

    with open(mailNotifierConfPath, 'w+') as outfile:
    	outfile.write(str(mailNotifierConf))

    #BubbleSortExpSeries(exp_repetitions, basicConfPath, slackNotifierConfPath, telegramNotifierConfPath, mailNotifierConfPath, timeoutConfPath)

    return "Created JSON-Config-Files successfully!"


run(host='localhost', port=8080, debug=True)