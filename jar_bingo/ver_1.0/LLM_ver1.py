import json
import os
import time
import requests
from requests.exceptions import RequestException
from ibm_watsonx_ai.foundation_models import Model
from response_parser import *

#watsonx API connection¶
#This cell defines the credentials required to work with watsonx API for Foundation Model inferencing.
#Action: Provide the IBM Cloud personal API key. For details, see documentation.
def get_credentials():
	return {
		"url" : "https://eu-de.ml.cloud.ibm.com",
		"apikey" : input("Please enter your api key (hit enter): ")
	}

def set_model():
    #Defining the model id
    model_id = "sdaia/allam-1-13b-instruct"
    #Defining the model parameters
    parameters = {
        "decoding_method": "sample",
        "max_new_tokens": 350,
        "stop_sequences": ["<end>"],
        "temperature": 0.9,
        "top_k": 40,
        "top_p": 0.9,
        "repetition_penalty": 1.08
    }
    #Defining the project id or space id
    project_id = input("PROJECT_ID")
    #Defining the Model object
    model = Model(
        model_id = model_id,
        params = parameters,
        credentials = get_credentials(),
        project_id = project_id,
        )
    return model

#Defining the inferencing input

def get_question_(lvl_prep, sentence_count, correct_example, with_jar = ""):
     return "اكتب 4 جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية."


