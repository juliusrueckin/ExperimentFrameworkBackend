from sacred import Experiment
import random
import csv
import numpy as np
import requests

ex = Experiment()

def send_slack_message(data):
        requests.post(self.webhook, headers={'Content-type': 'application/json'}, data=data)

def exportToCSV(output, csvFormat):
	with open('ouput.csv', 'w') as csvfile:
	    fieldnames = list(csvFormat)
	    print(fieldnames)
	    writer = csv.writer(csvfile, delimiter=',', quotechar='"')

	    writer.writerow(fieldnames)
	    for dataset in output:
	    	writer.writerow(dataset)

def prettyPrintOutputToTerminal(output):
	print(output)

def doThingsAfterTermination(outputArray):
	prettyPrintOutputToTerminal(outputArray)
	exportToCSV([outputArray], csvFormat)

def sortArray(inputArray):
	for i in range(0, len(inputArray)):
		for j in range(0, len(inputArray) - i - 1):
			if inputArray[j] > inputArray[j+1]:
				tmp = inputArray[j+1]
				inputArray[j+1] = inputArray[j]
				inputArray[j] = tmp

	return inputArray

@ex.named_config
def bubbleSortConfig():
    
    title = "Bubble Sort"
    params = [{"name": "unsortedArray", "value": random.sample(range(100), 10)}]

@ex.main
@ex.capture
def bubbleSort(params, csvFormat, title):
	print("Experiment: " + title + "\n")
	sortedArray = sortArray(params[0]["value"])
	outputArray = [param["value"] for param in params]
	outputArray.append(sortedArray)

	doThingsAfterTermination(outputArray)