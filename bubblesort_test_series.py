from test_experiment import ex, setRepetitionNumber

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

class BubbleSortExpSeries():
   	
	def forceKill(timeoutObsInst):
		pid = os.getpid()
		p = psutil.Process(pid)
		p.kill()


	def addObservers(self, slack_obs_file, telegram_obs_file, mail_obs_file, timeout_obs_file):
		ex.observers.append(MongoObserver.create(url='127.0.0.1:27017', db_name='BubbleSortExp'))
		ex.observers.append(FileStorageObserver.create('BubbleSortExps'))

		slack_obs = SlackObserver.from_config(slack_obs_file)
		ex.observers.append(slack_obs)

		telegram_obs = TelegramObserver.from_config(telegram_obs_file, os.getpid())
		ex.observers.append(telegram_obs)

		telegram_utilization_bot = UtilizationBot.from_config(telegram_obs_file, os.getpid())

		mail_obs = MailObserver.from_config(mail_obs_file, self.repetitions)
		ex.observers.append(mail_obs)

		timeout_obs = TimeoutObserver.from_config(timeout_obs_file, self)
		ex.observers.append(timeout_obs)


	def startExperimentSeries(self):
		for i in range(1, self.repetitions + 1):
				print(str(i) + ". Durchlauf")
				setRepetitionNumber(i)
				r = ex.run(named_configs=[self.confSrc])
				#print("\nÁllgemeiner Versuchsaufbau\n")
				#print(r.experiment_info)
				#print(r.host_info)
				print("---------------------------------------------------")


	def __init__(self, repetitions, confSrc='testConfig/bubbleSortConfigFile.json', slack_obs_file='testConfig/slack.json', telegram_obs_file='testConfig/telegram.json', mail_obs_file='testConfig/mail.json', timeout_obs_file='testConfig/timeout.json'):
		self.confSrc = confSrc
		self.repetitions = repetitions

		ex.captured_out_filter = apply_backspaces_and_linefeeds

		self.addObservers(slack_obs_file, telegram_obs_file, mail_obs_file, timeout_obs_file)
		self.startExperimentSeries()


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--repetitions", type=int, default=1, help="Defines how many iterations of this experiment will be performed")
	parser.add_argument("--configPath", type=str, default="config.json" ,help="Path to experiment's config file (.json-file required)")
	

	args = parser.parse_args()

	confSrc = "bubbleSortConfig"
	repetitions = 1

	if len(sys.argv) > 1:
		repetitions = args.repetitions

	if len(sys.argv) > 2:
		confSrc = args.configPath

	#confSrc = "bubbleSortConfig"
	
	BubbleSortExpSeries(repetitions, confSrc)