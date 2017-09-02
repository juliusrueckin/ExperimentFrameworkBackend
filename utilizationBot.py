import os
import psutil
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from sacred.config.config_files import load_config_file

class UtilizationAnalyser():

    def memory_usage_psutil(self):
        process = psutil.Process(self.obsProcID)
        mem = process.memory_percent()
        return mem

    def cpu_usage_psutil(self):
        process = psutil.Process(self.obsProcID)
        cpu = psutil.cpu_percent()
        return cpu

    def __init__(self, obsProcID):
    	self.obsProcID = obsProcID

class UtilizationBot():

	@classmethod
	def from_config(cls, filename, obsProcId):
		d = load_config_file(filename)
		obs = None
		if 'token' in d and 'chat_id' in d:
			obs = cls(d['token'],obsProcId)
		else:
		    raise ValueError("Telegram configuration file must contain "
		                     "entries for 'token' and 'chat_id'!")

		return obs

	def getUtilization(self, bot, update):
		bot.send_message(chat_id=update.message.chat_id, text="CPU-Utilization: " + str(self.utilizationAnalyser.cpu_usage_psutil()) + "%\nMemory-Utilization: " + str(self.utilizationAnalyser.memory_usage_psutil()) + "%")

	def __init__(self, token, obsProcID):
		self.utilizationAnalyser = UtilizationAnalyser(obsProcID)
		self.token = token

		self.updater = Updater(token=self.token)
		self.dispatcher = self.updater.dispatcher

		logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

		utilization_handler = CommandHandler('getUtilization', self.getUtilization)
		self.dispatcher.add_handler(utilization_handler)

		self.updater.start_polling()