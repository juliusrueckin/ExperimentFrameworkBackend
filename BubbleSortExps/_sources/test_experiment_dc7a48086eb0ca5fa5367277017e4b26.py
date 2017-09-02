from sacred import Experiment
from bubblesort_ingredient import data_ingredient, load_data

import random
import csv
import numpy as np

ex = Experiment('Bubble Sort', ingredients=[data_ingredient])

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

def doThingsAfterTermination(outputArray, csvFormat):
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

	# use give command param as input data file
	inputData = params[0]["value"]

	# use ingredient dataset as a default input data file
	#inputData = load_data()

	sortedArray = sortArray(inputData)

	outputArray = [param["value"] for param in params]
	outputArray.append(sortedArray)

	doThingsAfterTermination(outputArray, csvFormat)