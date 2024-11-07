from ibm_watsonx_ai.foundation_models import Model

from src.core.json_response_parser import *
from src.core.output import append_string_to_file
from src.jar_bingo.data import prep_letter_example_and_rule_dict

# watsonx API connection¶
# This cell defines the credentials required to work with watsonx API for Foundation Model inferencing.
# Action: Provide the IBM Cloud personal API key. For details, see documentation.
def get_credentials():
    return {
        "url": "https://eu-de.ml.cloud.ibm.com",
        "apikey": "Wse6HoPd7HSMBpK5auMPuYM5c3B1zFeiNTJnfg06q59I" #input("Please enter your api key (hit enter): ")
    }


def set_model():
    # Defining the model id
    model_id = "sdaia/allam-1-13b-instruct"
    # Defining the model parameters
    parameters = {
        "decoding_method": "sample",
        "max_new_tokens": 200,
        "stop_sequences": ["<end>"],
        "temperature": 0.72,
        "top_k": 45,
        "top_p": 0.98,
        "repetition_penalty": 1.03
    }
    # Defining the project id or space id
    project_id = "a9606b37-4f21-492c-90f2-ac1873e40946" #input("PROJECT_ID")
    # Defining the Model object
    model = Model(
        model_id=model_id,
        params=parameters,
        credentials=get_credentials(),
        project_id=project_id,
    )
    return model


