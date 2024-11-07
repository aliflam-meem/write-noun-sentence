from src.core.json_response_parser import *



string = "<start>[{'sentence': 'Alice 30', 'correct_answer': '30'}]<end>"
#string = string.find('<start>', '___', 0,10)
string = re.sub('<start>', '__', string, count=1, flags=0)
print (string)
# string = string.encode('utf-8').decode('utf-8').strip()
# # Remove extra tags and brackets.
# #print("parse json response function, before calling slplit:", string)
# string = split_response_string(string, "<start>", "<end>")
# json_response = json.loads(string)
# print(json_response)
# parsed_dict = json_response
# print("json parsed parsed_dict", parsed_dict)

# print("parse json response, before looping: ", string)
# # Parse the string using ast.literal_eval()
# i = 0
#     #if LLM returned the json object correctly having both sentence and correct answer
# parsed_dict = ast.literal_eval(f'""{string}""')
# print("dictionary length",len(parsed_dict.items))
# print(parsed_dict[0], parsed_dict[1])
# removed_prep_sentence_dict = add_ablank_inthe_sentence(parsed_dict)
# parsed_dict = removed_prep_sentence_dict
 
# #parsed_data = parse_coupled_json_response(string_data, "<start>","<end>")
# parsed_dict = parsed_dict[0]
# print(parsed_dict)

# sentence= parsed_dict["sentence"]
# prep = parsed_dict["correct_answer"]
# sentence = sentence.replace(prep, "___")
# parsed_dict["sentence"] = sentence
# print(sentence)
# # {"name": "Bob", "age": 25}, {"name": "Charlie", "age": 35}