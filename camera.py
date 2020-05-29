# -*- coding: utf-8 -*-
import requests
from PIL import Image
import io
import numpy as np
import cv2  # added to display image
import os   # added to allow saving files to directory
from time import strftime  # for adding timestamp 
from time import localtime # to images
import paramiko
from paramiko import SSHClient
from scp import SCPClient

from globals2 import *
#from globalvariables import *

from angle_estimator.AngleEstimator import AngleEstimator

estimator = AngleEstimator(resize_factor = 1.0, crop_factor = 0.5, max_pattern_size = [4,3], min_pattern_size = [4,3])

def captureimagechanl_0():
    print('Starting Chan 0')
    address = 'http://' + IP + PORT
    r = requests.post(address + '/cmd/getwarpsnap/post/0/')
    if r.status_code == 200:
        img = np.array(Image.open(io.BytesIO(r.content)), dtype=np.uint8)
    else:
        return False


    # # resize image  (It has been dropped since the angle estimator resizes internally)
    # scale_percent = 60
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    # dim = (width, height)    
    # resized_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)


    ############################ Angle Estimator Code ###############################
    angle, p1, p2 = estimator.Estimate(img)
    if angle is None or p1 is None or p2 is None:
        print('Fail!')
    else:   
        print('Success! angle = ' + str(angle))
        img = estimator.RenderResult(img, angle, p1, p2)
    #################################################################################


   # cv2.imshow('SVP Right-side sensor 0 (click "X" to close window and save file to \svp_images subdirectory)', resized_img)
   # cv2.waitKey(0) & 0xFF  # pause to view picture
    # save image
    root_path = os.getcwd()
    img_path = os.path.join(root_path, 'svp_images')
    imgtimestamp = str(strftime("%Y-%m-%d_%H-%M-%S", localtime()))
    saveimg = img_path + "\SVP_Channel_0_" + imgtimestamp + ".tif"
    #print(saveimg)
    cv2.imwrite(saveimg, img)
    return True
    
    

def captureimagechanl_1():
    print('Starting Chan 1')
    address = 'http://' + IP + PORT
    r = requests.post(address + '/cmd/getwarpsnap/post/1/')
    if r.status_code == 200:
        img = np.array(Image.open(io.BytesIO(r.content)), dtype=np.uint8)
    else:
        return False
    #print(r)
    #print(im)
    
    # # resize image (It has been dropped since the angle estimator resizes internally)
    # scale_percent = 60
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    # dim = (width, height)    
    # resized_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    
    ############################ Angle Estimator Code ###############################
    angle, p1, p2 = estimator.Estimate(img)
    if angle is None or p1 is None or p2 is None:
        print('Fail!')
    else:   
        print('Success! angle = ' + str(angle))
        img = estimator.RenderResult(img, angle, p1, p2)
    #################################################################################


  #  cv2.imshow('SVP Left-side sensor 1 (click "X" to close window and save file to \svp_images subdirectory)', resized_img)
  #  cv2.waitKey(0) & 0xFF  # pause to view picture
    # save image
    root_path = os.getcwd()
    img_path = os.path.join(root_path, 'svp_images')
    imgtimestamp = str(strftime("%Y-%m-%d_%H-%M-%S", localtime()))
    saveimg = img_path + "\SVP_Channel_1_" + imgtimestamp + ".tif"
    #print(saveimg)
    cv2.imwrite(saveimg, img)
    return True
    
'''
#
#  not used to capture image
#
def listfiles():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=IP, username=USERNAME, password=PASSWORD)
    check = 'ls -la'
    stdin, stdout, stderr = ssh_client.exec_command("ls -la " +PATH)
    for line in stdout:
        print('...' + line.strip('\n'))
    print(stdout.readlines())
    print(stderr.readlines())
    ssh_client.close()

def findfile():
    global gImageFilename
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=IP, username=USERNAME, password=PASSWORD)
    stdin, stdout, stderr = ssh_client.exec_command(
    "ls -t " + FILE_NAME + " | head -n 1")
    for line in stdout:
        print('...' + line.strip('\n'))
        gImageFilename = line.strip('\n')
    print(gImageFilename)
    print(stdout.readlines())
    print(stderr.readlines())
    ssh_client.close()

def copyfile():
    global gImageFilename
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=IP, username=USERNAME, password=PASSWORD)
    with SCPClient(ssh.get_transport()) as scp:
        scp.get(gImageFilename, preserve_times=True)
    print(gImageFilename)
    #print("Current File Name: ", os.path.realpath(__file__))
    ssh.close()
    scp.close()
'''
######################
# main()
######################
if __name__ == '__main__':    
    while True:
        ret  = captureimagechanl_0()
        #ret = captureimagechanl_1()
        if ret == False:
            break
 
