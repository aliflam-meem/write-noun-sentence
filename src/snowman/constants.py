import pathlib


snowman_working_directory = pathlib.Path(__file__).parent

# Images
SNOWMAN_GAME_RESULT = snowman_working_directory / 'assets/images/snowman_game_result.png'
SNOWMAN_GAME_SCREEN_BG = snowman_working_directory / 'assets/images/cartoon_style_snowy_landscape.jpg'
SNOWMAN_GAME_SCREEN_BG_TRA = snowman_working_directory / 'assets/images/cartoon_style_snowy_landscape_transparent.png'
snowman_thumbnail = snowman_working_directory / 'assets/images/snowman_thumbnail.jpg'
CHECK_MARK_IMAGE_PATH = snowman_working_directory / 'assets/images/check_mark.png'

# Sounds
snow_melting_sound = snowman_working_directory / 'assets/audio/snow_melting.mp3'

snowman_levels_keys = ["al_atareef", "demonstratives", "pronouns"]
snowman_levels = {
    snowman_levels_keys[0]: {
        "name": "al_atareef",
        "title": "المعرف بأل التعريف",
        "noun_types": ["اسم ظاهر معرف بـأل التعريف،بحالة المفرد",
                       "اسم ظاهر معرف بـأل التعريف،بحالة المثنى المذكر",
                       "اسم ظاهر معرف بـأل التعريف،بحالة المثنى المؤنث",
                       "اسم ظاهر معرف بـأل التعريف،بحالة جمع المؤنث السالم",
                       "اسم ظاهر معرف بـأل التعريف،بحالة جمع المذكر السالم"
                       "اسم ظاهر معرف بـأل التعريف،بحالة جمع التكسير"]
    },
    snowman_levels_keys[1]: {
        "name": "demonstratives",
        "title": "اسم الإشارة",
        "noun_types": ["اسم إشارة"]
    },
    snowman_levels_keys[2]: {
        "name": "pronouns",
        "title": "الضمير",
        "noun_types": ["ضمير مفرد", "ضمير مثنى", "ضمير جمع"]
    }
}

SINGULARITY_FORMATS = {
    "اسم ظاهر معرف بـأل التعريف،بحالة المفرد": "مفرد",
    "اسم ظاهر معرف بـأل التعريف،بحالة المثنى المذكر": "مثنى مذكر",
    "اسم ظاهر معرف بـأل التعريف،بحالة المثنى المؤنث": "مثنى مؤنث",
    "اسم ظاهر معرف بـأل التعريف،بحالة جمع المؤنث السالم": "جمع مؤنث سالم",
    "اسم ظاهر معرف بـأل التعريف،بحالة جمع المذكر السالم": "جمع مذكر سالم",
    "اسم ظاهر معرف بـأل التعريف،بحالة جمع التكسير": "جمع تكسير",
    "اسم إشارة": """-هذا كتاب جميل.
-هذه قصة مشوقة.
-هؤلاء طلاب مجتهدون.
-أولئك رجال شجعان.
-تلك سماء صافية.
-هذا جبل.
-هذه حديقة.""",
    "ضمير مفرد": """-أنت مهندس ماهر.
-هو ابن بار.
-هي ابنة مطيعة.
-أنا قارئ نهم.""",
    "ضمير مثنى": """-أنتما صديقان حميمان.
-هما أخوان متعاونان.
-أنتما مهندستان مبتكرتان.
-هما طالبتان مجدتان.""",
    "ضمير جمع": """-نحن طالبات مجتهدات.
-أنتم مهندسون أذكياء.
-هم أطباء متخصصون.
-هن بنات بارات.
-نحن قراء متشوقون.
-أنتن فتيات حسناوات."""
}

INPUT_EXAMPLES = {"اسم ظاهر معرف بـأل التعريف،بحالة المفرد": "",
                  "اسم ظاهر معرف بـأل التعريف،بحالة المثنى المذكر": """Input: اكتب ثلاث جمل تحقق القاعدة النحوية التالية:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة المثنى المذكر.
Output: <start_json>[{{"question":"الكتابان مفيدان لاكتساب مفردات في علم النفس","correct_answer":"الكتابان"}},{{"question":"الولدان ذكيّان ومبدعان في استخدام التكنولوجيا الحديثة","correct_answer":"الولدان"}},{{"question":"الشابان الطموحان يتنافسان بجدّ للفوز بالجائزة الكبرى للطلاب المتفوقين في الجامعات العالمية المرموقة","correct_answer":"الشابان"}}]<end_json>

Input: اكتب جملة تحقق القاعدة النحوية التالية:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة المثنى المذكر.
Output: <start_json>[{{"question":"الطالبان الناجحان يتميزان بقوة الذاكرة والتركيز السريع في حل المشكلات","correct_answer":"الطالبان"}}]<end_json> """,
                  "اسم ظاهر معرف بـأل التعريف،بحالة المثنى المؤنث": """Input: اكتب ثلاث جمل تحقق القاعدة النحوية التالية:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة المثنى المؤنث.
Output: <start_json>[{{"question":"الطبيبتان متعاونتان في إنجاز عملهما","correct_answer":"الطبيبتان"}},{{"question":"الطفلتان ذكيّتان ومبدعتان في استخدام التكنولوجيا الحديثة","correct_answer":"الطفلتان"}},{{"question":"الشابتان الطموحتان تتنافسان بجدّ للفوز بالجائزة الكبرى للطالبات المتفوقات في الجامعات العالمية المرموقة","correct_answer":"الشابتان"}}]<end_json>

Input: اكتب جملة تحقق القاعدة النحوية التالية:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة المثنى المؤنث.
Output: <start_json>[{{"question":"الطالبتان الناجحتان تتميزان بقوة الذاكرة والتركيز السريع في حل المشكلات","correct_answer":"الطالبتان"}}]<end_json> """,
                  "اسم ظاهر معرف بـأل التعريف،بحالة جمع المؤنث السالم": """Input: اكتب ثلاث جمل تحقق القاعدة النحوية التالية:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة جمع المؤنث السالم.
Output: <start_json>[{{"question":"المجلات مفيدة لاكتساب مفردات في علم النفس","correct_answer":"المجلات"},{"question":"الأخوات متعاضدات في ترتيب المنزل","correct_answer":"الأخوات"},{{"question":"الطاولات مليئة بأصناف الطعام المتنوع","correct_answer":"الطاولات"}}]<end_json>

Input: اكتب جملة تحقق القاعدة النحوية التالية:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة جمع المؤنث السالم.
Output: <start_json>[{{"question":"الخضروات مغذية ومفيدة لبناء جسم الإنسان","correct_answer":"الخضروات"}}]<end_json> """,
                  "اسم ظاهر معرف بـأل التعريف،بحالة جمع المذكر السالم": """""",
                  "اسم ظاهر معرف بـأل التعريف،بحالة جمع التكسير": """""",
                  "اسم إشارة": """""",
                  "ضمير مفرد": """""",
                  "ضمير مثنى": """""",
                  "ضمير جمع": """"""}

