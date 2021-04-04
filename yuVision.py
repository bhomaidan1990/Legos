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
from time import sleep
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

    def getImage(self, remotePath='vision/image.jpg', localPath):
        """
        Function: getImage, to copy the image from the Raspberry pi to a localPath in PC.
        ---
        Parameters:
        @param: remotePath, string, the path to the image on the Pi.
        @param: localPath, string, the path to the destination folder.
        ---
        @return: None.
        """
        transport = paramiko.Transport((host, port))
        transport.connect(username = self.username, password = self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remotePath, localPath+'image.jpg')

        sftp.close()
        transport.close()
        # print('Upload done.')

    def camController(self, val, keyfilename=None):
        """
        Function: camController, to control the camera capture status on the Raspberry pi.
        ---
        Parameters:
        @param: val, integer, 0 to exit the image capturing script, 2 to start capturing, 1 to stop capturing.
        @param: keyfilename, string, ssh key file name.
        ---
        @return: None.
        """
        if not val in [0, 1, 2]:
            print('please enter valid value: 0, 1, 2. any other values are not accepted!')
        else:
            if(keyfilename is None):
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname = self.host, username = self.username, password = self.password)
            else:
                k = paramiko.RSAKey.from_private_key_file(keyfilename) 
                # k = paramiko.DSSKey.from_private_key_file(keyfilename)
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=user, pkey=k)

            ftp  = ssh.open_sftp()
            file = ftp.file('vision/order', "w", -1)
            file.write(str(val))

            file.flush()
            ftp.close()
            ssh.close()

    def commander(self, cmd_to_execute, keyfilename=None):
        """
        Function: commander, to send commands to the Raspberry pi.
        ---
        Parameters:
        @param: cmd_to_execute, string, command to be excuted on the Raspberry pi.
        @param: keyfilename, string, ssh key file name.
        ---
        @return: None.
        """
        if(keyfilename is None):
            ssh = paramiko.SSHClient()
            ssh.connect(hostname = self.host, username = self.username, password = self.password)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
        else:
            k = paramiko.RSAKey.from_private_key_file(keyfilename) 
            # k = paramiko.DSSKey.from_private_key_file(keyfilename)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=user, pkey=k)

#======================
# class visionHandler |
#======================
class visionHandler():

    def __init__(self, pi_id, path):
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
        self.com.camController(1)
        self.com.commander('./vision/grabber.py')
        self.com.camController(2)
        self.com.getImage(self.path)
        self.com.camController(1)
        # Process the image.
        proc = imageProcessor(self.path)
        proc.stateAnalyzer()
        # write the colors to the worldState dictionary
        for key in proc.cellsState:
            self.worldState[proc.cellsState[key][0]] = proc.cellsState[key][1]
        for key in proc.swapState:
            self.worldState[proc.swapState[key][0]] = proc.swapState[key][1] 


    def captureHand(self):
        """
        Function: captureHand, to capture an image of the workspace/swap and check the human hand presence.
        ---
        Parameters:
        @param: None
        ---
        @return: hand, bool True if there is human hand, False if there is no human hand.
        """

        # capture an image.
        self.com.camController(2)
        self.com.commander('./vision/grabber.py')
        self.com.getImage(self.path)
        # Process the image.
        proc = imageProcessor(self.path)
        # check if there is human hand.
        while(proc.handDetector()):
            self.hand = True
            self.humanAction = True
            sleep(1)
            self.com.getImage(self.path)

        self.com.camController(1)
        self.hand = False

#----------------------------------------------------------------------------------

# path = 'F:/Grenoble/Semester_4/Project_Codes/Problem_Domain/New_Domain_Problem/'

# vh = visionHandler(path)
# vh.captureWorld()