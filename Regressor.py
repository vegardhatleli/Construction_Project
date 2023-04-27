import random as rd
import Project as p
import sys
import math
from sklearn import metrics
from sklearn.svm import SVR
from sklearn import tree
from sklearn.neighbors import KNeighborsRegressor


def prepareProjectForLearninig(project):
    trainingInstances = []
    for task in project.getTasks():
        if task.getTaskID() == 'Gate':
            break
        trainingInstances.append(task.getEarlyCompleationDate())
    label = project.getMinimumProjectDuration()
    return trainingInstances, label

def prepareDataForLearning(projects):
    allInstances = []
    allLabels = []
    for project in projects:
        Instance, label = prepareProjectForLearninig(project)
        allInstances.append(Instance)
        allLabels.append(label)
    split_index = int(len(allInstances) * 0.8)
    trainingInstances = allInstances[:split_index]
    trainingLabels = allLabels[:split_index]
    testInstances = allInstances[split_index:]
    testLabels = allLabels[split_index:]
    return trainingInstances, trainingLabels, testInstances, testLabels

def createSampleData():
    listOfProjects = []
    for i in range(1000):
        villa = p.Project([], f'Villa{i}')
        villa.loadProjectFromExcel(
            'Data/Villa copy.xlsx')
        factors = [0.8 , 1.0, 1.2, 1.4]
        villa.setEarlyDatesRandom(factors[rd.randint(0,3)])
        villa.setLateDatesRandom()
        listOfProjects.append(villa)
    return listOfProjects


def calculatePredictionResults(actualDuration, predictedDuration):
    with open('Task6/KNeighborsRegressor.txt', 'w') as file:
        file.write('## K-Neighbors Regression ## \n')
        file.write("Actual duration\tPredicted duration\n")
        for i in range(0, len(actualDuration)):
            file.write("{0:g}\t\t\t{1:g}".format(actualDuration[i], round(predictedDuration[i], 0)))
            file.write('\n')
        file.write('\n')
        file.write('RESULT\n')
        file.write("Mean Absolute Error\t{0:g}\n".format(metrics.mean_absolute_error(actualDuration, predictedDuration)))
        file.write("Root Mean Square Error\t{0:g}\n".format(math.sqrt(metrics.mean_squared_error(actualDuration, predictedDuration))))
        file.write("R^2\t{0:g}\n".format(metrics.r2_score(actualDuration, predictedDuration)))
        

def runRegressor():
    projects = createSampleData()
    trainingInstances, trainingLabels, testInstances, testLabels = prepareDataForLearning(projects)
    model1 = SVR()
    model2 = tree.DecisionTreeRegressor()
    model3 = KNeighborsRegressor()

    #Run the model you want (model1, model2, model3)
    #Remember to change the name of the write to file if you want to display data
    model3.fit(trainingInstances,trainingLabels)
    predictedLabels = model3.predict(testInstances)
    #calculatePredictionResults(testLabels,predictedLabels)

