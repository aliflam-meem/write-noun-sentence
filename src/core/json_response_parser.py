import json
import re

import pygame


# in: list, out: reshaped list
def list_parser(arabic_list, message_font, font_color): #list of strings, font_asset_path, rgb_color
    message_font.set_script("Arab")
    message_font.set_direction(pygame.DIRECTION_RTL)
    reshaped_list = []
    for i in arabic_list:
        message_text = message_font.render(i, True, font_color)
        reshaped_list.append(message_text)
        # print("reshaped the following item: ",reshaped_item)
    return reshaped_list


# in string, out: reshaped string
def string_parser(arabic_string, message_font, font_color): #string, font_asset_path, rgb_color
    reshaped_string = ""
    message_font.set_script("Arab")
    message_font.set_direction(pygame.DIRECTION_RTL)
    reshaped_string = message_font.render(arabic_string, True, font_color)
    # print("reshaped the following item: ",reshaped_string)
    return reshaped_string

def split_response_string(string, start_marker, end_marker):
    """Parses a string containing start and end markers, returning the split in the middle."""
    start_split_string = string.split(start_marker)
    end_split_string = start_split_string[1].split(end_marker)
    return end_split_string[0]


def parse_json_response(string, start_marker, end_marker):
    """Parses a string containing a list of dictionaries into a Python list.
    Args:             string: The input string.
                      start_marker: the string which marks the start of the json object.
                      end_marker: the string which marks the end of the json object.
    Returns:            A list of dictionaries.
    """
    dict_list = []
    # Remove leading and trailing spaces from the response
    string = string.encode('utf-8').decode('utf-8').strip()
    # Remove extra tags and brackets.
    string = split_response_string(string, start_marker, end_marker)
    string = string.replace(start_marker, "").replace(end_marker, "").replace(" [", "").replace("[ ", "").replace(" ]",
                                                                                                            "").replace(
        "] ", "").replace("]", "").replace("[", "")
    dict_str = string.split(",")
    i = 0
    while i < len(dict_str) - 1:
        key_value_pairs = dict_str[i].split(":")
        d = {}
        key = key_value_pairs[0].strip().replace(" ", "").replace("'", "").replace('"', '').replace("{", "").replace(
            "}", "")
        value = key_value_pairs[1].strip().replace("'", "").replace('"', '').replace("{", "").replace("}", "")
        d[key] = value
        dict_list.append(d)
        i += 1
    return dict_list


def parse_specific_json_response(string, start_marker="<start>", end_marker="<end>"):
    """Parses a string containing a list of dictionaries into a Python list.
    Args:             string: The input string.
                      start_marker: the string which marks the start of the json object.
                      end_marker: the string which marks the end of the json object.
    Returns:            A list of dictionaries.
    """
    # Remove leading and trailing spaces from the response
    string = get_substring_delimited_by(string, start_marker, end_marker)
    print("string after slicing")
    print(string)
    # Remove extra tags and brackets.
    string = string.replace(" [", "[").replace("[ ", "[").replace(" ]", "]").replace(
        "] ", "]").replace("\n", "").replace("\t", "")
    string = re.sub(' +', " ", string)

    search = json.dumps(string)
    data = json.loads(search)
    data = json.loads(data)
    print("data : ", data)
    print(type(data))
    return data


def get_substring_delimited_by(text, start_word, end_word):
    # Find the start and end index of the words
    start_index = text.find(start_word)
    end_index = text.find(end_word, start_index)

    # If start or end words are not found, return None
    if start_index == -1 or end_index == -1:
        return None

    # Adjust the start index to get the substring after 'start_word'
    start_index += len(start_word)

    # Extract the substring between the two words
    return text[start_index:end_index].strip()
