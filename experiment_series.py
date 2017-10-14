from experiment_instance import ex, setRepetitionNumber

from sacred.observers import MongoObserver
from sacred.observers import FileStorageObserver
from sacred.observers import SlackObserver
from sacred.observers import TelegramObserver
from mail import MailObserver
from timeout import TimeoutObserver
from utilizationBot import UtilizationBot

from sacred.utils import apply_backspaces_and_linefeeds
from sacred.utils import SacredInterrupt

import sys
import psutil
import os
import argparse
import telegram
import json

class ExperimentSeries():
   	
   	#kill currently running experiment instance
	def forceKill(timeoutObsInst):
		pid = os.getpid()
		p = psutil.Process(pid)
		p.kill()

	#add observers to experiment
	def addObservers(self, slack_obs_file, telegram_obs_file, mail_obs_file, timeout_obs_file, expTitle):
		#mongodb database name depends on experiment's title
		#add mongodb observer which stores major experiment stats
		dbName = expTitle.replace(" ","") + "_DB"
		ex.observers.append(MongoObserver.create(url='127.0.0.1:27017', db_name=dbName))

		#file storage folder name depends on experiment's titles
		#add file storage observer which stores produces outputs, stored config files and execution properties 
		fileStorageFolderName = expTitle.replace(" ","") + "StoredFiles"
		ex.observers.append(FileStorageObserver.create(fileStorageFolderName))

		#add slack observer which 
		slack_obs = SlackObserver.from_config(slack_obs_file)
		ex.observers.append(slack_obs)

		telegram_obs = TelegramObserver.from_config(telegram_obs_file, os.getpid())
		ex.observers.append(telegram_obs)

		telegram_utilization_bot = UtilizationBot.from_config(telegram_obs_file, os.getpid())

		mail_obs = MailObserver.from_config(mail_obs_file, self.repetitions)
		ex.observers.append(mail_obs)

		timeout_obs = TimeoutObserver.from_config(timeout_obs_file, self)
		ex.observers.append(timeout_obs)

	#run instances of experiment, increase repe
	def startExperimentSeries(self, StatusMessagesOutputFilename):
		for i in range(1, self.repetitions+1):			
			print(str(i) + ". Flow")
			setRepetitionNumber(i)
			#remove existing old status message file
			try:
			    os.remove(StatusMessagesOutputFilename)
			except OSError:
			    pass

			#create new empty output file
			open(StatusMessagesOutputFilename, "a").close()
			r = ex.run(named_configs=[self.confSrc])
			print("---------------------------------------------------")
		self.forceKill()


	def __init__(self, repetitions, confSrc='defaultConfig/bubbleSortConfigFile.json', slack_obs_file='defaultConfig/slack.json', telegram_obs_file='defaultConfig/telegram.json', mail_obs_file='defaultConfig/mail.json', timeout_obs_file='defaultConfig/timeout.json'):
		self.confSrc = confSrc
		self.repetitions = repetitions

		ex.captured_out_filter = apply_backspaces_and_linefeeds

		#add status message output file
		expTitle = ""

		with open(confSrc) as json_config_data_file:
			config_data = json.load(json_config_data_file)

    	#output file name depending on given title in json-config file
		expTitle = config_data["title"]
		StatusMessagesOutputFilename = expTitle + "StatusMessages.txt"

		#remove existing old status message file
		try:
		    os.remove(StatusMessagesOutputFilename)
		except OSError:
		    pass

		#create new empty output file
		open(StatusMessagesOutputFilename, "a").close()

		#add observers to experiment instance
		self.addObservers(slack_obs_file, telegram_obs_file, mail_obs_file, timeout_obs_file, expTitle)

		#start experiment instances
		self.startExperimentSeries(StatusMessagesOutputFilename)


if __name__ == "__main__":
	#parse command line parameters for repetition amount and json config file
	parser = argparse.ArgumentParser()
	parser.add_argument("--repetitions", type=int, default=1, help="Defines how many iterations of this experiment will be performed")
	parser.add_argument("--configPath", type=str, default="defaultConfig/bubbleSortConfigFile.json" ,help="Path to experiment's config file (.json-file required)")
	
	args = parser.parse_args()

	confSrc = "defaultConfig/bubbleSortConfigFile.json"
	repetitions = 1

	if len(sys.argv) > 1:
		repetitions = args.repetitions

	if len(sys.argv) > 2:
		confSrc = args.configPath
	
	ExperimentSeries(repetitions, confSrc)