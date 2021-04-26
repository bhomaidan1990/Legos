#! /usr/bin/python3
# -*- coding: utf-8 -*-

'''
| author: Belal HMEDAN,
| LIG Lab/ Marven Team,
| France, 2021.
'''

import re
import subprocess
from time import time
from yuVision import visionHandler

#=======================
# class problemHandler |
#=======================
class problemHandler():

    def __init__(self, path, filename):
        """
        Class problemHandler: Reads, Modifies, and Writes problems.
        ---
        Parameters:
        @param: path, string, the path to the problem.
        @param: filename, string, the problem filename.
        """
        self.path = path
        self.filename = filename
        self.plan = None
        self.solution = True
        # 'problem_id : list[ tuple( tuple(line index of 1st group of tasks),
        # tuple(line index of 2nd group of tasks), block line index)]'
        self.tasksMap = {
        'id_18': [((69, 71), (69, 73, 74) , 608),
        ((78, 80, 81), (78, 83, 84), 620),
        ((88, 90), (88, 92, 93), 609),
        ((98, 99), (101, 102), 616),
        ((106, 108, 109), (106, 111, 112), 621),
        ((117, 118), (120, 121), 617),
        ((125, 127, 128), (125, 130), 612),
        ((134, 136, 137), (134, 139), 613),
        ((145, 146), (148, 149), 618),
        ((153, 155, 156), (153, 158), 610),
        ((162, 164, 165), (162, 167), 614)],
        'id_25': [((175, 177), (175, 179, 180), 608),
        ((185, 186), (188, 189), 620),
        ((194, 195), (197, 198), 621),
        ((202, 204, 205), (202, 204, 205), 616),
        ((213, 214), (216, 217), 622),
        ((221, 223), (221, 225, 226), 612),
        ((230, 232, 233), (230, 235, 236), 617),
        ((240, 242), (240, 244, 245), 609),
        ((250, 252, 253), (250, 255, 256), 623),
        ((260, 262, 263), (260, 265), 613)],
        'id_101': [((273, 275, 276), (273, 278, 279), 616),
        ((283, 285, 286), (283, 288, 289), 617),
        ((293, 295, 296), (293, 298, 299), 618),
        ((304, 305), (307, 308), 619),
        ((312, 314), (312, 316, 317), 608),
        ((322, 324), (322, 326, 327), 612),
        ((331, 333), (331, 335, 336), 613),
        ((341, 342), (344, 345), 620),
        ((349, 351, 352), (349, 354, 355), 621),
        ((359, 361), (359, 363, 364), 614)],
        'y_2x2': [((372, 373), (372, 373), 611)],
        'y_2x4': [((377, 378, 379), (377, 378, 379), 619)],
        'b_2x2': [((383, 384), (383, 384), 613)],
        'b_2x4': [((388, 389, 390), (388, 389, 390), 623)]
        }

    def stateReader(self):
        """
        Function: stateReader, to read the problem file, and map the state read from Perception module
        to an empty/full locations.
        ---
        Parameters:
        @param: None
        ---
        @return: None
        """
        locationMap = {
        'ws_11': 419, #'p_13_07',
        'ws_12': 420, #'p_12_07',
        'ws_13': 421, #'p_11_07',
        'ws_14': 422, #'p_10_07',
        'ws_21': 423, #'p_13_06',
        'ws_22': 424, #'p_12_06',
        'ws_23': 425, #'p_11_06',
        'ws_24': 426, #'p_10_06',
        'ws_31': 427, #'p_13_05',
        'ws_32': 428, #'p_12_05',
        'ws_33': 429, #'p_11_05',
        'ws_34': 430, #'p_10_05',
        'ws_41': 431, #'p_13_04',
        'ws_42': 432, #'p_12_04',
        'ws_43': 433, #'p_11_04',
        'ws_44': 434, #'p_10_04',
        's1': 435, #'p_07_05',
        's2': 436, #'p_07_06',
        's3': 437, #'p_07_07'
        }

        colorMap = {
        'g': False,
        'b': True,
        'y': True
        }

        vH = visionHandler(self.path)
        vH.captureWorld()
        
        mappedState = {}
        for location in vH.worldState:
            mappedState[locationMap[location]] = colorMap[vH.worldState[location]]

        for lineIdx in mappedState:
            self.stateWriter(lineIdx, comment=mappedState[lineIdx])

    def stateWriter(self, lineIndex, comment=False, shift=0):
        """
        Function: stateWriter, to write the workspace/stock locations into the problem file.
        ---
        Parameters:
        @param: comment, boolean, True to comment the line, False to un-comment the line.
        @param: shift, integer, the shift in the line indicies.
        @param: lineIndex, integer, number of the line of which we want to update the state.
        ---
        @return: None.
        """
        with open(self.path + self.filename, 'r') as fp:
            state = fp.readlines()
        with open(self.path + self.filename, 'w') as fp:
            line = state[lineIndex+shift-1]
            if(not comment):
                state[lineIndex+shift-1] = re.sub(" ; ", " ", line)# line + '\n'
            else:
                if not re.findall("^;", line.strip()):
                    state[lineIndex+shift-1] = re.sub("\(", "; (", line, 1)# line + '\n'

            fp.writelines(state)

    def solver(self, 
        libraryPath='G:/Grenoble/Semester_4/PDDL/pddl4j-devel/build/libs/pddl4j-3.8.3.jar',
        planner = 'fr.uga.pddl4j.planners.htn.stn.tfd.TFDPlanner',
        Memory = ['-Xms12288m' ,'-Xmx12288m'],
        domainPath  = 'new_domain.pddl',
        problemPath = 'problem_main.pddl',
        save=False
        ):
        """
        Function: solver, to run the solver and get a plan if there is one.
        ---
        Parameters:
        @param: planner, string, planner name.
        @param: libraryPath, string, the path to the java library(extension included)
        @param: Memory, list of two ['-Xms size m', -Xmx size m'].
        @param: domainPath, string, the path to the domain, (extension included).
        @param: problemPath, string, the path to the problem, (extension included).
        @param: save, boolean, to save the plan as log file.
        ---
        @return: None.
        """
        cmd = ['java', '-javaagent:'+libraryPath, '-server' , Memory[0] , Memory[1], planner, '-d', self.path+domainPath, '-p', self.path+problemPath]
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')[1:]
        myresult = output.split('\n')[6:]
        # print('res: ', myresult)
        if(len(myresult)==0):
            # print('No Plan')
            self.plan = None
        elif(myresult[2]=='no plan found\r'):
            # print('No Plan')
            self.plan = None
        elif(int(float(myresult[-6][23:-1]))==0):
            # print('No Plan')
            self.plan = None
        else:
            print('The Plan is:\n')
            self.plan = myresult[1:int(float(myresult[-6][23:-1]))+1]
            for Action in self.plan:
                print(Action) # No plan: myresult[-8], plan cost: int(float(myresult[-6][23:-1]))
            
        if(save and self.plan is not None):
            with open(self.path + 'tmp/plan_{}.log'.format(time()), 'w') as fp:
                fp.writelines(self.plan)

    def taskActivator(self, problem):
        """
        Function: taskActivator, to activate a group of actions that have a plan.
        ---
        Parameters:
        @param: problem, string, problem ID: [id_18, id_25, id_101, 
                 y_2x2, y_2x4, b_2x2, b_2x4]
        ---
        @return: None.
        """
        vh = visionHandler(self.path)
        vh.captureWorld(verbose=False)
        vh.captureHand()

        taskList = self.tasksMap[problem]

        # Fill Human stock if empty
        if(problem[1:-1] != '_2x' and self.solution):
            for key in vh.humanStock:
                if (vh.humanStock[key] == 0):
                    print('Filling Human stock: ', key)
                    self.taskActivator(key)

        for taskGroup in taskList:
            #((69, 71), (69, 73, 74) , 609)

            for lineIndex in taskGroup[0]:
                # Un-Comment these lines.
                self.stateWriter(lineIndex)
            # Test if there is a solution for the temp copy.
            self.solver()
            # if there is a solution: 
            if(self.plan is not None):
                #   1. remove the taskGroup from taskList.
                taskList = taskList.remove(taskGroup)
                #   2. write the taskList to the tasksMap.
                taskList = self.tasksMap[problem]
                #   3. Un-comment the attached line.
                self.stateWriter(taskGroup[2])
            #   4. send the taskGroup to the Robot to be done.
                #   5. comment the taskGroup lines again
                for lineIndex in taskGroup[0]:
                    # comment these lines.
                    self.stateWriter(lineIndex, comment=True)

                self.stateWriter(taskGroup[2])
                self.solution = True
                #   6. break the taskList loop.
                return
            else:
                for lineIndex in taskGroup[0]:
                    # comment these lines.
                    self.stateWriter(lineIndex, comment=True)

            for lineIndex in taskGroup[1]:
                # Un-Comment these lines.
                self.stateWriter(lineIndex)
            # Test if there is a solution for the temp copy.
            self.solver()
            # if there is a solution: 
            if(self.plan is not None):
                #   1. remove the taskGroup from taskList.
                taskList = taskList.remove(taskGroup)
                #   2. write the taskList to the tasksMap.
                taskList = self.tasksMap[problem]
                #   3. Un-comment the attached line.
                self.stateWriter(taskGroup[2])
            #   4. send the taskGroup to the Robot to be done.
                #   5. comment the taskGroup lines again
                for lineIndex in taskGroup[1]:
                    # comment these lines.
                    self.stateWriter(lineIndex, comment=True)

                self.stateWriter(taskGroup[2])
                self.solution = True
                #   6. break the taskList loop.
                return

            else:
                for lineIndex in taskGroup[1]:
                    # comment these lines.
                    self.stateWriter(lineIndex, comment=True)

        if (self.plan is None):
            # There is no solution for the plan, ask the user to do the rest(GUI).
            print('No Plan')
            self.solution = False
            pass

    def reset_problem(self):
        """
        Function: reset_problem, to reset the problem.
        ---
        Parameters:
        @param: None
        ---
        @return: None.
        """
        for lineIndex in list(range(417,438)):
            # comment these lines.
            self.stateWriter(lineIndex)

        for lineIndex in list(range(608,624)):
            # comment these lines.
            self.stateWriter(lineIndex, comment=True)

