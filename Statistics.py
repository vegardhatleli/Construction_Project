import statistics
import Project as p
import numpy as np

def randomSampleOfDurations(riskfactor, project):
    durations = []
    for i in range (1000):
        durations.append(round(project.setEarlyDatesRandom(riskfactor),2))
    return durations


def sampleDurationCalculator(data):
    minValue = min(data)
    maxValue = max(data)
    meanValue = statistics.mean(data)
    standardDeviation = statistics.stdev(data)
    decile = np.percentile(data, np.arange(0,100,10))
    numberOfSuccessful = 0
    numberOfAcceptable = 0
    numberOfFailed = 0
    for time in data:
        if time <= 371 * 1.05:
            numberOfSuccessful += 1
        if time > 371 * 1.05 and time <= 371 * 1.15:
            numberOfAcceptable += 1
        if time > 371 * 1.15:
            numberOfFailed += 1
    return minValue,maxValue, meanValue,standardDeviation, decile, numberOfSuccessful, numberOfAcceptable, numberOfFailed

def sampleDurationTable(data):
    print(data)
    with open('Task4/sampleDurationTableRisk1.4.txt', 'w') as file:
        file.write(f"Minimum:            {data[0]}\n")
        file.write(f"Maximum:            {data[1]}\n")
        file.write(f"Mean:               {data[2]}\n")
        file.write(f"Standard Deviation: {data[3]}\n\n")
        for i in range(9):
            file.write(f"Decile{i+1}:            {data[4][i]}\n")
        file.write(f"Decile10:           {data[4][9]}\n\n")
        file.write(f"Sucsessful:         {data[5]}\n")
        file.write(f"Acceptable:         {data[6]}\n")
        file.write(f"Failed:             {data[7]}\n")


def runStatistics():
    villa = p.Project([], 'Villa')
    villa.loadProjectFromExcel(
        'Data/Villa copy 2.xlsx')
    villa.createPertDiagram()
    #Run the riskfactor you want (0.8, 1.0, 1.2, 1.4)
    #Remember to change the name of the write to file if you want to display data
    #alldata = randomSampleOfDurations(1.4, villa)
    #stats = sampleDurationCalculator(alldata)
    #sampleDurationTable(stats)

#runStatistics()