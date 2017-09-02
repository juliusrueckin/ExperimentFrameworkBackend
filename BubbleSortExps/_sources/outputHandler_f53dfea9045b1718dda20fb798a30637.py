import csv
import os

def prettyPrintOutputToTerminal(output):
	print(output)

def csvExportWanted(csvFields, csvFilename):
	return csvFields != None and csvFilename != None and csvFilename != "" and csvFields != None

def exportInCSVFile(csvfile, data, fields):
	with open(csvfile, 'w') as csvfile:
	    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
	    row_headers = list(fields)
	    writer.writerow(row_headers)
	 
	    for dataset in data:
	        row = [attr_value for attr_value in dataset]
	        writer.writerow(row)

def generateCSVFilename(csvFilename, repNum):
	outputPath = csvFilename + 'Outputs'
	if not os.path.exists(outputPath):
		os.makedirs(outputPath)

	return outputPath + '/' + csvFilename + '_R' + str(repNum) + '.csv'