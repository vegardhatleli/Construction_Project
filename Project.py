from Task import *


class Project:

    def __init__(self, tasks, projectID):
        self.projectID = projectID
        self.tasks = tasks

    def getTasks(self):
        return self.tasks

    def setTasks(self, tasks):
        self.tasks = tasks

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
                        earliestCompleationDateTask = min(
                            task.getPredecessors(), key=lambda x: x.getEarlyCompleationDate())
                        task.setEarlyStartDate(
                            earliestCompleationDateTask.getEarlyCompleationDate())

                        task.setEarlyCompleationDate(
                            int(task.getEarlyStartDate()) + int(task.getExpectedDuration()))

                        remainingTasks.remove(task)
        print('Early dates is set')
        return

    def printEarlyDates(self):
        for task in self.getTasks():
            print(
                f' Task: {task.getTaskID()} | Predecessor: {[p.getTaskID() for p in task.getPredecessors()]} | Succsessor: {[p.getTaskID() for p in task.getSuccessors()]} | Early Start Date: {task.getEarlyStartDate()}| Early Compleation Date: {task.getEarlyCompleationDate()}')

    def getMinimumProjectDuration(self):
        task = max(self.getTasks(), key=lambda x: x.getEarlyCompleationDate())
        return task.getEarlyCompleationDate()

    def setLateDates(self):
        # Denne skal jeg få til
        return


# Load class should do this, but here is only for testing
Start = Task('Start', [0, 0, 0])
A = Task('A', [3, 4, 6])
B = Task('B', [1, 2, 4])
C = Task('C', [1, 1, 3])
D = Task('D', [1, 1, 3])
E = Task('E', [1, 2, 4])
F = Task('F', [1, 2, 4])
G = Task('G', [1, 2, 4])
H = Task('H', [8, 10, 12])
J = Task('J', [3, 4, 6])
K = Task('K', [1, 1, 3])
End = Task('End', [0, 0, 0])

A.addPredecessor(Start)
B.addPredecessor(Start)
C.addPredecessor(A)
D.addPredecessor(A)
D.addPredecessor(B)
E.addPredecessor(A)
F.addPredecessor(C)
G.addPredecessor(D)
G.addPredecessor(F)
H.addPredecessor(E)
J.addPredecessor(G)
K.addPredecessor(H)
K.addPredecessor(J)
# End.addPredecessor(J)
# End.addPredecessor(H)


tasks = [Start, A, B, C, D, E, F, G, H, J, K, End]


warehouse = Project(tasks, 'Warehouse')


warehouse.setEarlyDates()


warehouse.printEarlyDates()

print(warehouse.getMinimumProjectDuration())
