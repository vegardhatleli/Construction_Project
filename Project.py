from Task import *
import pandas as pd
from graphviz import Digraph
import statistics
import numpy as np

class Project:

    def __init__(self, tasks, projectID):
        self.projectID = projectID
        self.tasks = tasks

    def getTasks(self):
        return self.tasks

    def taskSearch(self, taskID):
        for task in self.getTasks():
            if str(taskID) == str(task.getTaskID()):
                return task

    def setTasks(self, tasks):
        self.tasks = tasks

    def addTask(self, task):
        self.tasks.append(task)

    def setEarlyDates(self):
        remainingTasks = self.getTasks().copy()
        while len(remainingTasks) > 0:
            for task in remainingTasks:
                if not set(task.getPredecessors()).intersection(set(remainingTasks)):
                    if len(task.getPredecessors()) == 0:
                        task.setEarlyStartDate(0)
                        task.setEarlyCompleationDate(0)
                        remainingTasks.remove(task)
                    else:
                        latestCompleationDateTask = max(
                            task.getPredecessors(), key=lambda x: x.getEarlyCompleationDate())
                        task.setEarlyStartDate(
                            latestCompleationDateTask.getEarlyCompleationDate())

                        task.setEarlyCompleationDate(
                            int(task.getEarlyStartDate()) + int(task.getExpectedDuration()))

                        remainingTasks.remove(task)
        print('Early dates is set')
        return

    def getMinimumProjectDuration(self):
        task = max(self.getTasks(), key=lambda x: x.getEarlyCompleationDate())
        return task.getEarlyCompleationDate()

    def setLateDates(self):
        remainingTasks = self.getTasks().copy()
        while len(remainingTasks) > 0:
            for task in remainingTasks:
                if not set(task.getSuccessors()).intersection(set(remainingTasks)):
                    if len(task.getSuccessors()) == 0:
                        task.setLateStartDate(self.getMinimumProjectDuration())
                        task.setLateCompleationDate(
                            self.getMinimumProjectDuration())
                        remainingTasks.remove(task)
                    else:
                        maxLateStartDate = min(
                            task.getSuccessors(), key=lambda x: x.getLateStartDate())

                        task.setLateCompleationDate(
                            maxLateStartDate.getLateStartDate())

                        task.setLateStartDate(
                            task.getLateCompleationDate() - task.getExpectedDuration())

                        remainingTasks.remove(task)
        print('Late Date is set')

    def printProjectToExcel(self):
        headers = ['Task', 'Predecessor', 'Succsessor', 'Duration', 'Description', 'Early Start Date',
                   'Early Completion Date', 'Late Start Date', 'Late Completion Date', 'Critcal Task?']
        data = []
        for task in self.getTasks():
            values = [task.getTaskID(), [p.getTaskID() for p in task.getPredecessors()], [p.getTaskID() for p in task.getSuccessors()], task.getRandomDuration(
            ), task.getDescription(), task.getEarlyStartDate(), task.getEarlyCompleationDate(), task.getLateStartDate(), task.getLateCompleationDate(), task.getCritical()]
            data.append(values)

        df = pd.DataFrame(data, columns=headers)

        with pd.ExcelWriter('Results/VillaTestEcpe.xlsx') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

    def loadProjectFromExcel(self, filepath):
        df = pd.read_excel(filepath)

        for index, row in df.iterrows():
            if row.isnull().all():
                continue
            type = row['Types']
            taskID = row['Codes']
            description = row['Descriptions']
            durations = str(row['Durations'])
            predecessors = str(row['Predecessors'])

            predecessors = predecessors.split()
            predecessors = [s.replace(',', '') for s in predecessors]

            if (durations == 'nan'):
                durations = '(0,0,0)'

            durations = eval(durations)
            durations = list(durations)

            task = Task(taskID, durations, description)

            if (task.getTaskID() != 'Start'):
                for predess in predecessors:
                    predessesor = self.taskSearch(predess)
                    task.addPredecessor(predessesor)

            self.addTask(task)
        print('Load from Excel finish')
        return


    def createPertDiagram(self):
        dot = Digraph(comment='PERT Diagram')
        dot.attr(rankdir='LR') 
        for task in self.tasks:
            dot.node(task.getTaskID(), shape='box')
            for successor in task.getSuccessors():
                dot.edge(task.getTaskID(), successor.getTaskID())
        dot.render('pert', view=True)

# Task 4

    def setEarlyDatesRandom(self, riskFactor):
        for task in self.getTasks():
            task.setRandomDuration(riskFactor)
        remainingTasks = self.getTasks().copy()
        while len(remainingTasks) > 0:
            for task in remainingTasks:
                if not set(task.getPredecessors()).intersection(set(remainingTasks)):
                    if len(task.getPredecessors()) == 0:
                        task.setEarlyStartDate(0)
                        task.setEarlyCompleationDate(0)
                        remainingTasks.remove(task)
                    else:
                        latestCompleationDateTask = max(
                            task.getPredecessors(), key=lambda x: x.getEarlyCompleationDate())
                        task.setEarlyStartDate(
                            latestCompleationDateTask.getEarlyCompleationDate())

                        task.setEarlyCompleationDate(
                            task.getEarlyStartDate() + task.getRandomDuration())

                        remainingTasks.remove(task)
        print('Early dates is set')
        return self.getMinimumProjectDuration()

    def setLateDatesRandom(self):
        remainingTasks = self.getTasks().copy()
        while len(remainingTasks) > 0:
            for task in remainingTasks:
                if not set(task.getSuccessors()).intersection(set(remainingTasks)):
                    if len(task.getSuccessors()) == 0:
                        task.setLateStartDate(self.getMinimumProjectDuration())
                        task.setLateCompleationDate(
                            self.getMinimumProjectDuration())
                        remainingTasks.remove(task)
                    else:
                        maxLateStartDate = min(
                            task.getSuccessors(), key=lambda x: x.getLateStartDate())

                        task.setLateCompleationDate(
                            maxLateStartDate.getLateStartDate())

                        task.setLateStartDate(
                            task.getLateCompleationDate() - task.getRandomDuration())

                        remainingTasks.remove(task)
        print('Late Date is set')
        return

    def randomSampleOfDurations(self, riskfactor):
        durations = []
        for i in range (1000):
            durations.append(round(self.setEarlyDatesRandom(riskfactor),2))
        return durations


    def sampleDurationCalculator(self, data):
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

    def sampleDurationTable(self, data):
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







warehouse = Project([], 'Warehouse')
warehouse.loadProjectFromExcel(
    'Data/Villa.xlsx')

alldata = warehouse.randomSampleOfDurations(1.4)
stats = warehouse.sampleDurationCalculator(alldata)
warehouse.sampleDurationTable(stats)
#print(warehouse.sampleDurationCalculator(data))