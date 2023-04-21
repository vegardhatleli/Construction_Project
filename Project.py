from Task import *
import pandas as pd


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
                        latestCompleationDateTask = max(
                            task.getPredecessors(), key=lambda x: x.getEarlyCompleationDate())  # max her, ikke min som det står i oppgaven. Det gir mye mer mening i mitt hodet, og eller i tabellen
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

        '''
    def printEarlyDates(self):
        for task in self.getTasks():
            print(
                f' Task: {task.getTaskID()} | Predecessor: {[p.getTaskID() for p in task.getPredecessors()]} | Succsessor: {[p.getTaskID() for p in task.getSuccessors()]} | Early Start Date: {task.getEarlyStartDate()}| Early Compleation Date: {task.getEarlyCompleationDate()}')
        '''

    def setLateDates(self):
        remainingTasks = self.getTasks().copy()
        while len(remainingTasks) > 0:
            for task in remainingTasks:
                if not set(task.getSuccessors()).intersection(set(remainingTasks)):
                    if len(task.getSuccessors()) == 0:
                        # Denne er lowkey feil tror jeg, du må se her
                        task.setLateStartDate(self.getMinimumProjectDuration())
                        remainingTasks.remove(task)
                    else:
                        maxLateStartDate = min(  # Her står det max i oppgaven, men han mener min
                            task.getSuccessors(), key=lambda x: x.getLateStartDate())

                        task.setLateCompleationDate(
                            maxLateStartDate.getLateStartDate())

                        task.setLateStartDate(
                            task.getLateCompleationDate() - task.getExpectedDuration())

                        remainingTasks.remove(task)
        print('Late Date is set')

        '''
    def printLateDates(self):
        for task in self.getTasks():
            print(
                f' Task: {task.getTaskID()} | Predecessor: {[p.getTaskID() for p in task.getPredecessors()]} | Succsessor: {[p.getTaskID() for p in task.getSuccessors()]} | Late Start Date: {task.getLateStartDate()}| Late Completion Date: {task.getLateCompleationDate()}')
        '''

    def printProjectToExcel(self):
        headers = ['Task', 'Predecessor', 'Succsessor', 'Duration', 'Early Start Date',
                   'Early Completion Date', 'Late Start Date', 'Late Completion Date', 'Critcal Task?']
        data = []
        for task in self.getTasks():
            critcal = (task.getEarlyStartDate() == task.getLateStartDate())
            values = [task.getTaskID(), [p.getTaskID() for p in task.getPredecessors()], [p.getTaskID() for p in task.getSuccessors()], task.getExpectedDuration(
            ), task.getEarlyStartDate(), task.getEarlyCompleationDate(), task.getLateStartDate(), task.getLateCompleationDate(), critcal]
            data.append(values)

        df = pd.DataFrame(data, columns=headers)

        with pd.ExcelWriter('Warehouse.xlsx') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)


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
End.addPredecessor(K)

tasks = [Start, A, B, C, D, E, F, G, H, J, K, End]

warehouse = Project(tasks, 'Warehouse')

warehouse.setEarlyDates()

warehouse.setLateDates()

# warehouse.printEarlyDates()
# print('###########')
# warehouse.printLateDates()

warehouse.printProjectToExcel()
