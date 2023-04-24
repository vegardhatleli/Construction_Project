from Task import *
import pandas as pd


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
            critcal = (task.getEarlyStartDate() == task.getLateStartDate())
            values = [task.getTaskID(), [p.getTaskID() for p in task.getPredecessors()], [p.getTaskID() for p in task.getSuccessors()], task.getExpectedDuration(
            ), task.getDescription(), task.getEarlyStartDate(), task.getEarlyCompleationDate(), task.getLateStartDate(), task.getLateCompleationDate(), critcal]
            data.append(values)

        df = pd.DataFrame(data, columns=headers)

        with pd.ExcelWriter('Warehouse.xlsx') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

    def loadProjectFromExcel(self, filepath):
        df = pd.read_excel(filepath)

        for index, row in df.iterrows():
            if row.isnull().all():
                continue
            type = row['Types']
            taskID = row['Codes']
            description = row['Description']
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


warehouse = Project([], 'Warehouse')
warehouse.loadProjectFromExcel(
    '/Users/vegardhatleli/Downloads/Warehouse.xlsx')

# print(warehouse.getTasks()[5].getExpectedDuration())

warehouse.setEarlyDates()
warehouse.setLateDates()
warehouse.printProjectToExcel()


'''
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

warehouse.printProjectToExcel()
'''
