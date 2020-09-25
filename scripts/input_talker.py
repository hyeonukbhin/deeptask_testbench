#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import json
import rospy
from std_msgs.msg import String
import rospkg
import csv
from signal import signal, SIGINT
from sys import exit
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from termcolor import colored

def cb_dialog():
    current_time = rospy.get_rostime()
    dialog_dict = {
        'header': {
            'timestamp': '%i.%i' % (current_time.secs, current_time.nsecs),
            'target': ['dialog'],
            'content': ['dialog_generation'],
            'source': 'planning'
        },
        'dialog_generation': {
            'name': '이병현',
            'intent': 'transmit_information_health_advice',
            'id': 177,
            "human_speech": "좋아진 것 같아",
            'social_context': {'medicine_schedule': '식후 30분 후'}
        }
    }

    json_string = json.dumps(dialog_dict, ensure_ascii=False, indent=4)
    pub_input_dialog.publish(json_string)
    print('Input Topic Name : {}'.format(colored("/taskExecution", 'white', attrs=['bold'])))
    print(json_string)
    print("Press Enter to continue or Type exit to terminate")
    end_flag = raw_input("")
    # print('{}'.format(colored(json_string, 'white', attrs=['bold'])))


def cb_intent():
    while not rospy.is_shutdown():

        print("사용자의 발화문을 선택해 주세요.")
        print("1. 좋아진 것 같아")
        print("2. 설렁탕 먹었지")
        print("3. 잘잤지")

        speech_num = int(raw_input("-> "))
        # name = str(name)

        if speech_num == 1:
            user_speech = "좋아진 것 같아"
        elif speech_num == 2:
            user_speech = "설렁탕 먹었어"
        elif speech_num == 3:
            user_speech = "잘잤어"
        else:
            user_speech = ""

        current_time = rospy.get_rostime()

        json_frame = {
            "header": {
                "timestamp": "%i.%i" % (current_time.secs, current_time.nsecs),
                "source": "perception",
                "target": ["planning", "dialog"],
                "content": ["human_speech"]
            },
            "human_speech": {
                "name": "",
                "speech": user_speech
            }
        }

        json_string = json.dumps(json_frame, ensure_ascii=False, indent=4)
        pub_input_intent.publish(json_string)
        print('Input Topic Name : {}'.format(colored("/recognitionResult", 'white', attrs=['bold'])))
        print(json_string)


        print("Press Enter to continue or Type exit to terminate")
        end_flag = raw_input("")
        if end_flag == "exit":
            break


def terminal_loop():
    while True:
        print("=============================================")
        print("             2세부 Input Talker              ")
        print("=============================================")
        print("1. [M2-6] 발화생성기(HY) Input Topic Publish ")
        print("2. [M2-7] 의도추정기(HY) Input Topic Publish ")
        mode = int(raw_input("-> "))
        if mode == 1:
            cb_dialog()
        elif mode == 2:
            cb_intent()


def termination_handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

def main():
    global pub_input_intent
    global pub_input_dialog

    rospy.init_node('input_talker', anonymous=False)
    pub_input_intent = rospy.Publisher("recognitionResult", String, queue_size=100)
    pub_input_dialog = rospy.Publisher("taskExecution", String, queue_size=100)
    terminal_loop()
    rospy.spin()


if __name__ == '__main__':
    signal(SIGINT, termination_handler)
    main()
