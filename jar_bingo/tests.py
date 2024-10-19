from json_response_parser import *

string_data = '[{"name": "Alice", "age": 30}, "name": "Bob", "age": 25},]'
parsed_data = parse_dict_list(string_data)
print(parsed_data)
for d in parsed_data:
    if d.get("name"):
        print("name: ",d.get("name"))

# {"name": "Bob", "age": 25}, {"name": "Charlie", "age": 35}