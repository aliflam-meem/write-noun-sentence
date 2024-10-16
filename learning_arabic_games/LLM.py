import json
from ibm_watsonx_ai.foundation_models import Model


# watsonx API connection¶
# This cell defines the credentials required to work with watsonx API for Foundation Model inferencing.
# Action: Provide the IBM Cloud personal API key. For details, see documentation.
def get_credentials():
    return {
        "url": "https://eu-de.ml.cloud.ibm.com",
        "apikey": input("API key: ")
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
    project_id = input("PROJECT_ID: ")
    # Defining the Model object
    model = Model(
        model_id=model_id,
        params=parameters,
        credentials=get_credentials(),
        project_id=project_id,
    )
    return model


# Defining the inferencing input
def load_game_data(noun_type = """ضمير مفرد""", questions_count = """سؤالين"""):
    try:
        model = set_model()

        prompt_input = f"""لنلعب لعبة باللغة العربية وهي تأليف جملة اسمية بسيطة. المطلوب إكمال جملة تبدأ بأحد أشكال المبتدأ.

        أشكال المبتدأ في الجملة الاسمية:
        أمثلة عن أشكال المبتدأ
        - الاسم الصريح المعرف بـأل التعريف،حالة المفرد،مثال:
        1- الصبر مفتاح الفرج.
        2- الوطن أعز ما نملك.
        3- الحقيقة واضحة.

        - الاسم الصريح المعرف بـأل التعريف،حالة المثنى،مثال:
        1- الطالبتان متفوقتان.
        2- المهندسان مسافران لحضور المؤتمر
        3- العالمان مبتكران

        - الاسم الصريح المعرف بـأل التعريف،حالة جمع المؤنث السالم،مثال:
        - السيارات سريعة.
        - الفنانات موهوبات

        - الاسم الصريح المعرف بـأل التعريف،حالة جمع المذكر السالم،مثال:
        1- اللاعبون محترفون.
        2- المسافرون متعبون.
        3- المؤمنون متوحدون فيما بينهم.
        4- الفلاحون بارعون في الزراعة.

        - الاسم الصريح المعرف بـأل التعريف،حالة جمع التكسير،مثال:
        1- المدن صاخبة.
        2- الوجوه مبتسمة.
        3- الثمار لذيذة.
        4- الجبال شاهقة.

        -الاسم الصريح كاسم علم:
        1- زيد ذكي.
        2- فاطمة جميلة.
        3- عمر كريم.
        4- ليلى شاعرة.
        5- خالد رياضي.
        6- هند طبيبة.

        - حالة الضمير المفرد:
        1- أنت مهندس ماهر.
        2- هو ابن بار.
        3- هي ابنة مطيعة.
        4- أنا قارئ نهم.

        - حالة الضمير المثنى:
        1- أنتما صديقان حميمان.
        2- هما أخوان متعاونان.
        3- أنتما مهندستان مبتكرتان.
        4- هما طالبتان مجدتان.

        - الضمير الجمع:
        1- نحن طلاب مجتهدون.
        2- أنتم مهندسون أذكياء.
        3- هم أطباء متخصصون.
        4- هن بنات بارات.
        5- نحن قراء متشوقون.
        6- أنتن فتيات حسناوات.

        - اسم الإشارة:
        1- هذا كتاب جميل.
        2- هذه قصة مشوقة.
        3- هؤلاء طلاب مجتهدون.
        4- أولئك رجال شجعان.
        5- تلك سماء صافية.
        6- هذا جبل.
        7- هذه حديقة.


        توصيف اللعبة:
        سنساعد المتعلم على فهم جميع أشكال المبتدأ.
        ألّف جملة فيها فراغ واحد في البداية. هذا الفراغ هو المبتدأ.
        ألّف الجملة بحيث يكون للفراغ أكثر من إجابة صحيحة محتملة.
        اختر إجابة صحيحة منطقية ومتعلقة بموضوع الجملة.
        لا تكرر أي خرج


        تنسيق الخرج:
        قدم لي الخرج بتنسيق JSON، حيث يكون لكل سؤال كائن يحتوي على الحقول التالية:
        question: وهو الجملة ذات الفراغ.
        correct_answer: وهي الكلمة الصحيحة التي تكمل الجملة.
        help_questions: وهي قائمة من ثلاثة أسئلة هدفها مساعدة المتعلم على تخمين الإجابة الصحيحة.اجعل واحد من الأسئلة المساعدة سؤال يخبرنا بعدد أحرف الإجابة الصحيحة ثم يصف وظيفة أو شكل أو مواصفات الإجابة الصحيحة إن أمكن ذلك.
        grammar: وهو شرح بسيط للقاعدة النحوية.

        Input: اكتب جملة فيها فراغ واحد بحيث تحذف المبتدأ ،يطلب من اللاعب إكمالها بكلمة مناسبة تأتي في بداية الجملة. اعتمد على القاعدة التالية لتوليد الخرج:
        المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف. ولِّد سؤالين.
        Output: <start_json>
        [
          {{
        	"question": "... مغلق.",
        	"correct_answer": "الباب",
        	"help_questions": ["ما هو الشيء الذي عادة ما يكون له قفل ويمكن فتحه وإغلاقه؟", "تما هو الشيء الذي ندخله منه إلى الغرفة ونخرجه منه؟", "هو جسم خشبي صلب، له مقبض وعادةً ما يكون لونه بني، فما هو"],
        	"grammar": "المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف."
          }},

          {{
        	"question": "... من أهم مصادر الطاقة المتجددة.",
        	"correct_answer": "الطاقة الشمسية",
        	"help_questions": [
        "ما هو المصدر الذي يستخدم أشعة الشمس لتوليد الكهرباء؟",
        "ما هو المصدر الذي يعتبر صديق للبيئة ومستدام؟",
        "ما هو المصدر الذي يستخدم الألواح الشمسية لاستغلال الطاقة؟",
        ],
        	"grammar": "المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف."
          }},
        ]
        <end_json>


        Input: اكتب جملة فيها فراغ واحد بحيث تحذف المبتدأ ،يطلب من اللاعب إكمالها بكلمة مناسبة تأتي في بداية الجملة. اعتمد على القاعدة التالية لتوليد الخرج:
        المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل ضمير مفرد.
        Output: <start_json>
        [
          {{
        	"السؤال": "... معلمة متفانية.",
        	"correct_answer": "هي",
        	"help_questions": ["إذا قلنا أن فاطمة معلمة متفانية، ما هو الضمير الذي يمكن أن يحل محل اسم فاطمة؟", 
        "تخيل أنك تتحدث عن صديقتك، كيف تصفها؟ استخدم الضمير المناسب", 
        "ما هو الضمير الذي يشير إلى الاسم المفرد المؤنث؟"],
        	"grammar": "المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل ضمير."
          }},
        ]
        <end_json>

        Input: اكتب جملة فيها فراغ واحد بحيث تحذف المبتدأ ،يطلب من اللاعب إكمالها بكلمة مناسبة تأتي في بداية الجملة. اعتمد على القاعدة التالية لتوليد الخرج:
        المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم إشارة.
        Output: <start_json>
        [
          {{
        	"question": "... علم بلادي.",
        	"correct_answer": "هذا",
        	"help_questions": [
        ما هي الكلمة التي نستخدمها للإشارة إلى شيء قريب منا ونريده؟",
              "عندما نريد التعبير عن فخرنا بشيء يمثل بلدنا، ما هي الكلمة التي نستخدمها للإشارة إليه؟",
              "كلمة مؤلفة من ثلاثة أحرف، وهي الاسم المذكر من اسم الإشارة (هي)؟",
        ],
        	"grammar": "المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم إشارة."
          }},
        ]
        <end_json>

        Input: اكتب جملة فيها فراغ واحد بحيث تحذف المبتدأ ،يطلب من اللاعب إكمالها بكلمة مناسبة تأتي في بداية الجملة. اعتمد على القاعدة التالية لتوليد الخرج:
        المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف. ولِّد سؤالين.
        Output:  <start_json>
        [
          {{
        	"question": "... مدينة جميلة.",
        	"correct_answer": "القاهرة",
        	"help_questions": [
        "ما هي عاصمة مصر؟",
        "أي دولة تعتبر ملتقى الحضارات القديمة والحديثة؟",
        "ما هي المدينة المعروفة بتاريخها العريق وأسواقها النابضة بالحياة؟",
        ],
        	"grammar": "المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف."
          }},
          {{
        	"question": "... أسرع حيوان.",
        	"correct_answer": "الظبي ",
        	"help_questions": ["ما هو الحيوان الذي يتميز بسرعة تفوق معظم الحيوانات الأخرى؟",
        "اسم حيوان يبدأ بحرف الظاء ويعتبر أسرع الكائنات الحية؟",
        "حيوان يتميز بالرشاقة والسرعة العالية، وقد ورد ذكره في القرآن الكريم",
        ],
        	"grammar": "المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف."
          }},
        ]
        <end_json>

        Input: اكتب جملة فيها فراغ واحد بحيث تحذف المبتدأ ،يطلب من اللاعب إكمالها بكلمة مناسبة تأتي في بداية الجملة. اعتمد على القاعدة التالية لتوليد الخرج:
        المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل {noun_type}. ولِّد {questions_count}.
        Output:"""

        allam_response = model.generate_text(prompt=prompt_input,
                                             guardrails=False)
        json_data = allam_response.replace("<start_json>",
                                           "").replace("<end_json>", "")
        quiz_data = json.loads(json_data)
        print(quiz_data)
        return quiz_data

    except Exception as e:
        print(f"Error: {str(e)}")
        return
