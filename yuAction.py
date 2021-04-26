#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
| author:
| Belal HMEDAN, LIG lab/ Marven Team, France, 2021.
| Action Handeling script.
'''
import subprocess
from RWS4YuMi import RWS4YuMi
from time import sleep
#

#======================
# class actionHandler |
#======================
class actionHandler():
	def __init__(self, plan):
	    """
	    Class actionHandler: map the plan into Rapid code.
	    ---
	    Parameters:
	    @param: plan, list of strings list, each string list is an action with parameters.
	    """
	    self.plan = plan
	    self.api = RWS4YuMi()

	def actionInterpreter(self):
	    """
	    Function: actionInterpreter, to extract the pick, place, neighbuorhood points, and rotation.
	    ---
	    Parameters:
	    @param: None
	    ---
	    @return: pickPos, string of the shape 'p_yy_xx', the position for pick task.
	             placePos, string of the shape 'p_yy_xx', the position for place task.
	             rotAngle, integer, [-90, 0, 90] rtoation angle ==> [anticlockwise, no-rotaion, clockwise].
	             neighborhood, list of strings of the shape 'p_yy_xx', defines the neighbourhood.
	    """
	    rotAngle = 0
		legoDict = {
		# y_2x2
		'y_2x2_11' : 'p_20_00',
		'y_2x2_12' : 'p_21_00',
		'y_2x2_13' : 'p_22_00',
		'y_2x2_14' : 'p_23_00',
		# b_2x2
		'b_2x2_41' : 'p_20_06',
		'b_2x2_42' : 'p_21_06',
		'b_2x2_43' : 'p_22_06',
		'b_2x2_44' : 'p_23_06',
		# y_2x4
		'y_2x4_21_L' : 'p_21_02',
		'y_2x4_22_L' : 'p_23_02',
		'y_2x4_31_L' : 'p_21_04',
		'y_2x4_32_L' : 'p_23_04', 
		'y_2x4_21_R' : 'p_20_02',
		'y_2x4_22_R' : 'p_22_02',
		'y_2x4_31_R' : 'p_20_04',
		'y_2x4_32_R' : 'p_22_04',
		# b_2x4
		'b_2x4_51_L' : 'p_18_08',
		'b_2x4_52_L' : 'p_20_08',
		'b_2x4_53_L' : 'p_22_08',
		'b_2x4_41_L' : 'p_18_06',
		'b_2x4_51_R' : 'p_19_08',
		'b_2x4_52_R' : 'p_21_08',
		'b_2x4_53_R' : 'p_23_08',
		'b_2x4_41_R' : 'p_19_06'
		}
		# action is a list of action and related params
		for action in self.plan:

			action[action.index('(')+1:action.index(')')].split()

			if action[0]=='hold_gripper':
				pickPos = legoDict[action[1]]
			elif action[0]=='hold_gripper_right':
				pickPos = legoDict[action[1]+'_R']
			elif action[0]=='hold_gripper_left':
				pickPos = legoDict[action[1]+'_L']

			elif action[0] in ['put_2x2_v', 'put_2x2_h']:
				placePos = action[-3]
				neighborhood = action[-2:]
			elif action[0] in ['put_upper_4x2', 'put_lower_4x2', 'put_left_2x4', 'put_right_2x4']:
				placePos = action[-4]
				neighborhood = action[-3:]

			elif action[0] in ['rotate_2x2_loaded_gripper_v2h', 'rotate_2x4_right_loaded_gripper_v2h_clk', 'rotate_2x4_left_loaded_gripper_v2h_clk']:
				rotAngle = 90
			elif action[0] in ['rotate_2x4_right_loaded_gripper_v2h_anticlk', 'rotate_2x4_left_loaded_gripper_v2h_anticlk']:
				rotAngle = -90

		return pickPos, placePos, rotAngle, neighborhood

	def pathPlanner(self, srcPoint, dstPoint):
		"""
		Function: pathPlanner, to find the path among available paths.
		---
		Parameters:
		@param: srcPoint, string of the shape 'p_yy_xx', start point.
		@param: dstPoint, string of the shape 'p_yy_xx', end point.
		---
		@return: path, list of strings(points) of the shape 'p_yy_xx'
		"""
		# paths = [[p1, p2, p3, p4], [p1, p2, p5], ...]
		paths = []
		for path in paths:
			if (path[0] == srcPoint and path[-1] == dstPoint):
				return path

	def actionMapper(self):

	    pass

	def actionWriter(self):

	    pass

	def action(self):
		"""
		Function: action, to excute an action by sending RAPID code to the robot.
		---
		Parameters:
		@param: None
		---
		@return: None.
		"""
		apiPath = "G:/Grenoble/Semester_4/Project_Codes/Theabut_API/rwsclient4yu"
		cmd = ['gradlew', 'run']
		result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, cwd=apiPath)
		# output = result.stdout.decode('utf-8')[1:]
		# print(output)

	def actionEnded(self):
		"""
		Function: actionEnded, to check if the robot action has ended.
		---
		Parameters:
		@param: None
		---
		@return: boolean, True if the action ended, False in case of Errors.
		"""
		status = ''
		while(status!='stopped' and status is not None):
			status = self.api.actionStatus()
			sleep(3)
		if status is None:
			return False
		return True