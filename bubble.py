import random

def bubble(inputArray):
	x = 1

	error = 100
	errorImprovement = 7
	errorFunctionTest = False

	accuracy = 0
	accuracyImprovement = 6
	accuracyFunctionTest = True

	for i in range(0, len(inputArray)):
		for j in range(0, len(inputArray)-1):
			if i * len(inputArray) >= ((len(inputArray)**2) * (x/5)):
				print("Algorithm still working fine")
				x += 1

				if errorFunctionTest:
					error = error - errorImprovement
					errorImprovement = errorImprovement - 1
					print("Loss function: " + str(error))

				if accuracyFunctionTest:
					accuracy = accuracy + accuracyImprovement
					accuracyImprovement = accuracyImprovement - 1
					print("Accuracy function: " + str(accuracy))

			if inputArray[j] > inputArray[j+1]:
				tmp = inputArray[j+1]
				inputArray[j+1] = inputArray[j]
				inputArray[j] = tmp

	return [inputArray]

if __name__ == "__main__":

	inputArray = random.sample(range(1000000), 1000)

	#if len(sys.argv) > 1:
	#	inputArray = sys.argv[1]

	print(bubble(inputArray))