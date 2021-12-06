#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# from pygame import mixer
from termcolor import colored
# import json
# import rospy
from std_msgs.msg import String, ColorRGBA, Empty
from sensor_msgs.msg import JointState
import rospkg
# import csv
from signal import signal, SIGINT
from sys import exit
import sys

from playsound import playsound

reload(sys)
sys.setdefaultencoding('utf-8')


def play_beep():
    SE_PACKAGE_PATH = rospkg.RosPack().get_path("deeptask_testbench")
    beep_file = SE_PACKAGE_PATH + "/scripts/beep_robot_start.wav"
    playsound(beep_file)

    # mixer.init()
    # mixer.music.load(beep_file)
    # mixer.music.play()
    # print("beep play")


play_beep()
