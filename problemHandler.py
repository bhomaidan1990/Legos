#! /usr/bin/python3
# -*- coding: utf-8 -*-

'''
| author: Belal HMEDAN,
| LIG Lab/ Marven Team,
| France, 2021.
'''
#-------------#
#--  Usage ---#
#-------------#
# ./sth params
#--------------------------------------------------------------

import re
import subprocess

#=======================
# class problemHandler |
#=======================
class problemHandler():

    def __init__(self, path):
        """
        Class problemHandler: Reads, Modifies, and Writes problems.
        ---
        Parameters:
        @param: path, string, the path to the problem(extension included .hddl/.pddl).
        """
        self.path = path
        self.plan = None
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
        'swap_W2x2': [((372, 373), (372, 373), 611)],
        'swap_W2x4': [((377, 378, 379), (377, 378, 379), 619)],
        'swap_B2x2': [((383, 384), (383, 384), 613)],
        'swap_B2x4': [((388, 389, 390), (388, 389, 390), 623)]
        }

    def stateReader(self):
        """
        Function: stateReader, to read the problem file, and map the state read from Perception module
        to an empty/full locations.
        ---
        Parameters:
        @param: None
        ---
        @return: list of locations state empty/full
        """
        locationMap = {
        'ws_11': 'p_10_04',
        'ws_12': 'p_10_05',
        'ws_13': 'p_10_06',
        'ws_14': 'p_10_07',
        'ws_21': 'p_11_04',
        'ws_22': 'p_11_05',
        'ws_23': 'p_11_06',
        'ws_24': 'p_11_07',
        'ws_31': 'p_12_04',
        'ws_32': 'p_12_05',
        'ws_33': 'p_12_06',
        'ws_34': 'p_12_07',
        'ws_41': 'p_13_04',
        'ws_42': 'p_13_05',
        'ws_43': 'p_13_06',
        'ws_44': 'p_13_07',
        's1': 'p_07_05',
        's2': 'p_07_06',
        's3': 'p_07_07'
        }

        colorMap = {
        'g': '        ( empty_location )',
        'b': '        ; ( empty_location )',
        'y': '        ; ( empty_location )'
        }

        vH = visionHandler(self.path)
        vH.captureWorld()
        
        mappedState = []
        for location in vH.worldState:
            mappedState.append(colorMap[vH.worldState[location][:-1]] + locationMap[location] + colorMap[vH.worldState[location]][-1])  

        return mappedState

    def stateWriter(self, lineIndex, filename, comment=False, shift=0):
        """
        Function: stateWriter, to write the workspace/stock locations into the problem file.
        ---
        Parameters:
        @param: comment, boolean, True to comment the line, False to un-comment the line.
        @param: shift, integer, the shift in the line indicies.
        @param: lineIndex, integer, number of the line of which we want to update the state.
        @param: filename, string, the problem filename to write locations state empty/full.
        ---
        @return: None.
        """
        with open(self.path + filename, 'r') as fp:
            state = fp.readlines()
        with open(self.path + filename, 'w') as fp:
            line = state[lineIndex+shift-1]
            if(not comment):
                state[lineIndex+shift-1] = re.sub(" ; ", " ", line)# line + '\n'
            else:
                state[lineIndex+shift-1] = re.sub("\(", "; (", line, 1)# line + '\n'

            fp.writelines(state)

    def solver(self, 
        libraryPath='F:/Grenoble/Semester_4/PDDL/pddl4j-devel/build/libs/pddl4j-3.8.3.jar',
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

        if(myresult[0]==''):
            # print('No Plan')
            self.plan = None
        else:
            print('The Plan is:\n')
            self.plan = myresult[1:int(float(myresult[-6][23:-1]))+1]
            for Action in self.plan:
                print(Action) # No plan: myresult[-8], plan cost: int(float(myresult[-6][23:-1]))
            
        if(save):
            with open(self.path + 'plan.log', 'w') as fp:
                fp.writelines(output)

    def taskActivator(self, filename, problem):
        """
        Function: taskActivator, to activate a group of actions that have a plan.
        ---
        Parameters:
        @param: filename, string, the problem filename.
        @param: problem, string, problem ID: [id_18, id_25, id_101, 
                 swap_W2x2, swap_W2x4, swap_B2x2, swap_W2x4]
        ---
        @return: None.
        """
        taskList = self.tasksMap[problem]
        solution = False

        for taskGroup in taskList:
            #((69, 71), (69, 73, 74) , 609)

            for lineIndex in taskGroup[0]:
                # Un-Comment these lines.
                self.stateWriter(lineIndex, filename)
            # Test if there is a solution for the temp copy.
            self.solver(problem=self.path+filename)
            # if there is a solution: 
            if(self.plan is not None):
                #   1. solution = True
                solution=True
                #   2. remove the taskGroup from taskList.
                taskList = taskList.remove(taskGroup)
                #   3. write the taskList to the tasksMap.
                taskList = self.tasksMap[problem]
                #   4. Un-comment the attached line.
                self.stateWriter(taskGroup[2], filename)
            #   5. send the taskGroup to the Robot to be done.
                #   6. comment the taskGroup lines again
                for lineIndex in taskGroup[0]:
                    # comment these lines.
                    self.stateWriter(lineIndex, filename, comment=True)
                #   7. break the taskList loop.
                return

            for lineIndex in taskGroup[1]:
                # Un-Comment these lines.
                self.stateWriter(lineIndex, filename)
            # Test if there is a solution for the temp copy.
            # if there is a solution: 
            #   1. solution = True  
            #   2. remove the taskGroup from taskList. 
            #   3. write the taskList to the tasksMap.
            #   4. Un-comment the attached line.
            #   5. send the taskGroup to the Robot to be done.
            #   6. comment the taskGroup lines again
            for lineIndex in taskGroup[1]:
                # Comment these lines.
                self.stateWriter(lineIndex, filename, comment=True)
            #   7. break the taskList loop.
                pass
        if (not solution):
            # There is no solution for the plan, ask the user to do the rest.
            pass
#--------------------------------------------------------------
path = 'F:/Grenoble/Semester_4/Project_Codes/Problem_Domain/New_Domain_Problem/'
ph = problemHandler(path)

ph.solver()