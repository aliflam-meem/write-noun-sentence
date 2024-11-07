from ibm_watsonx_ai.foundation_models import Model

from src.core.json_response_parser import *
from src.core.output import append_string_to_file


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
        "max_new_tokens": 350,
        "stop_sequences": ["<end>"],
        "temperature": 0.8,
        "top_k": 40,
        "top_p": 0.9,
        "repetition_penalty": 1.08
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
def get_questions(model, _diff_level, _lvl_prep, _correct_example):
    lvl_prep = _lvl_prep
    diff_level =  _diff_level
    correct_example = _correct_example 
    prompt_input = f"""اكتب جملة مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية تناسب متعلم من المستوى {diff_level}.
    الجملة يجب أن تحتوي على حرف الجر الآتي: {lvl_prep} .
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    حرف جر من المذكور هو الإجابة الصحيحة.
    إذا كان حرف الجر هو : {lvl_prep} ، فالإجابة الصحيحة هي حرف الجر بالإضافة إلى الكلمة المجرورة التي تليه. : {correct_example}.
    اكتب حرف الجر في مكان الإجابة الصحيحة.
    شكل الخرج:
    اطبع الجملة sentence والإجابة الصحيحة correct_answer على شكل كيان JSON:
    <start>
    [
    ,{{ "sentence": "...", "correct_answer": "..." }}
    {{ "sentence": "...", "correct_answer": "..." }}
    ....
    ]
    <end>

    Input: اكتب جملة مشكولة صحيحة المعنى وصرف الكلمات باللغة العربية تناسب متعلم من المستوى المتقدم.
    الجملة يجب أن تحتوي على حرف الجر الآتي: ب.
    يمكن أن يأتي حرف الجر في بداية الجملة أو وسطها أو نهايتها.
    أجعل بعض الجمل تبدأ باسم وبعض الجمل الأخرى تبدأ بفعل. 
    حرف جر من المذكور هو الإجابة الصحيحة.
    إذا كان حرف الجر هو : ب ، فالإجابة الصحيحة هي حرف الجر بالإضافة إلى الكلمة المجرورة التي تليه. مثال: بالدماء.
    اكتب حرف الجر في مكان الإجابة الصحيحة.
    Output:"""


    print("Submitting generation request...")
    try:
        processed_response = None
        while processed_response == None:
            generated_response = model.generate_text(prompt=prompt_input)  # guardrails=False
            print("generated_response: ", generated_response)
            #if both keys don't get generated, regenerate again
            if "sentence" not in generated_response:
                append_string_to_file("Missing_sentence", "src/jar_bingo/assets/jar_bingo_questions.txt")
                continue
            if "correct_answer" not in generated_response:
                append_string_to_file("Missing_correct_answer", "src/jar_bingo/assets/jar_bingo_questions.txt")
                continue
            processed_response = parse_coupled_json_response(generated_response, "<start>", "<end>")
            print("processed_response:", processed_response)

    except IndexError as i:
        print("An error occurred:", i)
    except Exception as e:
        print("An error occurred:", e)
    output_string = processed_response[0].get("sentence")+"/"+ processed_response[0].get("correct_answer")
    print(output_string)
    append_string_to_file(output_string, "src/jar_bingo/assets/jar_bingo_content_ver2.txt")
    return processed_response[0]
