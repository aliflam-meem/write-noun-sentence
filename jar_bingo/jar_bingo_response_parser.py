import arabic_reshaper
from bidi.algorithm import get_display

#in: list, out: reshaped list
def list_parser(arabic_list):
    reshaped_list = []
    for i in arabic_list:
        reshaped_item = arabic_reshaper.reshape(i)
        reshaped_list.append(get_display(reshaped_item))
        #print("reshaped the following item: ",reshaped_item)
    return reshaped_list

#in string, out: reshaped string
def string_parser(arabic_string):
    reshaped_string = ""
    reshaped_item = arabic_reshaper.reshape(arabic_string)
    reshaped_string = get_display(reshaped_item)
    #print("reshaped the following item: ",reshaped_string)
    return reshaped_string


def parse_dict_list(string):
    """Parses a string containing a list of dictionaries into a Python list.
    Args:             string: The input string.
    Returns:            A list of dictionaries.
    """
    dict_list = []
    # Remove leading and trailing spaces from the response
    string = string.encode('utf-8').decode('utf-8').strip()
    # Remove extra tags and brackets.
    string = string.replace("<start>", "").replace("<end>", "").replace(" [", "").replace("[ ", "").replace(" ]", "").replace("] ", "").replace("]", "").replace("[", "")
    dict_str = string.split(",")
    i=0
    while i < len(dict_str)-1:
        key_value_pairs = dict_str[i].split(":")
        d = {}
        key = key_value_pairs[0].strip().replace(" ","").replace("'","").replace('"','').replace("{","").replace("}","")
        value = key_value_pairs[1].strip().replace("'","").replace('"','').replace("{","").replace("}","")
        d[key] = value
        dict_list.append(d)
        i +=1
    return dict_list
