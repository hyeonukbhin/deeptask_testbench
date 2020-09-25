#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
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

    try :
        json_dict = json.loads(data.data)
        if check_address(json_dict, "ETRI", "UOS", "human_recognitiopn"):
            print('Output Topic Name : {}'.format(colored("/recognitionResult", 'white', attrs=['bold'])))
            print('From : {}'.format(colored("[M2-1] ETRI Short-term Sociality Recognizer", 'blue', attrs=['bold'])))
            json_string = json.dumps(json_dict, ensure_ascii=False, indent=4)
            print(json_string)

        if check_address(json_dict, "perception", "planning", "human_personality"):
            print('Output Topic Name : {}'.format(colored("/recognitionResult", 'white', attrs=['bold'])))
            print('From : {}'.format(colored("[M2-4] KIST Personality Recognizer", 'blue', attrs=['bold'])))
            print(data.data)

        if check_address(json_dict, "dialog", "planning", "dialog_generation"):
            print('Output Topic Name : {}'.format(colored("/taskCompletion", 'white', attrs=['bold'])))
            print('From : {}'.format(colored("[M2-6] HY Dialogue Generator", 'blue', attrs=['bold'])))
            print(data.data)

        if check_address(json_dict, "dialog", "planning", "dialog_intent"):
            print('Output Topic Name : {}'.format(colored("/dialog_intent", 'white', attrs=['bold'])))
            print('From : {}'.format(colored("[M2-7] HY Intention Classifier", 'blue', attrs=['bold'])))
            print(data.data)
    except ValueError : 
        pass






def termination_handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

def get_header(json_dict):
    source = json_dict["header"]["source"]
    target_list = json_dict["header"]["target"]
    content_list = json_dict["header"]["content"]

    return source, target_list, content_list


def check_address(json_dict, source, target, content):
    source_from_json = json_dict["header"]["source"]
    target_list_from_json = json_dict["header"]["target"]
    content_list_from_json = json_dict["header"]["content"]
    if (source == source_from_json) and (target in target_list_from_json) and (content in content_list_from_json):
        output = True
    else:
        output = False

    return output



def main():
    rospy.init_node('output_listener', anonymous=False)
    rospy.Subscriber("recognitionResult", String, cb_output)
    rospy.Subscriber("dialog_intent", String, cb_output)
    rospy.Subscriber("taskCompletion", String, cb_output)

    rospy.spin()


if __name__ == '__main__':
    signal(SIGINT, termination_handler)

    main()