def get_questions(model, _lvl_prep, _sentence_count, _correct_example, _with_jar):
    lvl_prep = _lvl_prep
    sentence_count = _sentence_count
    correct_example = _correct_example
    with_jar = _with_jar
    prompt_input = f"""اكتب {sentence_count} جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية.
    الجملة يجب أن تحتوي على حرف الجر الآتي: {lvl_prep} .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    استبدل حرف جرٍ واحدٍ في كل جملة بفراغ واحد مكانه، هذا الفراغ هو لحرف جر من المذكور. كما أن هذا الحرف هو الإجابة الصحيحة.
    إذا كان حرف الجر هو :  {lvl_prep} ، فالإجابة الصحيحة هي حرف الجر {with_jar}. مثال: {correct_example}.
    يجب أن يتماثل حرف الجر في الجملة وحرف الجر في الإجابة الصحيحة.
    اكتب الجملة بحيث يكون للفراغ إجابة واحدة صحيحة فقط وهي حرف الجر المذكور.
    اكتب حرف الجر المستبدل في الجملة في مكان الإجابة الصحيحة.
    شكل الخرج:
    اطبع الجملة sentence والإجابة الصحيحة correct_answer على شكل كيان JSON:
    <start>
    [
    ,{{ "sentence": "...", "correct_answer": "..." }}
    {{ "sentence": "...", "correct_answer": "..." }}
    ....
    ]
    <end>


    Input: اكتب 4 جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية.
    الجملة يجب أن تحتوي على حرف الجر الآتي: ب .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    استبدل حرف جرٍ واحدٍ في كل جملة بفراغ واحد مكانه، هذا الفراغ هو لحرف جر من المذكور. كما أن هذا الحرف هو الإجابة الصحيحة.
    إذا كان حرف الجر هو :  ب ، فالإجابة الصحيحة هي حرف الجر بالإضافة إلى الكلمة المجرورة التي تليه. مثال: بالدماء .
    يجب أن يتماثل حرف الجر في الجملة وحرف الجر في الإجابة الصحيحة.
    اكتب الجملة بحيث يكون للفراغ إجابة واحدة صحيحة فقط وهي حرف الجر المذكور.
    اكتب حرف الجر المستبدل في الجملة في مكان الإجابة الصحيحة.

    Output:  <start>
    [
    {{ "sentence": "تسابق الفرسان _ نزاهة.", "correct_answer": "بنزاهةٍ" }},
        {{ "sentence": "فاز الفارس _ السباقِ.", "correct_answer": "بالسباقِ" }},
    {{ "sentence": "اذهبْ _ سلامٍ.", "correct_answer": "بسلامٍ" }},
        {{ "sentence": "أكل التفاحة _ القشرة.",  "correct_answer": "بلا قشرة" }},
    ]
    <end>


    Input: اكتب 3 جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية.
    الجملة يجب أن تحتوي على حرف الجر الآتي: عن .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    استبدل حرف جرٍ واحدٍ في كل جملة بفراغ واحد مكانه، هذا الفراغ هو لحرف جر من المذكور. كما أن هذا الحرف هو الإجابة الصحيحة.
    إذا كان حرف الجر هو :  عن ، فالإجابة الصحيحة هي حرف الجر . مثال: عن.
    يجب أن يتماثل حرف الجر في الجملة وحرف الجر في الإجابة الصحيحة.
    اكتب الجملة بحيث يكون للفراغ إجابة واحدة صحيحة فقط وهي حرف الجر المذكور.
    اكتب حرف الجر المستبدل في الجملة في مكان الإجابة الصحيحة.
    Output: <start>
    [
    {{ "sentence": "سأل المعلم _ الواجب.", "correct_answer": "عن" }},
    {{ "sentence": " _ قريبٍ ستُدرِكُ الحقيقة.", "correct_answer": "عن" }},
    {{ "sentence": " غبت _ الدار ساعة.", "correct_answer": "عن" }},
    ]
    <end>

    Input: اكتب 2 جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية.
    الجملة يجب أن تحتوي على حرف الجر الآتي: ك .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    استبدل حرف جرٍ واحدٍ في كل جملة بفراغ واحد مكانه، هذا الفراغ هو لحرف جر من المذكور. كما أن هذا الحرف هو الإجابة الصحيحة.
    إذا كان حرف الجر هو :  ك ، فالإجابة الصحيحة هي حرف الجر بالإضافة إلى الكلمة المجرورة التي تليه. مثال: كالبرق .
    يجب أن يتماثل حرف الجر في الجملة وحرف الجر في الإجابة الصحيحة.
    اكتب الجملة بحيث يكون للفراغ إجابة واحدة صحيحة فقط وهي حرف الجر المذكور.
    اكتب حرف الجر المستبدل في الجملة في مكان الإجابة الصحيحة.
    Output:  <start>
    [
    {{ "sentence": "السماء زرقاء _ البحرِ.",  "correct_answer": "كالبحرِ" }},
    {{ "sentence": "السماء زرقاء _ البحرِ.", "correct_answer": "كالبحرِ" }},
    {{ "sentence": "_ أنك توأمُهُ الشقيق.",  "correct_answer": "كأنك" }},
    ]
    <end>


    Input: اكتب 1 جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية.
    الجملة يجب أن تحتوي على حرف الجر الآتي: على .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    استبدل حرف جرٍ واحدٍ في كل جملة بفراغ واحد مكانه، هذا الفراغ هو لحرف جر من المذكور. كما أن هذا الحرف هو الإجابة الصحيحة.
    إذا كان حرف الجر هو :  على ، فالإجابة الصحيحة هي حرف الجر . مثال: على.
    يجب أن يتماثل حرف الجر في الجملة وحرف الجر في الإجابة الصحيحة.
    اكتب الجملة بحيث يكون للفراغ إجابة واحدة صحيحة فقط وهي حرف الجر المذكور.
    اكتب حرف الجر المستبدل في الجملة في مكان الإجابة الصحيحة.
    Output:  <start>
    [
    {{ "sentence": "كتب أحمد _ اللوح الأخضر.", "correct_answer": "على" }},
    ]
    <end>

    Input: اكتب 3 جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية.
    الجملة يجب أن تحتوي على حرف الجر الآتي: ل .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    استبدل حرف جرٍ واحدٍ في كل جملة بفراغ واحد مكانه، هذا الفراغ هو لحرف جر من المذكور. كما أن هذا الحرف هو الإجابة الصحيحة.
    إذا كان حرف الجر هو :  ل ، فالإجابة الصحيحة هي حرف الجر بالإضافة إلى الكلمة المجرورة التي تليه. مثال: للعمل .
    يجب أن يتماثل حرف الجر في الجملة وحرف الجر في الإجابة الصحيحة.
    اكتب الجملة بحيث يكون للفراغ إجابة واحدة صحيحة فقط وهي حرف الجر المذكور.
    اكتب حرف الجر المستبدل في الجملة في مكان الإجابة الصحيحة.
    Output:  <start>
    [
    {{ "sentence": "سافرتُ _ الدراسةِ والعمل.",  "correct_answer": "للدراسةِ" }},
    {{ "sentence": "السيف لي والسرجُ _ الفرس.",  "correct_answer": "للفرس" }},
    {{ "sentence": "يا _ الشرفاء.",  "correct_answer": "للشرفاء" }},
    ]
    <end>

    Input: اكتب 2 جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية.
    الجملة يجب أن تحتوي على حرف الجر الآتي: إلى .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    استبدل حرف جرٍ واحدٍ في كل جملة بفراغ واحد مكانه، هذا الفراغ هو لحرف جر من المذكور. كما أن هذا الحرف هو الإجابة الصحيحة.
    إذا كان حرف الجر هو :  إلى، فالإجابة الصحيحة هي حرف الجر . مثال: إلى.
    يجب أن يتماثل حرف الجر في الجملة وحرف الجر في الإجابة الصحيحة.
    اكتب الجملة بحيث يكون للفراغ إجابة واحدة صحيحة فقط وهي حرف الجر المذكور.
    اكتب حرف الجر المستبدل في الجملة في مكان الإجابة الصحيحة.
    Output: <start>
    [
        {{ "sentence": "أنا أحب الذهاب _ المدرسة.", "correct_answer": "إلى" }},
        {{ "sentence": "ضم هذا المال _ مالك.", "correct_answer": "إلى" }},
    ]
    <end>

    Input: اكتب 1 جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية.
    الجملة يجب أن تحتوي على حرف الجر الآتي: من .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    استبدل حرف جرٍ واحدٍ في كل جملة بفراغ واحد مكانه، هذا الفراغ هو لحرف جر من المذكور. كما أن هذا الحرف هو الإجابة الصحيحة.
    إذا كان حرف الجر هو :  من، فالإجابة الصحيحة هي حرف الجر . مثال: من.
    يجب أن يتماثل حرف الجر في الجملة وحرف الجر في الإجابة الصحيحة.
    اكتب الجملة بحيث يكون للفراغ إجابة واحدة صحيحة فقط وهي حرف الجر المذكور.
    اكتب حرف الجر المستبدل في الجملة في مكان الإجابة الصحيحة.
    Output: <start>
    [
        {{ "sentence": "قرأتُ سورة _ القرآن.", "correct_answer": "من" }},
    ]
    <end>

    Input: اكتب 2 جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية.
    الجملة يجب أن تحتوي على حرف الجر الآتي: في .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    استبدل حرف جرٍ واحدٍ في كل جملة بفراغ واحد مكانه، هذا الفراغ هو لحرف جر من المذكور. كما أن هذا الحرف هو الإجابة الصحيحة.
    إذا كان حرف الجر هو :  في ، فالإجابة الصحيحة هي حرف الجر . مثال: في .
    يجب أن يتماثل حرف الجر في الجملة وحرف الجر في الإجابة الصحيحة.
    اكتب الجملة بحيث يكون للفراغ إجابة واحدة صحيحة فقط وهي حرف الجر المذكور.
    اكتب حرف الجر المستبدل في الجملة في مكان الإجابة الصحيحة.
    Output: <start>
    [
        {{ "sentence": "سنبقى _ السيارة حتى يتوقف المطر.", "correct_answer": "في" }},
    {{ "sentence": "الغِنى كلُّه _ القناعة.", "correct_answer": "في" }},
    ]
    <end>

    Input: اكتب {sentence_count} جمل مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية.
    الجملة يجب أن تحتوي على حرف الجر الآتي: {lvl_prep} .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    استبدل حرف جرٍ واحدٍ في كل جملة بفراغ واحد مكانه، هذا الفراغ هو لحرف جر من المذكور. كما أن هذا الحرف هو الإجابة الصحيحة.
    إذا كان حرف الجر هو :  {lvl_prep} ، فالإجابة الصحيحة هي حرف الجر {with_jar}. مثال: {correct_example}.
    يجب أن يتماثل حرف الجر في الجملة وحرف الجر في الإجابة الصحيحة.
    اكتب الجملة بحيث يكون للفراغ إجابة واحدة صحيحة فقط وهي حرف الجر المذكور.
    اكتب حرف الجر المستبدل في الجملة في مكان الإجابة الصحيحة.
    Output:"""

    print("Submitting generation request...")
    #model = set_model()
    generated_response = model.generate_text(prompt=prompt_input) #guardrails=False
    print("generated_response", generated_response)
    # Remove spaces before "[" and after "]"
    processed_response = parse_dict_list(generated_response)
    print("processed_response:", processed_response)
    # try:
    #     json_response = json.loads(processed_response)
    #     print(json_response)
    # except json.decoder.JSONDecodeError as e:
    #      print(f"Error decoding JSON: {e}")
    return processed_response[0]


def get_prepositions_and_question():
    prepositions = ["in", "on", "at", "of", "to", "for", "with", "by", "from", "about"]
    quiz_questions = [
        "What preposition is used to indicate location inside something?",
        "What preposition is used to indicate location on a surface?",
        "What preposition is used to indicate a specific point in time or location?",
        "What preposition is used to indicate ownership or possession?",
        "What preposition is used to indicate movement or direction?",
        "What preposition is used to indicate purpose or reason?",
        "What preposition is used to indicate accompaniment or association?",
        "What preposition is used to indicate the agent of an action or means of transportation?",
        "What preposition is used to indicate origin or starting point?",
        "What preposition is used to indicate a topic or subject?"
    ]
