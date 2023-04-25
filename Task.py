from logging import critical
import random


class Task:

    def __init__(self, taskID, duration, description):
        self.taskID = taskID
        self.predecessors = []
        self.successors = []
        self.duration = duration
        self.randomDuration = None
        self.description = description
        self.earlyStartDate = None
        self.earlyCompleationDate = None
        self.lateStartDate = None
        self.lateCompleationDate = None
        self.critcal = False

    def getTaskID(self):
        return self.taskID

    def setTaskID(self, taskID):
        self.taskID = taskID

    def addPredecessor(self, task):
        self.predecessors.append(task)
        task.addSuccessor(self)
        '''
        for predess in task.getPredecessors():
            if predess not in self.predecessors:
                self.predecessors.append(predess)
                predess.addSuccessor(self)
                '''

    def addSuccessor(self, task):
        self.successors.append(task)

    def getPredecessors(self):
        return self.predecessors

    def getSuccessors(self):
        return self.successors

    def getExpectedDuration(self):
        return self.duration[1]

    def setDuration(self, duration):
        self.duration = duration

    def setRandomDuration(self, riskFactor):
        if (riskFactor*self.duration[1] < self.duration[0]):
            self.duration[1] = self.duration[0]
        elif (riskFactor*self.duration[1] > self.duration[2]):
            self.duration[1] = self.duration[2]
        else:
            self.duration[1] = self.duration[1] * riskFactor

        self.randomDuration = round(random.triangular(self.duration[0], self.duration[2], self.duration[1]),2)

    def getRandomDuration(self):
        return self.randomDuration

    def getDuration(self):
        return self.duration

    def setEarlyStartDate(self, date):
        self.earlyStartDate = date

    def getEarlyStartDate(self):
        return self.earlyStartDate

    def setEarlyCompleationDate(self, date):
        self.earlyCompleationDate = date

    def getEarlyCompleationDate(self):
        return self.earlyCompleationDate

    def setLateStartDate(self, date):
        self.lateStartDate = date

    def getLateStartDate(self):
        return self.lateStartDate

    def getLateCompleationDate(self):
        return self.lateCompleationDate

    def setLateCompleationDate(self, date):
        self.lateCompleationDate = date

    def setDescription(self, description):
        self.description = description

    def getDescription(self):
        return self.description
    
    def setCritcal(self, bool):
        self.critical = bool

    def getCritical(self):
        if abs(self.getLateStartDate() - self.getEarlyStartDate()) <= 0.1:
            return True
        else:
            return False
