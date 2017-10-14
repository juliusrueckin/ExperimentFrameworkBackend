import csv
import os

def prettyPrintOutputToTerminal(output):
	print(output)

def csvExportWanted(csvFields, csvFilename):
	return csvFields != None and csvFilename != None and csvFilename != "" and csvFields != None

def exportInCSVFile(csvfile, datafile, fields):
	with open(datafile) as data:
		with open(csvfile, "w") as csvfile:
			for line in data:
				csvfile.write(line)
	'''
	structured csv export not possible, just use all output of experiment as export file
	with open(csvfile, 'w') as csvfile:
	    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
	    row_headers = list(fields)
	    writer.writerow(row_headers)
	 
	    for dataset in data:
	        row = [attr_value for attr_value in dataset]
	        writer.writerow(row)
	'''

#returns a file path to experiment's output in format of 'csvFilename'Outputs/'csvFilename'_Rx.csv where x is a repetition number of current instance
def generateCSVFilename(csvFilename, repNum):
	outputPath = csvFilename + 'Outputs'
	if not os.path.exists(outputPath):
		os.makedirs(outputPath)

	return outputPath + '/' + csvFilename + '_R' + str(repNum) + '.csv'