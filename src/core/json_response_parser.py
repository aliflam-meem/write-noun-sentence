import ast
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


def parse_coupled_json_response(string, start_marker, end_marker):
    """Parses a string containing a list of dictionaries into a Python list.
    Args:             string: The input string.
                      start_marker: the string which marks the start of the json object.
                      end_marker: the string which marks the end of the json object.
    Returns:            A list of dictionaries.
    """
    # Remove leading and trailing spaces from the response
    string = string.encode('utf-8').decode('utf-8').strip()
    # Remove extra tags and brackets.
    #print("parse json response function, before calling slplit:", string)
    string = split_response_string(string, start_marker, end_marker)
    try:
        json_response = json.loads(string)
        print(json_response)
        parsed_dict = json_response
        print("json parsed parsed_dict", parsed_dict)
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        string = string.replace(start_marker, "").replace(end_marker, "").replace(" [", "").replace("[ ", "").replace(" ]",
                                                                                                            "").replace(
        "] ", "").replace("]", "").replace("[", "").replace("\n", "").replace("'","")

        print("parse json response, before looping: ", string)
        # Parse the string using ast.literal_eval()
        i = 0
        #if LLM returned the json object correctly having both sentence and correct answer
        try:
            parsed_dict = ast.literal_eval(f'""{string}""')
            print("dictionary length",len(parsed_dict.items))
            print(parsed_dict[0], parsed_dict[1])
            removed_prep_sentence_dict = add_ablank_inthe_sentence(parsed_dict)
            parsed_dict = removed_prep_sentence_dict
        except Exception:
            parsed_dict=[]
            d = {}
            d["sentence"] = "لقد حدث خطأ في توليد السؤال ):"
            parsed_dict.append(d)
            d["correct_answer"] = "لقد حدث خطأ في توليد الإجابة ):"
            parsed_dict.append(d)

    print("returned dict: ", parsed_dict)
    return parsed_dict


def parse_specific_json_response(string, start_marker="<start>", end_marker="<end>"):
    """Parses a string containing a list of dictionaries into a Python list.
    Args:             string: The input string.
                      start_marker: the string which marks the start of the json object.
                      end_marker: the string which marks the end of the json object.
    Returns:            A list of dictionaries.
    """
    # Remove leading and trailing spaces from the response
    string = get_substring_delimited_by(string, start_marker, end_marker)
    # print("string after slicing")
    # print(string)
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

def add_ablank_inthe_sentence(parsed_dict):
    """
    Takes the question dictionary, edit the question to include a blank space and returns the whole dictionary.
    """
    sentence= parsed_dict["sentence"]
    prep = parsed_dict["correct_answer"]
    sentence = sentence.replace(prep, "___")
    parsed_dict["sentence"] = sentence
    return parsed_dict
