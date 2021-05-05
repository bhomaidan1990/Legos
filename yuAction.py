#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
| author:
| Belal HMEDAN, 
| LIG lab/ Marven Team, 
| France, 2021.
| Action Handeling script.
'''
import subprocess
from RWS4YuMi import RWS4YuMi
from time import time
from PyQt5.QtCore import QTimer
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
	    self.actionTimer = None
	    self.api = RWS4YuMi()

	def pointCoords(self, point, filepath='points.txt', name=None):
		"""
		Function: pointCoords, to map the string point 'p_yy_xx' into robtarget.
		---
		Parameters:
		@param: point, string, the point to be written to RAPID code: ['p_yy_xx', 'p_yy_xxVS', 'p_yy_xxHA', 'p_yy_xxHC'] 
		@param: filepath, string, thae path to the RAPID code to be modified.
		---
		@return: None.
		"""
		with open(filepath, 'r') as fp:
			line = True
			while(line):
				line = fp.readline()
				if(len(line.split())>2):
					if(line.split()[2]==point):
						if name is not None:
							line = line.split()
							line[2] = name
							line = " ".join(line)
						return line
		print("Point {} Not Found!".format(point))
		return None
	
	def writeLine(self, point, filepath='Rapid/currLeft.mod'):
		"""
		Function: writeLine, to write the point robtarget into the RAPID code.
		---
		Parameters:
		@param: point, string, the point to be written to RAPID code: ['p_yy_xx', 'p_yy_xxVS', 'p_yy_xxHA', 'p_yy_xxHC'] 
		@param: filepath, string, thae path to the RAPID code to be modified.
		---
		@return: None.
		"""
		name = 'pickpoint'
		lineIndex = 10
			
		if len(point)>7 :
			name = 'placepoint'
			lineIndex = 11

		line = "  "+self.pointCoords(point, name=name)

		with open(filepath, 'r') as fp:
		    codeList = fp.readlines()

		with open(filepath, 'w') as fp:
			codeList[lineIndex-1] = line+"\n"
			fp.writelines(codeList)

	def actionInterpreter(self, verbose=False):
		"""
		Function: actionInterpreter, to interpret the plan into pick & place positions, and neighbours.
		---
		Parameters:
		@param: None
		---
		@return: neighborhood, list of point strings to be passed to the GUI.
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
		'b_2x4_51_R' : 'p_18_08',
		'b_2x4_52_R' : 'p_20_08',
		'b_2x4_53_R' : 'p_22_08',
		'b_2x4_41_R' : 'p_18_06',
		'b_2x4_51_L' : 'p_19_08',
		'b_2x4_52_L' : 'p_21_08',
		'b_2x4_53_L' : 'p_23_08',
		'b_2x4_41_L' : 'p_19_06'
		}
		rotDict = {
		'p_20_00' : ['HA', 'HC'],
		'p_21_00' : ['HA', 'HC'],
		'p_22_00' : ['HA', 'HC'],
		'p_23_00' : ['HA', 'HC'],
		'p_20_06' : ['HA', 'HC'],
		'p_21_06' : ['HA', 'HC'],
		'p_22_06' : ['HA', 'HC'],
		'p_23_06' : ['HA', 'HC'],
		# 
		'p_23_02' : ['HA', 'HC'],
		'p_22_02' : ['HC', 'HA'],
		'p_21_02' : ['HA', 'HC'],
		'p_20_02' : ['HC', 'HA'],
		'p_23_08' : ['HA', 'HC'],
		'p_22_08' : ['HC', 'HA'],
		'p_21_08' : ['HA', 'HC'],
		'p_20_08' : ['HC', 'HA'],
		'p_19_08' : ['HA', 'HC'],
		'p_18_08' : ['HC', 'HA'],
		'p_23_04' : ['HA', 'HC'],
		'p_22_04' : ['HC', 'HA'],
		'p_21_04' : ['HA', 'HC'],
		'p_20_04' : ['HC', 'HA'],
		'p_19_06' : ['HA', 'HC'],
		'p_18_06' : ['HC', 'HA'],
		# swap
		'p_07_06' : ['HC', 'HC'],
		'p_07_07' : ['HC', 'HC']
		}
		# action is a list of action and related params
		for action in self.plan:

			action = action[action.index('(')+1:action.index(')')].split()
			if(verbose):
				print(action)
			if action[0]=='hold_gripper':
				pickPos = legoDict[action[1]]
			elif action[0]=='hold_gripper_right':
				pickPos = legoDict[action[1]+'_R']
			elif action[0]=='hold_gripper_left':
				pickPos = legoDict[action[1]+'_L']

			elif action[0] in ['put_2x2_v', 'put_2x2_h']:
				placePos = action[-3]+"VS"
				# print(placePos)
				neighborhood = action[-3:]
			elif action[0] in ['put_upper_4x2', 'put_lower_4x2', 'put_left_2x4', 'put_right_2x4']:
				placePos = action[-4]+"VS"
				# print(placePos)
				neighborhood = action[-4:]

			elif action[0] in ['rotate_2x2_loaded_gripper_v2h', 'rotate_2x4_right_loaded_gripper_v2h_clk', 'rotate_2x4_left_loaded_gripper_v2h_clk']:
				rotAngle = 90
				
			elif action[0] in ['rotate_2x4_right_loaded_gripper_v2h_anticlk', 'rotate_2x4_left_loaded_gripper_v2h_anticlk']:
				rotAngle = -90
				
		if rotAngle == 90:
			placePos = placePos[:-2]+rotDict[pickPos][1]
		elif rotAngle == -90:
			placePos = placePos[:-2]+rotDict[pickPos][0]

		self.writeLine(pickPos)
		self.writeLine(placePos)
		if verbose:
			print("points: ",pickPos, placePos)

		return neighborhood

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
		status = self.api.actionStatus()

		if status!='stopped':
			return False
			
		elif status=='stopped':
			return True

#----------------------------------

# ah = actionHandler([])
# # # ah.actionMapper()

# # # tic = time()
# ah.action()

# if(ah.actionEnded()):
# 	toc = time()
# 	print('Done within: {} seconds.'.format(round(toc-tic, 3)))