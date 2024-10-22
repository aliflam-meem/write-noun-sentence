import pygame

# in: list, out: reshaped list
def list_parser(arabic_list, font, font_color): #list of strings, font_asset_path, rgb_color
    message_font = pygame.font.Font(font, 35)
    message_font.set_script("Arab")
    message_font.set_direction(pygame.DIRECTION_RTL)
    reshaped_list = []
    for i in arabic_list:
        message_text = message_font.render(i, True, font_color)
        reshaped_list.append(message_text)
        # print("reshaped the following item: ",reshaped_item)
    return reshaped_list


# in string, out: reshaped string
def string_parser(arabic_string, font, font_color): #string, font_asset_path, rgb_color
    reshaped_string = ""
    message_font = pygame.font.Font(font, 35)
    message_font.set_script("Arab")
    message_font.set_direction(pygame.DIRECTION_RTL)
    reshaped_string = message_font.render(arabic_string, True, font_color)
    # print("reshaped the following item: ",reshaped_string)
    return reshaped_string


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
