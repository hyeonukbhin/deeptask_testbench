#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from os import wait
from termcolor import colored
import json
import rospy
from std_msgs.msg import String, ColorRGBA, Empty
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
from social_msgs.srv import SocialMotion, SocialMotionRequest, SocialMotionResponse

import rospkg
import csv
from signal import signal, SIGINT
from sys import exit
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class IntroPlay:

    def __init__(self):
        rospy.init_node('IntroPlay', anonymous=False)
        rospy.Subscriber("test", String, self.cb_test)
        self.pub_cmd_vel = rospy.Publisher("robot_beep", Twist, queue_size=100)
        self.srv_motion_play = rospy.ServiceProxy('/social_motion_player/play_motion', SocialMotion)
        print("Waiting sct_trigger service...")
        rospy.wait_for_service('/social_motion_player/play_motion')
        print("sct_service connection")

        rospy.spin()

    def cb_test(self, data):
        input_str = data.data
        if input_str == "0":
            file_name = "right_hand_wink"
            text = "안녕하세요 저는 노인지원 서비스로봇이에요"

            response_action = SocialMotionRequest(file_name=file_name, text=text, with_home=False)
            response_sct = self.srv_motion_play.call(response_action)
            print("motion played")
            print(response_sct)
        if input_str == "1":
            file_name = "right_hand_wink"
            text = "안녕하세요 저는 노인지원 서비스로봇이에요"
            response_action = SocialMotionRequest(file_name=file_name, text=text, with_home=False)
            response_sct = self.srv_motion_play.call(response_action)

            vel_msg = Twist()
            vel_msg.linear.x = 0.1
            vel_msg.linear.y = 0.1
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            self.pub_cmd_vel.publish(vel_msg)
            rospy.sleep(1)

            vel_msg = Twist()
            vel_msg.linear.x = 0
            vel_msg.linear.y = -0.1
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            self.pub_cmd_vel.publish(vel_msg)
            rospy.sleep(1)

            vel_msg = Twist()
            vel_msg.linear.x = -0.1
            vel_msg.linear.y = -0.1
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            self.pub_cmd_vel.publish(vel_msg)


def termination_handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


if __name__ == '__main__':
    signal(SIGINT, termination_handler)
    IntroPlay()
