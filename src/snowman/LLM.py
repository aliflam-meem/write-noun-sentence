from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model

# watsonx API connection¶
# This cell defines the credentials required to work with watsonx API for Foundation Model inferencing.
# Action: Provide the IBM Cloud personal API key. For details, see documentation.
from src.core.json_response_parser import parse_specific_json_response, get_substring_delimited_by
from src.core.output import append_string_to_file
from src.snowman.constants import snowman_working_directory


def get_credentials():
    return {
        "url": "https://eu-de.ml.cloud.ibm.com",
        "apikey": "WNTEfrjfUygDMK5_8eW-TMGYGUgNgxw2aor4bWsb0Wit"
    }


def set_model(parameters):
    # Defining the model id
    model_id = "sdaia/allam-1-13b-instruct"

    # Defining the project id or space id
    project_id = "5637c821-378b-4fc9-b2b7-c96b62f8be4e"
    client = APIClient(get_credentials())
    client.set.default_project(project_id)

    # Defining the Model object
    model = Model(
        model_id=model_id,
        params=parameters,
        credentials=get_credentials(),
        project_id=project_id,
    )
    return model


# Defining the inferencing input
def load_game_data(model, system_prompt_examples, input_examples,
                   noun_type="""اسم ظاهر معرف بأل التعريف بحالة جمع التكسير""",
                   questions_count="""تمرين واحد""", ):
    try:

        prompt_input = f"""لنلعب لعبة باللغة العربية وهي تأليف جملة اسمية بسيطة. المطلوب إكمال جملة منقوصة المبتدأ.
تذكّر أن المبتدأ هو الاسم المرفوع الذي نبدأ به الكلام،ونخبر عنه باسم آخر ليتم المعنى، يسمى الخبر،ومن المبتدأ والخبر تتألف ما يسمى (الجملة الاسمية).
{system_prompt_examples}
ألّف جملة اسمية بسيطة ذات معنى.
احذف المبتدأ من الجملة الاسمية واجعل الخبر على شكل نكرة.
المبتدأ هو كلمة واحدة.
تنسيق الخرج:
قدم لي الخرج بتنسيق JSON سليم، حيث يكون لكل سؤال كائن يحتوي على الحقول التالية:
question: وهو الجملة الاسمية
correct_answer: وهو المبتدأ
{input_examples}
Input: اعتمد على القاعدة التالية لتوليد {questions_count} تحقق القاعدة النحوية التالية:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل {noun_type}.
Output:"""

        allam_response = model.generate_text(prompt=prompt_input)
        print("allam_response: ", allam_response)
        data, string_result = parse_specific_json_response(allam_response, "<start_json>", "<end_json>")
        append_string_to_file(string_result, snowman_working_directory / 'assets/files/generated_questions.txt')
        return data

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


# Defining the inferencing input
def load_help_questions_data(model, keyword):
    try:

        prompt_input = f"""اكتب ثلاثة أسئلة.
ابدأ السؤال بإحدى الكلمات المفتاحية التالية (ما،من، كيف، لماذا،أين،متى)
تنسيق الخرج:
قدم لي الخرج بالتنسيق التالي:
<start_json>["...","...","..."]<end_json>

اكتب ثلاثة أسئلة يكون جوابها كلمة (المشروعان)
<start_json>["ما هما العملان اللذان يتم تنفيذهما بشكل مشترك بين فريقين أو شخصين؟","ما هي الكلمة المرتبطة بمفهوم التعاون والعمل الجماعي؟","ما هي الكلمة المرتبطة بمفهوم التعاون بين الأفراد أو المؤسسات لتحقيق هدف مشترك؟"]<end_json>


اكتب ثلاثة أسئلة يكون جوابها كلمة (المطالعة)
<start_json>["ما هو النشاط الذي يقوم به الشخص عندما يقرأ الكتب أو المواد المكتوبة؟","ما هي الكلمة المرتبطة بمفهوم القراءة والتعلم من النصوص؟","ما هي الكلمة التي تساعد ممارستها على تحسين مهارات اللغة والثقافة؟"]<end_json>


اكتب ثلاثة أسئلة يكون جوابها كلمة (السرعة). 
<start_json>["ما هو العنصر المهم في الأداء الرياضي والتنافسية؟","ما هي الكلمة المرتبطة بمفهوم كفاءة الإنجاز والنشاط؟","ما هي الكلمة المهمة لتحديد الوقت المستغرق لإنجاز مهمة ما؟"]<end_json>

اكتب ثلاثة أسئلة يكون جوابها كلمة ({keyword}). """
        allam_response = model.generate_text(prompt=prompt_input)
        print("allam_response: ", allam_response)
        data, string_result = parse_specific_json_response(allam_response, "<start_json>", "<end_json>")
        append_string_to_file(string_result, snowman_working_directory / 'assets/files/help_questions.txt')
        return data

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


# Defining the inferencing input
def check_questions_correctness(model, sentence="""الوالدان حنون""", type="""مفرد مؤنث"""):
    try:
        prompt_input = f"""أجب ب "نعم" أو "لا" فقط

Input: هل المبتدأ في جملة (الكتب مفيدة) هو (مثنى مذكر)
Output: <start_json>لا<end_json>


Input: هل المبتدأ في جملة (الطقس جميل) هو (مثنى مؤنث)
Output: <start_json>لا<end_json>

Input: هل المبتدأ في جملة (الطالبان مجدان ونشيطان) هو (مثنى مذكر)
Output: <start_json>نعم<end_json>

Input: هل المبتدأ في جملة (العاملون متفانون في العمل) هو (جمع مذكر)
Output: <start_json>نعم<end_json>

Input: هل المبتدأ في جملة (الصديقات مستمتعات في الرحلة) هو (جمع مؤنث)
Output: <start_json>نعم<end_json>

Input: هل المبتدأ في جملة (المعلمان ملتزمان بمتابعة الطلاب) هو (جمع مؤنث)
Output: <start_json>لا<end_json>

Input: هل المبتدأ في جملة ({sentence}) هو ({type})
Output:"""

        allam_response = model.generate_text(prompt=prompt_input)
        print("allam_response: ", allam_response)
        is_correct = get_substring_delimited_by(allam_response, "<start_json>", "<end_json>")
        is_correct = is_correct.strip()
        append_string_to_file(is_correct, snowman_working_directory / 'assets/files/check_questions_correctness.txt')
        return is_correct

    except Exception as e:
        print(f"Error: {str(e)}")
        return None