#--------------------------------------------------------------

mypath = 'G:/Grenoble/Semester_4/Project_Codes/Problem_Domain/New_Domain_Problem/'

ph = problemHandler(path = mypath, filename='problem_main.pddl')
tic = time()
ph.stateReader()
toc = time()
print("time for perception is: ", round(toc-tic, 3))
tic = toc
ph.taskActivator(problem='id_18')
while(ph.plan is not None):
    ph.taskActivator(problem='id_18')
toc = time()
print("time for planning is: ", round(toc-tic, 3))

ph.reset_problem()

# loop as long as there is a solution
# solution = True
# while(solution):
#     pass
#     # 0. capture the world state
#     ph.stateReader()
#     # 1. do a task.

#     # 2. ensure that the robot has finished the execution.

#     # 3. delay for 3 seconds(more or less), then hand detection.

#     # 4. capture the world state

#     # 5. write the world state to the problem

#     # 6. call the solver to see if there is a solution go back to 1.
#     #        otherwise go to 7.

#     # 7- show on the GUI that the user has to do the rest

#     # 8. check human stock and call the solver to see if there is a solution got to 9.
#     #       otherwise do nothing!

#     # 9- fill empty human stock, then go back to 1.

#     # 10. check the whole ArUco is done, then:

#     solution = False