# Defining the inferencing input
def get_questions(model, _diff_level, _lvl_prep):
    diff_level =  _diff_level 
    lvl_prep =  _lvl_prep 
    prep_letter_example_and_rule = ""
    if _lvl_prep == 'ب':
        prep_letter_example_and_rule = prep_letter_example_and_rule_dict['ب']
    elif _lvl_prep == 'ل':
        prep_letter_example_and_rule = prep_letter_example_and_rule_dict['ل']
    elif _lvl_prep == 'ك':
        prep_letter_example_and_rule = prep_letter_example_and_rule_dict['ك']

    prompt_input = f"""أحرف الجر: من، إلى، عن، على، ك، ل، ب.
    اكتب جملة منطقية، صحيحة المعنى وصرف الكلمات، مشكولة باللغة العربية تناسب متعلم من المستوى {diff_level}.
    الجملة يجب أن تحتوي على حرف الجر الآتي: {lvl_prep} .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    اكتب حرف الجر المذكور في مكان الإجابة الصحيحة.
    {prep_letter_example_and_rule}
    شكل الخرج:
    اطبع الجملة sentence والإجابة الصحيحة correct_answer على شكل كيان JSON:
    <start>
    [{{ "sentence": "...", "correct_answer": "..." }}]
    <end>


    Input: اكتب جملة منطقية، صحيحة المعنى وصرف الكلمات، مشكولة، باللغة العربية تناسب متعلم من المستوى المبتدئ.
    الجملة يجب أن تحتوي على حرف الجر الآتي: على.
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    اكتب حرف الجر المذكور في مكان الإجابة الصحيحة.
    Output: <start>
    [{{
    "sentence": "جلس الطفل على الكرسي",
    "correct_answer": "على"
    }}]
    <end>

    Input: اكتب جملة منطقية، صحيحة المعنى وصرف الكلمات، مشكولة، باللغة العربية تناسب متعلم من المستوى المتقدم.
    الجملة يجب أن تحتوي على حرف الجر الآتي: ل.
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    اكتب حرف الجر المذكور في مكان الإجابة الصحيحة.
    إذا كان حرف الجر هو : ل، فالإجابة الصحيحة هي حرف الجر بالإضافة إلى الاسم المجرور الذي يليه. مثال: للطلاب.
    Output: <start>
    [{{
    "sentence": "أحببت أن أجلس على الشاطئ لأستمتع بمنظر البحر الجميل",
    "correct_answer": "لأستمتع"
    }}]
    <end>

    Input: اكتب جملة منطقية، صحيحة المعنى وصرف الكلمات، مشكولة، باللغة العربية تناسب متعلم من المستوى المتقدم.
    الجملة يجب أن تحتوي على حرف الجر الآتي: ب.
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    اكتب حرف الجر المذكور في مكان الإجابة الصحيحة.
    إذا كان حرف الجر هو : ب، فالإجابة الصحيحة هي حرف الجر بالإضافة إلى الاسم المجرور الذي يليه. مثال: بالدماء.
    Output: <start>
    [{{
    "sentence": "شعرت بالراحة عندما جلست تحت ظل الشجرة",
    "correct_answer": "بالراحة"
    }}]
    <end>

    Input: اكتب جملة منطقية، صحيحة المعنى وصرف الكلمات، مشكولة، باللغة العربية تناسب متعلم من المستوى المبتدئ.
    الجملة يجب أن تحتوي على حرف الجر الآتي: في.
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    اكتب حرف الجر المذكور في مكان الإجابة الصحيحة.
    Output: <start>
    [{{
    "sentence": "ذهبنا إلى المدرسة في الصباح الباكر",
    "correct_answer": "في"
    }}]
    <end>

    Input: اكتب جملة منطقية، صحيحة المعنى وصرف الكلمات، مشكولة، باللغة العربية تناسب متعلم من المستوى المتقدم.
    الجملة يجب أن تحتوي على حرف الجر الآتي: ك.
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    اكتب حرف الجر المذكور في مكان الإجابة الصحيحة.
    إذا كان حرف الجر هو : ك، فالإجابة الصحيحة هي حرف الجر بالإضافة إلى الاسم المجرور الذي يليه. مثال: كالفهد.
    Output: <start>
    [{{
    "sentence": "تحركت السيارة بسرعة كبيرة كسيارة رياضية",
    "correct_answer": "كسيارة"
    }}]
    <end>

    Input: اكتب جملة منطقية، صحيحة المعنى وصرف الكلمات، مشكولة، باللغة العربية تناسب متعلم من المستوى المبتدئ.
    الجملة يجب أن تحتوي على حرف الجر الآتي: إلى.
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    اكتب حرف الجر المذكور في مكان الإجابة الصحيحة.
    Output: <start>
    [{{
    "sentence": "وصل الطالب إلى الفصل متأخرا",
    "correct_answer": "إلى"
    }}]
    <end>

    Input: اكتب جملة منطقية، صحيحة المعنى وصرف الكلمات، مشكولة، باللغة العربية تناسب متعلم من المستوى المبتدئ.
    الجملة يجب أن تحتوي على حرف الجر الآتي: من.
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    اكتب حرف الجر المذكور في مكان الإجابة الصحيحة.
    Output: <start>
    [{{
    "sentence": "خرجت من البيت بعد أن تناولت الإفطار",
    "correct_answer": "من"
    }}]
    <end>

    Input: اكتب جملة منطقية، صحيحة المعنى وصرف الكلمات، مشكولة، باللغة العربية تناسب متعلم من المستوى المتقدم.
    الجملة يجب أن تحتوي على حرف الجر الآتي: عن.
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    اكتب حرف الجر المذكور في مكان الإجابة الصحيحة.
    Output: <start>
    [{{
    "sentence": "تحدث المعلم عن أهمية القراءة وتنمية مهارات التفكير الناقد",
    "correct_answer": "عن"
    }}]
    <end>

    Input: اكتب جملة منطقية، صحيحة المعنى وصرف الكلمات، مشكولة، باللغة العربية تناسب متعلم من المستوى {diff_level}.
    الجملة يجب أن تحتوي على حرف الجر الآتي: {lvl_prep}.
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    اكتب حرف الجر المذكور في مكان الإجابة الصحيحة.
    {prep_letter_example_and_rule}
    Output:"""


    print("Submitting generation request...")
    prep_parts_list = []
    try:
        processed_response = None
        while processed_response == None:
            generated_response = model.generate_text(prompt=prompt_input)  # guardrails=False
            print("generated_response: ", generated_response)
            #if both keys don't get generated, regenerate again
            if "sentence" not in generated_response:
                append_string_to_file("Missing_sentence", "src/jar_bingo/assets/jar_bingo_questions.txt")
                print("in: if sentence not in generated_response:")
                generated_response = None
                continue
            elif "correct_answer" not in generated_response:
                append_string_to_file("Missing_correct_answer", "src/jar_bingo/assets/jar_bingo_questions.txt")
                generated_response = None
                print("in: elif correct_answer not in generated_response:")
                continue
            elif """correct_answer": "ب" """ in  generated_response or """correct_answer": "ك" """ in generated_response or """correct_answer": "ل" """ in generated_response:
                #incorrect correct_answer, generated only single_prep_letters
                processed_response = None
                append_string_to_file("Missing_correct_answer", "src/jar_bingo/assets/jar_bingo_questions.txt")
                generated_response = None
                print("in: elif correct_answer: ب in  generated_response or correct_answer")
                continue
            processed_response, prep_parts_list = parse_coupled_json_response(generated_response, "<start>", "<end>")
            print("processed_response:", processed_response)

    except IndexError as i:
        print("An error occurred:", i)
    except Exception as e:
        print("An error occurred:", e)
    print("processed_response",processed_response)
    output_string = processed_response.get("sentence")+"/"+ processed_response.get("correct_answer")
    print(output_string)
    append_string_to_file(output_string, "src/jar_bingo/assets/jar_bingo_content_ver2.txt")
    return processed_response, prep_parts_list
