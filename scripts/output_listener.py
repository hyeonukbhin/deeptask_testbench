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



'''
              "social_action": nSocialActionCode,     // -1: not recognized,
                                                        //  0:bitenail,                   
                                                        //  1: covering mouth with hands,
                                                        //  2: cheering up!, 3: finger heart sign,
                                                        //  4: OK sign, 5: crossing arms, 6: neutral
                                                        //  7: picking ears,
                                                        //  8: resting chin on a hand,
                                                        //  9: scratching head, 10: shake hands 
                                                        // 11: a thumb up, 12: touching nose
                                                        // 13: waving hand, 14: bowing 
'''

def convert_social_action_name(action_num):
    if action_num is -1:
        action_str = "not recognized"
    elif action_num is 0:
        action_str = "bitenail"
    elif action_num is 1:
        action_str = "covering mouth with hands,"
    elif action_num is 2:
        action_str = "cheering up!"
    elif action_num is 3:
        action_str = "finger heart sign"
    elif action_num is 4:
        action_str = "OK sign,"
    elif action_num is 5:
        action_str = "crossing arm"
    elif action_num is 6:
        action_str = "neutral"
    elif action_num is 7:
        action_str = "picking ears,"
    elif action_num is 8:
        action_str = "resting chin on a hand,"
    elif action_num is 9:
        action_str = "scratching head,"
    elif action_num is 10:
        action_str = "shake hands "
    elif action_num is 11:
        action_str = "a thumb up"
    elif action_num is 12:
        action_str = "touching nose"
    elif action_num is 13:
        action_str = "waving hand,"
    elif action_num is 14:
        action_str = "bowing"
    return action_str



def cb_output(data):
    try :

        json_dict = json.loads(data.data)

        if check_address(json_dict, "ETRI", "UOS", "human_recognitiopn"):
            print('Output Topic Name : {}'.format(colored("/recognitionResult", 'white', attrs=['bold'])))
            print('From : {}'.format(colored("[M2-1] ETRI Short-term Sociality Recognizer", 'blue', attrs=['bold'])))

    #	print(json_dict["human_recognition"][0]["social_action"])
            social_action_str = convert_social_action_name(int(json_dict["human_recognition"][0]["social_action"]))
            print('Social Action : {}'.format(colored(social_action_str, 'white', attrs=['bold'])))
            json_string = json.dumps(json_dict, ensure_ascii=False, indent=4)

            print(json_string)


        try :
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


