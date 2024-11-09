import json

from ibm_watsonx_ai.foundation_models import Model


# watsonx API connection¶
# This cell defines the credentials required to work with watsonx API for Foundation Model inferencing.
# Action: Provide the IBM Cloud personal API key. For details, see documentation.
def get_credentials():
    return {
        "url": "https://eu-de.ml.cloud.ibm.com",
        "apikey": "G7HLLKrhe-Zl2sJcYH9yF3MFs5E14Sj9zJhho_bvWE9B"
    }


def set_model():
    # Defining the model id
    model_id = "sdaia/allam-1-13b-instruct"
    # Defining the model parameters

    parameters = {
        "decoding_method": "sample",
        "max_new_tokens": 600,
        "stop_sequences": ["<end_json>"],
        "temperature": 0.6,
        "top_k": 50,
        "top_p": 1,
        "repetition_penalty": 1.09,
        "timeout": 60,
    }

    # Defining the project id or space id
    project_id = "404e8279-d931-4311-b13d-4327914f2b8c"  # input("PROJECT_ID: ")
    # Defining the Model object
    model = Model(
        model_id=model_id,
        params=parameters,
        credentials=get_credentials(),
        project_id=project_id,
    )
    return model


def load_whack_a_mole_data():
    try:
        # Defining the model id
        model_id = "sdaia/allam-1-13b-instruct"
        # Defining the model parameters
        parameters = {
            "decoding_method": "sample",
            "max_new_tokens": 600,
            "stop_sequences": ["<end>", "<end json>"],
            "repetition_penalty": 1,
            "temperature": 0.7,
            "top_p": 1,
            "timeout": 60
        }
        # Defining the project id or space id
        project_id = "404e8279-d931-4311-b13d-4327914f2b8c"
        # Defining the Model object
        model = Model(
            model_id=model_id,
            params=parameters,
            credentials=get_credentials(),
            project_id=project_id,
        )
        sentenses_count = """10"""

        prompt_input = f"""التزم بقواعد اللغة العربية في كتابة الجمل
        اطبع الجمل بتنسيق JSON كقائمة قواميس
        يجب أن يحتوي كل قاموس على 4 مفاتيح 'sentense', 'word', 'answer' , 'options'
        الكلمة word هي أحد كلمات الجملة وتمثل اسم أو فعل أو حرف جر
        لا تكرر الجمل
        في كل جملة اختر قسم مختلف من أقسام الكلام (اسم أو حرف جر أو فعل)

        اكتب 3 جمل مفيدة مشكولة باللغة العربية تكون فيها الكلمة word فعل أو حرف جر أو اسم
        <start json>
         [
        {{"sentence": "يجلسُ الطالبُ على المقعدِ", "word": "على", "answer": "حرف", "options": ["اسم", "حرف", "فعل"]}},
        {{"sentence": " يلعبُ الطفلُ في الحديقةِ.", "word": "يلعب", "answer": "فعل", "options": ["اسم", "حرف", "فعل"]}},
        {{"sentence": "السماءُ صافيةٌ", "word": "صافية", "answer": "اسم", "options": ["اسم", "حرف", "فعل"]}}
        ]
        <end json>

        اكتب 4 جمل مفيدة مشكولة باللغة العربية تكون فيها الكلمة word فعل أو حرف جر أو اسم
        <start json> 
         [
        {{"sentence": "يذهبُ الطالبُ إلى المدرسةِ", "word": "الطالبُ", "answer": "اسم", "options": ["اسم", "حرف", "فعل"]}},
        {{"sentence": "كتبَ أحمدُ الدرسَ", "word": "كتبَ", "answer": "فعل", "options": ["اسم", "حرف", "فعل"]}},
        {{"sentence": "لعبتُ في الحديقةِ", "word": "في", "answer": "حرف", "options": ["اسم", "حرف", "فعل"]}},
        {{"sentence": "الشمسُ ساطعةٌ", "word": "الشمسُ", "answer": "اسم", "options": ["اسم", "حرف", "فعل"]}}
        ]
        <end json>

        اكتب {sentenses_count} جمل مفيدة مشكولة باللغة العربية تكون فيها الكلمة word فعل أو حرف جر أو اسم"""

        allam_response = model.generate_text(prompt=prompt_input,
                                             guardrails=False)
        json_data = allam_response.replace("<start json>",
                                           "").replace("<end json>", "")
        quiz_data = json.loads(json_data)
        print(quiz_data)
        return quiz_data
    except Exception as e:
        print(f"Error: {str(e)}")
        return

'''
def add_tashkil():
    try:

        return
    except Exception as e:
        print(f"Error: {str(e)}")
        return
'''
