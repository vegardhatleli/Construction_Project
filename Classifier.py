import Project as p
import Task
import random as rd
## CLASSIFIER

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
    trainingInstances = []
    labels = []
    for project in projects:
        trainInstance, label = prepareProjectForLearninig(project)
        trainingInstances.append(trainInstance)
        labels.append(label)
    return trainingInstances, labels

def createSampleData():
    listOfProjects = []
    for i in range(1000):
        warehouse = p.Project([], f'Warehouse{i}')
        warehouse.loadProjectFromExcel(
            'Data/Villa copy.xlsx')
        factors = [0.8 , 1.0, 1.2, 1.4]
        warehouse.setEarlyDatesRandom(factors[rd.randint(0,3)])
        warehouse.setLateDatesRandom()
        listOfProjects.append(warehouse)
    return listOfProjects

projects = createSampleData()
trainingInstances, labels = prepareDataForLearning(projects)
print(len(trainingInstances))
print(len(labels))
print(labels)
