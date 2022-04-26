#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import os
import webbrowser
import requests
import json
import rospy
from std_msgs.msg import String
import rospkg
import csv
from signal import signal, SIGINT
from sys import exit
from termcolor import colored
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def cb_output(data):
    screen_num = int(data.data)
    if screen_num == 999:
        os.system("pkill -9 -ef chrome")
    else:
        name_list = ["1_물다.jpg", "2_찌르다_검정.jpg", "3_다시듣기.jpg", "4_찌르다_노랑.jpg", "5_본실험시작.jpg", "6_묶다.jpg", "7_쫒다.jpg", "8_흔들다.jpg"]
        base_url = "https://raw.githubusercontent.com/hyeonukbhin/deeptask_testbench/master/scripts/sct_screen/"
        # "https://raw.githubusercontent.com/hyeonukbhin/deeptask_testbench/master/scripts/sct_screen/1_%EB%AC%BC%EB%8B%A4.jpg"
        url = "{}{}".format(base_url, name_list[screen_num])
        webbrowser.get(using='google-chrome').open_new(url)


def termination_handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    # webbrowser.
    exit(0)


def main():
    rospy.init_node('dummy_sct', anonymous=False)
    rospy.Subscriber("dummy_sct", String, cb_output)

    rospy.spin()


if __name__ == '__main__':
    signal(SIGINT, termination_handler)

    main()
