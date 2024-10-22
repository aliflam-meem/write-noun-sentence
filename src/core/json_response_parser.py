import json
import re

import pygame

from src.jar_bingo.settings import F_Arial, BLACK


# in: list, out: reshaped list
def list_parser(arabic_list):
    message_font = pygame.font.Font(F_Arial, 35)
    message_font.set_script("Arab")
    message_font.set_direction(pygame.DIRECTION_RTL)
    reshaped_list = []
    for i in arabic_list:
        message_text = message_font.render(i, True, BLACK)
        reshaped_list.append(message_text)
        # print("reshaped the following item: ",reshaped_item)
    return reshaped_list


# in string, out: reshaped string
def string_parser(arabic_string):
    reshaped_string = ""
    message_font = pygame.font.Font(F_Arial, 35)
    message_font.set_script("Arab")
    message_font.set_direction(pygame.DIRECTION_RTL)
    reshaped_string = message_font.render(arabic_string, True, BLACK)
    # print("reshaped the following item: ",reshaped_string)
    return reshaped_string


def parse_dict_list(string, start_marker="<start>", end_marker="<end>"):
def parse_json_response(string, start_marker, end_marker):
    """Parses a string containing a list of dictionaries into a Python list.
    Args:             string: The input string.
                      start_marker: the string which marks the start of the json object.
                      end_marker: the string which marks the end of the json object.
    Returns:            A list of dictionaries.
    """
    dict_list = []
    # Remove leading and trailing spaces from the response
    # string = string.encode('utf-8').decode('utf-8').strip()
    # Remove extra tags and brackets.
    string = string.replace(start_marker, "").replace(end_marker, "") \
        .replace(" [", "[").replace("[ ", "[").replace(" ]", "]").replace(
        "] ", "]").replace("\n", "").replace("\t", "")
    string = re.sub(' +', " ", string)

    # print("string : ", string)
    search = json.dumps(string)
    # print(search)
    # dict_str = string.split(",")
    # print("dict_str : ", dict_str)
    data = json.loads(search)
    data = json.loads(data)
    print("data : ", data)
    print(type(data))
    return data
