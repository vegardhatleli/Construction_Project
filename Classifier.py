from cgi import test
import Project as p
import Task
import random as rd
import sys
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
import numpy as np


## CLASSIFIER

def PrintConfusionMatrix(labels, actualLabels, predictedLabels, output):
    numberOfLabels = len(labels)
    counts = [[0 for _ in range(0, numberOfLabels)]
              for _ in range(0, numberOfLabels)]
    for i in range(0, len(actualLabels)):
        counts[int(actualLabels[i])][int(predictedLabels[i])] += 1
    for column in range(0, numberOfLabels):
        output.write("\t{0:s}".format(labels[column]))
    output.write("\n")
    for row in range(0, numberOfLabels):
        output.write("{0:s}".format(labels[row]))
        for column in range(0, numberOfLabels):
            output.write("\t{0:d}".format(counts[row][column]))
        output.write("\n")



def prepareProjectForLearninig(project):
    trainingInstances = []
    for task in project.getTasks():
        if task.getTaskID() == 'Gate':
            break
        trainingInstances.append(task.getEarlyCompleationDate())
    earlyCompletionDate = project.getMinimumProjectDuration()
    if earlyCompletionDate <= 371 * 1.05:
        label = 0
    if earlyCompletionDate > 371 * 1.05 and earlyCompletionDate <= 371 * 1.15:
        label = 1
    if earlyCompletionDate > 371 * 1.15:
        label = 2
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

def calculatePredictionResults(testlabels, predictedLabels):
    class_names = ['Success', 'Acceptable', 'Failure']
    f = open("Task5/KNeighborsClassifier.out", "w")
    sys.stdout = f
    cm = confusion_matrix(testlabels,predictedLabels)
    accuracy = ((cm[0][0] + cm[1][1] + cm[2][2])/200) * 100
    print('Confusion Matrix and Accuracy with KNeighborsClassifier: \n')
    print('             Success    Acceptable    Failure')
    print('---------------------------------------------')
    for i in range(len(cm)):
        row_str = class_names[i] + ' ' * (13 - len(class_names[i]))
        for j in range(len(cm)):
            row_str += '{:12d}'.format(cm[i][j])
        print(row_str)
    print('\n')
    print(f'Accuracy: {accuracy}%')

def runClassifier():
    projects = createSampleData()
    model1 = DecisionTreeClassifier()
    model2 = svm.SVC()
    model3 = KNeighborsClassifier()
    trainingInstances, trainingLabels, testInstances, testLabels = prepareDataForLearning(projects)

    #Run the model you want (model1, model2, model3)
    #Remember to change the name of the write to file if you want to display data
    model3.fit(trainingInstances, trainingLabels)
    predictedLabels = model3.predict(testInstances)
    #calculatePredictionResults(testLabels,predictedLabels)