SYSTEM_PROMPT_EXAMPLES = {
    "اسم ظاهر معرف بـأل التعريف،بحالة المفرد": """
أمثلة عن شكل المبتدأ في الجملة الاسمية كاسم ظاهر:
-الاسم الظاهر المعرّف بـأل التعريف،حالة المفرد
-الصبر مفتاح الفرج.
-الوطن أعز ما نملك.
-الحقيقة واضحة.
-أخوك ذو همة.
الاسم الظاهر المعرّف بأل التعريف،حالة المثنى المؤنث
-الطالبتان متفوقتان في الرياضيات.
-الشجرتان مثمرتان.
-النافذتان تلمعان.
- الاسم الظاهر المعرّف بـأل التعريف،حالة المثنى المذكر
-العالمان مبتكران.
-المهندسان مسافران لحضور المؤتمر.""",
    "اسم ظاهر معرف بـأل التعريف،بحالة المثنى المذكر": """
أمثلة عن شكل المبتدأ في الجملة الاسمية كاسم ظاهر:
-الاسم الظاهر المعرّف بـأل التعريف،حالة المفرد
-الصبر مفتاح الفرج.
-الوطن أعز ما نملك.
-الحقيقة واضحة.
-أخوك ذو همة.
الاسم الظاهر المعرّف بأل التعريف،حالة المثنى المؤنث
-الطالبتان متفوقتان في الرياضيات.
-الشجرتان مثمرتان.
-النافذتان تلمعان.
- الاسم الظاهر المعرّف بـأل التعريف،حالة المثنى المذكر
-العالمان مبتكران.
-المهندسان مسافران لحضور المؤتمر.""",
    "اسم ظاهر معرف بـأل التعريف،بحالة المثنى المؤنث": """
أمثلة عن شكل المبتدأ في الجملة الاسمية كاسم ظاهر:
-الاسم الظاهر المعرّف بـأل التعريف،حالة المفرد
-الصبر مفتاح الفرج.
-الوطن أعز ما نملك.
-الحقيقة واضحة.
-أخوك ذو همة.
الاسم الظاهر المعرّف بأل التعريف،حالة المثنى المؤنث
-الطالبتان متفوقتان في الرياضيات.
-الشجرتان مثمرتان.
-النافذتان تلمعان.
- الاسم الظاهر المعرّف بـأل التعريف،حالة المثنى المذكر
-العالمان مبتكران.
-المهندسان مسافران لحضور المؤتمر.""",
    "اسم ظاهر معرف بـأل التعريف،بحالة جمع المؤنث السالم": """""",
    "اسم ظاهر معرف بـأل التعريف،بحالة جمع المذكر السالم": """""",
    "اسم ظاهر معرف بـأل التعريف،بحالة جمع التكسير": """""",
    "اسم إشارة": """""",
    "ضمير مفرد": """""",
    "ضمير مثنى": """""",
    "ضمير جمع": """"""}

PARAMETERS_SHORT_SENTENCES = {
    "decoding_method": "sample",
    "max_new_tokens": 600,
    "stop_sequences": ["<end_json>", "}}]<end_json>"],
    "temperature": 0.8,
    "top_k": 52,
    "top_p": 0.8,
    "repetition_penalty": 1.2,
    "timeout": 60,
}

PARAMETERS_LONG_SENTENCES = {
    "decoding_method": "sample",
    "max_new_tokens": 600,
    "stop_sequences": ["<end_json>", "}}]<end_json>"],
    "temperature": 0.7,
    "top_k": 51,
    "top_p": 1,
    "repetition_penalty": 1.2,
    "timeout": 60,
}

HELP_QUESTIONS_PARAMETERS = {
    "decoding_method": "sample",
    "max_new_tokens": 500,
    "min_new_tokens": 0,
    "stop_sequences": [
        "<end_json>"
    ],
    "temperature": 0.8,
    "top_k": 50,
    "top_p": 1,
    "repetition_penalty": 1.1,
    "timeout": 60,
}

CORRECTNESS_PARAMETERS = {
    "decoding_method": "greedy",
    "max_new_tokens": 200,
    "stop_sequences": ["<end_json>"],
    "repetition_penalty": 1,
    "timeout": 60,
}
