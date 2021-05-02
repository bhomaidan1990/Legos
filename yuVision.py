#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
| author:
| Belal HMEDAN, 
| LIG lab/ Marven Team, 
| France, 2021.
| Raspberry vision handeling script.
'''
import paramiko
import numpy as np
import cv2
from time import sleep, time
from imageProcessor import imageProcessor

#=====================
# class communicator |
#=====================
class communicator():
    def __init__(self, host, username, password, port=22):
        """
        Class communicator: Read images remotely.
        ---
        Parameters:
        @param: host, string, host address 192.168.0.40 , www.something.org
        @param: username, string, the username.
        @param: password, string, the password.
        @param: port, integer.
        """
        self.host     = host
        self.username = username
        self.password = password
        self.port     = port

        self.ssh = paramiko.SSHClient()                                         #  <-- 0
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=host, username=username, password=password)


    def getImage(self, localPath, remotePath='vision/image.jpg'):
        """
        Function: getImage, to copy the image from the Raspberry pi to a localPath in PC.
        ---
        Parameters:
        @param: localPath, string, the path to the destination folder.
        @param: remotePath, string, the path to the image on the Pi.
        ---
        @return: None.
        """
        sftp = self.ssh.open_sftp()
        # remove the image
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command('sudo rm {}'.format(remotePath))
        channel = ssh_stdout.channel
        status = channel.recv_exit_status()
        # read a new image
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command('sudo raspistill -o {} --nopreview --exposure sports --timeout 1'.format(remotePath))
        channel = ssh_stdout.channel
        status = channel.recv_exit_status()
        sftp.get(remotePath, (localPath+'image.jpg'))

        sftp.close()

#======================
# class visionHandler |
#======================
class visionHandler():

    def __init__(self, path, pi_id=1, taskID='id_18'):
        """
        Class visionHandler: Read and Process images remotely.
        ---
        Parameters:
        @param: pi_id, integer, raspberry pi module id: 1, 2, ..., 6.
        @param: path, string, the path to save the image locally on PC.
        """
        self.pi_id = pi_id
        self.path = path
        self.com = communicator('192.168.125.{}0'.format(pi_id), 'pi{}'.format(pi_id), '000000')
        self.humanAction = False
        self.hand = False
        self.taskID = taskID
        self.errors = []
        self.message = ""
        self.solved = False
        self.worldState = {
        # First column
        'p_10_04': 'g', 'p_11_04': 'g', 'p_12_04': 'g', 'p_13_04': 'g',
        # Second column
        'p_10_05': 'g', 'p_11_05': 'g', 'p_12_05': 'g', 'p_13_05': 'g',
        # Third column
        'p_10_06': 'g', 'p_11_06': 'g', 'p_12_06': 'g', 'p_13_06': 'g',
        # Fourth column
        'p_10_07': 'g', 'p_11_07': 'g', 'p_12_07': 'g', 'p_13_07': 'g',
        # Swap
        'p_07_06'   : 'g', 'p_07_06'   : 'g'
        }

        self.humanStock = {
        'b_2x2': 1, 'b_2x4': 1, 'y_2x2': 1, 'y_2x4': 1
        }

        self.taskWorld = {
        'id_18' : {
        # First column
        'p_10_04': 'b', 'p_11_04': 'y', 'p_12_04': 'y', 'p_13_04': 'b',
        # Second column
        'p_10_05': 'y', 'p_11_05': 'y', 'p_12_05': 'b', 'p_13_05': 'b',
        # Third column
        'p_10_06': 'b', 'p_11_06': 'y', 'p_12_06': 'b', 'p_13_06': 'y',
        # Fourth column
        'p_10_07': 'y', 'p_11_07': 'y', 'p_12_07': 'y', 'p_13_07': 'b'
        },
        'id_25' : {
        # First column
        'p_10_04': 'y', 'p_11_04': 'b', 'p_12_04': 'b', 'p_13_04': 'y',
        # Second column
        'p_10_05': 'b', 'p_11_05': 'y', 'p_12_05': 'b', 'p_13_05': 'b',
        # Third column
        'p_10_06': 'b', 'p_11_06': 'y', 'p_12_06': 'y', 'p_13_06': 'y',
        # Fourth column
        'p_10_07': 'b', 'p_11_07': 'b', 'p_12_07': 'b', 'p_13_07': 'y'
        },
        'id_101' : {
        # First column
        'p_10_04': 'y', 'p_11_04': 'b', 'p_12_04': 'y', 'p_13_04': 'y',
        # Second column
        'p_10_05': 'b', 'p_11_05': 'y', 'p_12_05': 'b', 'p_13_05': 'b',
        # Third column
        'p_10_06': 'y', 'p_11_06': 'y', 'p_12_06': 'y', 'p_13_06': 'b',
        # Fourth column
        'p_10_07': 'y', 'p_11_07': 'b', 'p_12_07': 'y', 'p_13_07': 'b'
        }
        }

    def compareWorld(self):
        """
        Function: compareWorld, to compare the world with the task.
        ---
        Parameters:
        @param: None
        ---
        @return: None
        """
        groundTruth = self.taskWorld[self.taskID]
        self.solved = True
        self.message = ""
        for point in groundTruth:
            if not self.worldState[point] in ['g', groundTruth[point]]:
                # signal to the GUI an error in position
                self.errors.append(point)
                # send a message to the operator.
                self.message = "please pay attention, there is a wrong block!"

            if self.worldState[point] != groundTruth[point]:
                self.solved = False

    def captureWorld(self, verbose=False):
        """
        Function: captureWorld, to capture an image of the workspace/swap and analyse the locations.
        ---
        Parameters:
        @param: verbose, boolean, to print the output of the function. 
        ---
        @return: None
        """
        # capture an image.
        self.com.getImage(self.path)                                        #  <-- 1
        # Process the image.
        proc = imageProcessor(self.path)
        proc.stateAnalyzer(verbose=verbose)
        self.compareWorld()
        # write the colors to the worldState dictionary
        for key in proc.cellsState:
            self.worldState[proc.cellsState[key][0]] = proc.cellsState[key][1]
        for key in proc.swapState:
            self.worldState[key] = proc.swapState[key]
        for key in self.humanStock:
            self.humanStock[key] = proc.humanStock[key]

    def captureHand(self, verbose=False):
        """
        Function: captureHand, to capture an image of the workspace/swap and check the human hand presence.
        ---
        Parameters:
        @param: verbose, boolean, to print the output of the function. 
        ---
        @return: hand, bool True if there is human hand, False if there is no human hand.
        """

        # capture an image.
        tic = time()
        self.com.getImage(self.path)                                         #  <-- 2
        toc = time()
        if verbose:
            print('time for getting the image is: ', round(toc-tic, 3))
        proc = imageProcessor(self.path)
        detected = proc.handDetector()

        if(detected):
            self.hand = True
            self.humanAction = True

        # check if there is human hand.
        while(detected):
            # Process the image.
            print('detected status', detected)
            tic = time()
            self.com.getImage(self.path)                                     #  <-- 3
            toc = time()
            if verbose:
                print('time for getting the image is: ', round(toc-tic, 3))
                tic = toc
            detected = proc.handDetector()

        if verbose:
            print('Detected Hand status: ', detected)
        self.hand = False

#----------------------------------------------------------------------------------

# mypath = 'G:/Grenoble/Semester_4/Project_Codes/Problem_Domain/New_Domain_Problem/'

# vh = visionHandler(path=mypath)

# vh.captureWorld()

# vh.captureHand(verbose=True)
# print('out', vh.hand)
# print(vh.worldState, '\n', vh.humanStock, '\n', vh.humanAction)