#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
| author:
| Belal HMEDAN, 
| LIG lab/ Marven Team, 
| France, 2021.
| Planning script.
'''
import sys
import re
import subprocess
from time import sleep, time
from yuVision import visionHandler
from yuAction import actionHandler
from PyQt5.QtCore import QTimer

#=======================
# class problemHandler |
#=======================
class problemHandler():
    def __init__(self, path, filename, ui):
        """
        Class problemHandler: Reads, Modifies, and Writes problems.
        ---
        Parameters:
        @param: path, string, the path to the problem.
        @param: filename, string, the problem filename.
        @param: ui, user interface class.
        """
        self.path = path
        self.filename = filename
        self.plan = None
        self.solution = True
        self.NoSolution = False
        self.solved = False
        # self.actionState = True
        self.vh = visionHandler(path)
        self.ui = ui
        self.ah = None
        self.actionTimer = None
        self.neighbours = None
        # 'problem_id : list[ tuple( tuple(line index of 1st group of tasks),
        # tuple(line index of 2nd group of tasks), block line index)]'
        self.tasksMap = {
        'id_18': [((69, 71), (69, 73, 74) , 610),
        ((78, 80, 81), (78, 83, 84), 622),
        ((88, 90), (88, 92, 93), 611),
        ((98, 99), (101, 102), 618),
        ((106, 108, 109), (106, 111, 112), 623),
        ((117, 118), (120, 121), 619),
        ((125, 127, 128), (125, 130), 614),
        ((134, 136, 137), (134, 139), 615),
        ((145, 146), (148, 149), 620),
        ((153, 155, 156), (153, 158), 612),
        ((162, 164, 165), (162, 167), 616)],
        'id_25': [((175, 177), (175, 179, 180), 610),
        ((185, 186), (188, 189), 622),
        ((194, 195), (197, 198), 623),
        ((202, 204, 205), (202, 204, 205), 618),
        ((213, 214), (216, 217), 624),
        ((221, 223), (221, 225, 226), 614),
        ((230, 232, 233), (230, 235, 236), 619),
        ((240, 242), (240, 244, 245), 611),
        ((250, 252, 253), (250, 255, 256), 625),
        ((260, 262, 263), (260, 265), 615)],
        'id_101': [((273, 275, 276), (273, 278, 279), 618),
        ((283, 285, 286), (283, 288, 289), 619),
        ((293, 295, 296), (293, 298, 299), 620),
        ((304, 305), (307, 308), 621),
        ((312, 314), (312, 316, 317), 610),
        ((322, 324), (322, 326, 327), 614),
        ((331, 333), (331, 335, 336), 615),
        ((341, 342), (344, 345), 622),
        ((349, 351, 352), (349, 354, 355), 623),
        ((359, 361), (359, 363, 364), 616)],
        'id_21': [((0, 0, 0), (0, 0, 0), 0),
        ((0, 0, 0), (0, 0, 0), 0),
        ((0, 0, 0), (0, 0, 0), 0),
        ((0, 0), (0, 0), 0),
        ((0, 0), (0, 0, 0), 0),
        ((0, 0), (0, 0, 0), 0),
        ((0, 0), (0, 0, 0), 0),
        ((0, 0), (0, 0), 0),
        ((0, 0, 0), (0, 0, 0), 0),
        ((0, 0), (0, 0, 0), 0)],
        'y_2x2': [((372, 373, 374), (372, 373, 374), 613)],
        'y_2x4': [((378, 379, 380), (378, 379, 380), 621)],
        'b_2x2': [((384, 385, 386), (384, 385, 386), 615)],
        'b_2x4': [((390, 391, 392), (390, 391, 392), 625)]
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
        'p_10_04': 436,
        'p_11_04': 435,
        'p_12_04': 434,
        'p_13_04': 433,
        #
        'p_10_05': 432,
        'p_11_05': 431,
        'p_12_05': 430,
        'p_13_05': 429,
        #
        'p_10_06': 428,
        'p_11_06': 427,
        'p_12_06': 426,
        'p_13_06': 425,
        #
        'p_10_07': 424,
        'p_11_07': 423,
        'p_12_07': 422,
        'p_13_07': 421,
        #       
        'p_07_06': 438,
        'p_07_07': 439
        }

        colorMap = {
        'g': False,
        'b': True,
        'y': True
        }

        self.vh.captureWorld()

        if len(self.vh.errors) > 0:
            for point in self.vh.errors:
                self.ui.wrong(point)

        if self.vh.message != "":
            self.ui.messenger(self.vh.message)

        mappedState = {}
        print(self.vh.worldState)
        for location in self.vh.worldState:
            mappedState[locationMap[location]] = colorMap[self.vh.worldState[location]]

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
            # print('The Plan is:\n')
            self.plan = myresult[1:int(float(myresult[-6][23:-1]))+1]
            # for Action in self.plan:
            #     print(Action) # No plan: myresult[-8], plan cost: int(float(myresult[-6][23:-1]))
            
        if(save and self.plan is not None):
            with open(self.path + 'tmp/plan_{}.log'.format(time()), 'w') as fp:
                fp.writelines(self.plan)

    def taskActivator(self, problem=None):
        """
        Function: taskActivator, to activate a group of actions that have a plan.
        ---
        Parameters:
        @param: problem, string, problem ID: [id_18, id_25, id_101, 
                 y_2x2, y_2x4, b_2x2, b_2x4]
        ---
        @return: None.
        """
        if self.ui.problemChanged:
            print("Problem changed")
            self.reset_problem()
            self.vh.taskID = self.ui.getArUcoID()
            self.vh.solved = False
            self.solved = False
            self.ui.problemChanged = False

        self.solved = self.vh.solved

        if self.solved:
            print("Solved !")
            for point in self.vh.taskWorld[self.ui.getArUcoID()]:
            	self.ui.blinker(point, self.vh.taskWorld[self.ui.getArUcoID()][point])
            return

        if problem == None:
            problem = self.ui.getArUcoID()

        self.vh.captureWorld(verbose=False)

        if len(self.vh.errors) > 0:
            for point in self.vh.errors:
                self.ui.wrong(point)
        if self.vh.message != "":
            self.ui.messenger(self.vh.message, idx=1)
        
        for point in self.vh.worldState:
            if self.vh.worldState[point] !='g':
                self.ui.blinker(point, self.vh.worldState[point])

        taskList = self.tasksMap[problem]
        # Fill Human stock if empty
        if(problem[1:-1] != '_2x' and self.solution):
            for key in self.vh.humanStock:
                if (self.vh.humanStock[key] == 0):
                    print('Filling Human stock: ', key)
                    self.taskActivator(problem=key)
                    #                                            #<----
                    self.solution = False
                    return

        for taskGroup in taskList:
            #((69, 71), (69, 73, 74) , 609)

            for lineIndex in taskGroup[0]:
                # Un-Comment these lines.
                self.stateWriter(lineIndex)
            # Test if there is a solution for the temp copy.
            self.solver()
            # if there is a solution: 
            if(self.plan is not None):
                #   3. Un-comment the attached line.
                self.stateWriter(taskGroup[2])
                #   4. comment the taskGroup lines again
                for lineIndex in taskGroup[0]:
                    # comment these lines.
                    self.stateWriter(lineIndex, comment=True)
                #   1. remove the taskGroup from taskList.
                taskList.remove(taskGroup)
                #   2. write the taskList to the tasksMap.
                self.tasksMap[problem] = taskList
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
                #   3. Un-comment the attached line.
                self.stateWriter(taskGroup[2])
                #   4. comment the taskGroup lines again
                for lineIndex in taskGroup[1]:
                    # comment these lines.
                    self.stateWriter(lineIndex, comment=True)
                #   1. remove the taskGroup from taskList.
                taskList.remove(taskGroup)
                #   2. write the taskList to the tasksMap.
                self.tasksMap[problem] = taskList
                return

            else:
                for lineIndex in taskGroup[1]:
                    # comment these lines.
                    self.stateWriter(lineIndex, comment=True)

            #   1. remove the taskGroup from taskList.
            taskList.remove(taskGroup)
            #   2. write the taskList to the tasksMap.
            self.tasksMap[problem] = taskList

        self.solution = False

        if (problem[1:-1] != '_2x'):
            # There is no solution for the plan, ask the user to do the rest(GUI).
            print('No Plan')
            self.NoSolution = True
            self.ui.messenger("Please Do the Rest, our Robot cannot do more!")
            # self.reset_problem(full=False)
        else:
            print("No Solution for Swap!\n")

    def reset_problem(self, full=True):
        """
        Function: reset_problem, to reset the problem.
        ---
        Parameters:
        @param: None
        ---
        @return: None.
        """
        for lineIndex in list(range(96,392)):
            # comment these lines.
            self.stateWriter(lineIndex, comment=True)

        if full:
            for lineIndex in list(range(421,440)):
                # Un comment these lines.
                self.stateWriter(lineIndex)

            for lineIndex in list(range(610,626)):
                # comment these lines.
                self.stateWriter(lineIndex, comment=True)

    def checkAction(self):
        """
        Function: checkAction, to check if action ended.
        ---
        Parameters:
        @param: None
        ---
        @return: None.
        """
        status = self.ah.actionEnded()

        # self.actionState = status
        self.ui.actionState = status

        if status:
            self.interaction('g')
        else:
            self.interaction('p')            

    def run(self):        
        """
        Function: run, to run the problem handler.
        ---
        Parameters:
        @param: None
        ---
        @return: None.
        """
        tic = time()
        self.taskActivator()
        toc = time()
        print("time for planning is: ", round(toc-tic, 3))
        # self.reset_problem(full=False)

        if self.plan is not None:
            self.ah = actionHandler(self.plan)
            self.interaction(verbose=True)
            self.ah.action()
            self.checkAction()
        else:
            self.ui.messenger("Please Do the Rest, our Robot cannot do more!")

    def interaction(self, mode='p', verbose=False):
        """
        Function: interaction, to handle the interaction with user.
        ---
        Parameters:
        @param: mode, string, ['g', 'p']
        ---
        @return: None.
        """
        if self.neighbours is None:
            self.neighbours = self.ah.actionInterpreter(verbose=verbose)

        if mode=='p':
            # signal to neighbours to blink in red.
            self.ui.blinker(self.neighbours[0], self.vh.taskWorld[self.ui.getArUcoID()][self.neighbours[0]]+'p')
            if len(self.neighbours) > 3:
                self.ui.blinker(self.neighbours[3], self.vh.taskWorld[self.ui.getArUcoID()][self.neighbours[3]]+'p')
            for neighbour in self.neighbours[1:3]:
                if neighbour in self.vh.worldState:
                    self.ui.blinker(neighbour, self.vh.worldState[neighbour]+'p')
                    self.ui.messenger("I'm Moving to the red blinking zone!")

            self.neighbours = None

        else:
            # signal to neighbours to blink in original.
            self.ui.blinker(self.neighbours[0], self.vh.taskWorld[self.ui.getArUcoID()][self.neighbours[0]])
            if len(self.neighbours) > 3:
                self.ui.blinker(self.neighbours[3], self.vh.taskWorld[self.ui.getArUcoID()][self.neighbours[3]])
            for neighbour in self.neighbours[1:3]:
                if neighbour in self.vh.worldState:
                    self.ui.blinker(neighbour, self.vh.worldState[neighbour])
                    self.ui.messenger("I Have done my movement!")

            self.neighbours = None
#--------------------------------------------------------------