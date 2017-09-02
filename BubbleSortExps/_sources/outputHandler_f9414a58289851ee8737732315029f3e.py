import csv

def prettyPrintOutputToTerminal(output):
	print(output)	

def exportInCSVFile(csvfile, data, fields):
	with open(csvfile, 'w') as csvfile:
	    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
	    row_headers = list(fields)
	    writer.writerow(row_headers)
	 
	    for dataset in data:
	        row = [attr_value for attr_value in dataset]
	        writer.writerow(row)