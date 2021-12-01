#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from termcolor import colored
import json
import rospy
from std_msgs.msg import String, ColorRGBA, Empty
from sensor_msgs.msg import JointState
import rospkg
import csv
from signal import signal, SIGINT
from sys import exit
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def cb_rgb():
    current_time = rospy.get_rostime()
    action_dict = {
        "header": {
            "timestamp": "1514956482.075935057",
            "source": "planning",
            "target": ["action"],
            "content": ["robot_action"]
        },
        "robot_action": {
            "id": 319,
            "sm": "greeting",
            "behavior": "action",
            "user": "test",
            "dialog": "hi."
        }
    }
    control_part = ["earL_led", "earR_led",
                    "torso_led", "lidar_led", "wheel_led"]
    c_white = [1.0, 1.0, 1.0, 0.0]
    c_red = [1.0, 0.0, 0.0, 0.0]
    c_green = [0.0, 1.0, 0.0, 0.0]
    c_blue = [0.0, 0.0, 1.0, 0.0]
    c_red_green = [1.0, 1.0, 0.0, 0.0]
    c_green_blue = [0.0, 1.0, 1.0, 0.0]
    c_blue_red = [1.0, 0.0, 1.0, 0.0]

    # if control_part == control_part[0]:

    pub_earL.publish(json_string)
    print('Input Topic Name : {}'.format(
        colored("/taskExecution", 'white', attrs=['bold'])))
    print(json_string)
    print("Press Enter to continue or Type exit to terminate")
    end_flag = raw_input("")
    # print('{}'.format(colored(json_string, 'white', attrs=['bold'])))


def cb_waiting():
    # RGB EAR BG

    pub_earL.publish(ColorRGBA(0.0, 1.0, 1.0, 0.0))
    pub_earR.publish(ColorRGBA(0.0, 1.0, 1.0, 0.0))

    msg = JointState()
    msg.header.stamp = rospy.Time.now()

    # msg.header.seq = 0
    # msg.header.stamp = {"secs": 0, "nsecs": 0}

    msg.name = ['']
    msg.position = [0.0, 0.0, 0.1, 0.0]
    msg.velocity = [0.3, 0.3, 1.3, 0.3]
    msg.effort = [0]
    pub_cmd_pos.publish(msg)

    rospy.sleep(2)
    pub_earL.publish(ColorRGBA(1.0, 1.0, 1.0, 0.0))
    pub_earR.publish(ColorRGBA(1.0, 1.0, 1.0, 0.0))

    msg = JointState()
    msg.header.stamp = rospy.Time.now()

    # msg.header.seq = 0
    # msg.header.stamp = {"secs": 0, "nsecs": 0}
    msg.name = ['']
    msg.position = [0.0, 0.0, 0.0, 0.0]
    msg.velocity = [0.3, 0.3, 0.3, 0.3]
    msg.effort = [0]
    pub_cmd_pos.publish(msg)


def terminal_loop():
    while True:
        print("=============================================")
        print("             wating test          ")
        print("=============================================")
        print("rgb test")
        print("wating_test")
        mode = int(raw_input("-> "))
        if mode == 1:
            cb_rgb()
        elif mode == 2:
            cb_waiting()


def termination_handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


def main():
    global pub_earL, pub_earR, pub_torso, pub_lidar, pub_wheel, pub_cmd_pos

    rospy.init_node('input_talker', anonymous=False)
    pub_earL = rospy.Publisher("earL_led", ColorRGBA, queue_size=100)
    pub_earR = rospy.Publisher("earR_led", ColorRGBA, queue_size=100)
    pub_torso = rospy.Publisher("torso_led", ColorRGBA, queue_size=100)
    pub_lidar = rospy.Publisher("lidar_led", ColorRGBA, queue_size=100)
    pub_wheel = rospy.Publisher("wheel_led", ColorRGBA, queue_size=100)
    pub_cmd_pos = rospy.Publisher("cmd_pos", JointState, queue_size=100)

    terminal_loop()
    rospy.spin()


if __name__ == '__main__':
    signal(SIGINT, termination_handler)
    main()
