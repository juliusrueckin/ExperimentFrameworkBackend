from sacred import Experiment
from bubblesort_ingredient import data_ingredient, load_data
from operator import attrgetter

import random
import csv
import numpy as np

ex = Experiment('Bubble Sort', ingredients=[data_ingredient])
 
def exportInCSVFile(csvfile, objects, fields):
	with open(csvfile, 'w') as csvfile:
	    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
	    row_headers = list(fields)
	    writer.writerow(row_headers)
	 
	    for obj in objects:
	        row = [attrgetter(header)(obj) for header in row_headers]
	        for count, column in enumerate(row):
	            if callable(column):
	                row[count] = column()
	            if type(column) is unicode:
	                row[count] = column.encode('utf8')
	        writer.writerow(row)

def prettyPrintOutputToTerminal(output):
	print(output)

def doThingsAfterTermination(outputArray, csvFields, csvFilename):
	prettyPrintOutputToTerminal(outputArray)

	if csvFields != "" and csvFilename != "":
		filename = csvFilename + '.csv'
		exportInCSVFile(filename, [outputArray], csvFields)

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
    
    title = "Bubble Sort Experiment"
    params = [{"name": "unsortedArray", "value": random.sample(range(1000000), 100000)}]
    csvFields = ["unsortedArray", "chaosMeasure", "sortedArray"]
    csvFilename = "output"

@ex.main
@ex.capture
def bubbleSort(params, csvFields, title, csvFilename):
	print("Experiment: " + title + "\n")

	# use given command param as input data file
	inputData = params[0]["value"]

	# use ingredient dataset as a default input data file
	#inputData = load_data()

	sortedArray = sortArray(inputData)

	outputArray = [param["value"] for param in params]
	outputArray.append(sortedArray)

	doThingsAfterTermination(outputArray, csvFields, csvFilename)