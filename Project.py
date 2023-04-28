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

    def printProjectToExcel(self):
        headers = ['Task', 'Predecessor', 'Succsessor', 'Duration', 'Description', 'Early Start Date',
                   'Early Completion Date', 'Late Start Date', 'Late Completion Date', 'Critcal Task?']
        data = []
        for task in self.getTasks():
            values = [task.getTaskID(), [p.getTaskID() for p in task.getPredecessors()], [p.getTaskID() for p in task.getSuccessors()], task.getRandomDuration(
            ), task.getDescription(), task.getEarlyStartDate(), task.getEarlyCompleationDate(), task.getLateStartDate(), task.getLateCompleationDate(), task.getCritical()]
            data.append(values)

        df = pd.DataFrame(data, columns=headers)

        with pd.ExcelWriter('Results/VillaWithGate.xlsx') as writer:
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
        return


    def createPertDiagram(self):
        dot = Digraph(comment='PERT Diagram')
        dot.attr(rankdir='LR') 
        for task in self.tasks:
            if task.getTaskID() == 'Gate':
                dot.node(task.getTaskID(), shape='oval',style='filled', color='red')
            else:
                dot.node(task.getTaskID(), shape='box')
            for successor in task.getSuccessors():
                dot.edge(task.getTaskID(), successor.getTaskID())
        dot.render('Task5/Diagram/PertDiagramWithGateEarly', view=True)

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
        return



