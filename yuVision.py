#! /usr/bin/python3
# -*- coding: utf-8 -*-

'''
| author:
| Belal HMEDAN, LIG lab/ Marven Team, France, 2021.
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

        self.ssh = paramiko.SSHClient()
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
        sftp.get(remotePath, localPath+'image.jpg')

        sftp.close()

#======================
# class visionHandler |
#======================
class visionHandler():

    def __init__(self, path, pi_id=1):
        """
        Class visionHandler: Read and Process images remotely.
        ---
        Parameters:
        @param: pi_id, integer, raspberry pi module id: 1, 2, ..., 6.
        @param: path, string, the path to save the image locally on PC.
        """
        self.pi_id = pi_id
        self.path = path
        self.com = communicator('192.168.0.{}0'.format(pi_id), 'pi{}'.format(pi_id), '000000')
        self.humanAction = False
        self.hand = False
        self.worldState = {
        # First column
        'ws_11': 'g',
        'ws_12': 'g',
        'ws_13': 'g',
        'ws_14': 'g',
        # Second column
        'ws_21': 'g',
        'ws_22': 'g',
        'ws_23': 'g',
        'ws_24': 'g',
        # Third column
        'ws_31': 'g',
        'ws_32': 'g',
        'ws_33': 'g',
        'ws_34': 'g',
        # Fourth column
        'ws_41': 'g',
        'ws_42': 'g',
        'ws_43': 'g',
        'ws_44': 'g',
        # Swap
        's1'   : 'g',
        's2'   : 'g',
        's3'   : 'g'
        }
        self.humanStock = {
        'b_2x2': 1,
        'b_2x4': 1,
        'y_2x2': 1,
        'y_2x4': 1
        }
        
    def captureWorld(self):
        """
        Function: captureWorld, to capture an image of the workspace/swap and analyse the locations.
        ---
        Parameters:
        @param: None
        ---
        @return: None
        """
        # capture an image.
        self.com.getImage(self.path)

        # Process the image.
        proc = imageProcessor(self.path)
        proc.stateAnalyzer()
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
        self.com.getImage(self.path)
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
            print('detected', detected)
            tic = time()
            self.com.getImage(self.path)
            toc = time()
            if verbose:
                print('time for getting the image is: ', round(toc-tic, 3))
                tic = toc
            detected = proc.handDetector()

        print('Detected', detected)
        self.hand = False

#----------------------------------------------------------------------------------