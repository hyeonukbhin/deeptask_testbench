#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import json
import rospy
from std_msgs.msg import String
import rospkg
import csv
from signal import signal, SIGINT
from sys import exit
import sys
import time
from std_msgs.msg import String, ColorRGBA, Empty, Bool
from sensor_msgs.msg import JointState


def send_speech(name, speech):
    msgs_dict = {}
    current_time = rospy.get_rostime()

    rospy.set_param("perception/is_speaking_human/data", True)
    rospy.set_param("perception/is_speaking_human/timestamp", time.time())
    msgs_dict = {
        "header": {
            "timestamp": "%i.%i" % (current_time.secs, current_time.nsecs),
            "source": "perception",
            "target": ["dialog", "planning"],
            "content": ["human_speech"]
        },
        "human_speech": {
            "name": name,
            "speech": "%s" % speech
        }
    }
    rospy.sleep(0.5)
    rospy.set_param("perception/is_speaking_human/data", False)
    rospy.set_param("perception/is_speaking_human/timestamp", time.time())

    json_string = json.dumps(msgs_dict, ensure_ascii=False, indent=4)
    pub_recog_topic.publish(json_string)


def callback_cmd(cmd_idx, speed=1):

    if cmd_idx == 1:
        print("True = 1")
        print("False = 1")

        tf_idx = int(input("-> "))
        if tf_idx == 1:

            rospy.set_param("/unknown_avail", True)

        if tf_idx == 2:

            rospy.set_param("/unknown_avail", False)

    if cmd_idx == 2:
        # 3.4, 2.5, 3.5, 4.6, 4.8
        # M, M, M, H ,H
        rospy.set_param("/root/master_node", "master_request")
        print("general_councelling = 1")
        print("check_exercise_ability = 2")
        print("health_councelling = 3")
        print("root/stand_by = 4")

        tf_idx = int(input("-> "))
        if tf_idx == 1:
            rospy.set_param("/root/master_node", "general_councelling")
        if tf_idx == 2:
            rospy.set_param("/root/master_node", "check_exercise_ability")
        if tf_idx == 3:
            rospy.set_param("/root/master_node", "health_councelling")
        if tf_idx == 4:
            rospy.set_param("/root/master_node", "stand_by")
    if cmd_idx == 3:
        # 3.4, 2.5, 3.5, 4.6, 4.8
        # M, M, M, H ,H
        rospy.set_param("/root/master_node", "master_request")
        rospy.sleep(2)
        rospy.set_param("/root/master_node", "sentence_completion_test")

        print("Countinue ? = 1")

        tf_idx = int(input("-> "))
        if tf_idx == 1:
            rospy.set_param("/sentence_completion_test/sct_initiation", "continue")

    if cmd_idx == 4:
        waiting_start

    if cmd_idx == 5:
        print("사용자의 이름을 입력해 주세요.")
        # test = input("-> ")
        # print(test)
        # print(type(test))

        user_name = str(input("-> "))

        print(user_name)
        while not rospy.is_shutdown():
            print("사용자의 발화문을 입력해 주세요.")
            speech = input("-> ")
            # name = str(name)
            send_speech(user_name, str(speech))
            print(str(speech))

            print("Press Enter to continue or Type exit to terminate")
            end_flag = input("")
            if end_flag == "exit":
                break


def terminal_loop():
    while True:
        print("=============================================")
        print("Select Command")
        print("1. Unknown 인식 가능/불가능                                 ")
        print("2. 마스터 노드 진입 이후 노드선택     ")
        print("3. SCT 시작 후 초기부분 패스        ")
        print("4. LED 초기화     ")
        print("5. stt                    ")
        mode = int(input("-> "))

        if mode == 1:
            callback_cmd(1)
        if mode == 2:
            callback_cmd(2, speed=1)
        if mode == 3:
            callback_cmd(3, speed=1)
        if mode == 4:
            callback_cmd(4, speed=1)
        if mode == 5:
            callback_cmd(5, speed=1)


def termination_handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


def demo_remote_handler():
    global pub_recog_topic
    global pub_earL, pub_earR, pub_torso, pub_lidar, pub_robot_gaze, pub_gaze_init

    rospy.init_node('demo_remote_handler', anonymous=False)
    # rospy.Subscriber("simulation_trigger", String, callback_cmd)
    pub_recog_topic = rospy.Publisher(
        "recognitionResult", String, queue_size=100)
    # pub_dialog_topic = rospy.Publisher("dialogResult", String, queue_size=100)
    # pub_task_topic = rospy.Publisher("taskCompletion", String, queue_size=100)
    # pub_recog_topic = rospy.Publisher("recognitionResult", String, queue_size=100)
    # rospy.Subscriber("taskResult", String, callback_task)
    # pub_task_topic = rospy.Publisher("taskExecution", String, queue_size=100)
    pub_earL = rospy.Publisher("earL_led", ColorRGBA, queue_size=100)
    pub_earR = rospy.Publisher("earR_led", ColorRGBA, queue_size=100)
    pub_torso = rospy.Publisher("torso_led", ColorRGBA, queue_size=100)
    pub_lidar = rospy.Publisher("lidar_led", ColorRGBA, queue_size=100)
    pub_robot_gaze = rospy.Publisher("robot_gaze", Bool, queue_size=100)
    pub_gaze_init = rospy.Publisher("init_joint", String, queue_size=100)

    terminal_loop()
    rospy.spin()
    # rospy.s


def waiting_end(up_down="up"):
    pub_earL.publish(ColorRGBA(1.0, 1.0, 1.0, 0.0))
    pub_earR.publish(ColorRGBA(1.0, 1.0, 1.0, 0.0))
    pub_torso.publish(ColorRGBA(1.0, 1.0, 1.0, 0.0))
    pub_lidar.publish(ColorRGBA(1.0, 1.0, 1.0, 0.0))

    pub_robot_gaze.publish(Bool(False))
    pub_gaze_init.publish(up_down)


if __name__ == '__main__':
    signal(SIGINT, termination_handler)

    demo_remote_handler()
