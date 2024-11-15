import requests


url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

body = {
	"input": """لنلعب لعبة باللغة العربية وهي تأليف جملة اسمية بسيطة. المطلوب إكمال جملة منقوصة المبتدأ.
تذكّر أن المبتدأ هو الاسم المرفوع الذي نبدأ به الكلام،ونخبر عنه باسم آخر ليتم المعنى، يسمى الخبر،ومن المبتدأ والخبر تتألف ما يسمى (الجملة الاسمية).
أمثلة عن شكل المبتدأ في الجملة الاسمية كاسم ظاهر:
-الاسم الظاهر المعرّف بـأل التعريف،حالة المفرد
-الصبر مفتاح الفرج.
-الوطن أعز ما نملك.
-الحقيقة واضحة.
-أخوك ذو همة.
- الاسم الظاهر المعرّف بـأل التعريف،حالة المثنى المذكر
-العالمان مبتكران.
-المهندسان مسافران لحضور المؤتمر.
الاسم الظاهر المعرّف بأل التعريف،حالة المثنى المؤنث
-الطالبتان متفوقتان في الرياضيات.
-الشجرتان مثمرتان.
-النافذتان تلمعان.
-الاسم الظاهر المعرّف بـأل التعريف،حالة جمع المؤنث السالم
-السيارات سريعة.
-الفنانات موهوبات.
-الاسم الصريح المعرف بـأل التعريف،حالة جمع المذكر السالم،مثال:
-اللاعبون محترفون.
-المسافرون متعبون من السفر.
-المؤمنون متوحدون فيما بينهم.
-الفلاحون بارعون في الزراعة.
-الاسم الصريح المعرف بـأل التعريف،حالة جمع التكسير،مثال:
-المدن صاخبة.
-الوجوه مبتسمة.
-الثمار لذيذة.
-الجبال شاهقة.
توصيف اللعبة:
اكتب جملة فيها فراغ واحد في بداية الجملة الاسمية بحيث تحذف المبتدأ ،ليتمكن المتعلم  من إكمالها.
 ألّف الجملة بحيث يكون للفراغ أكثر من إجابة صحيحة محتملة.
احذف المبتدأ من الجملة الاسمية واجعل الخبر على شكل نكرة.
حافظ على مطابقة المبتدأ للخبر.
تذكّر أنه إذا كان المبتدأ والخبر مثنيين فعلامة رفعهما الألف والنون، وأما إذا كان المبتدأ والخبر جمع مذكر سالم فعلامة رفعهما الواو والنون.
تذكّر أنه إذا كان المبتدأ والخبر من الأسماء التالية(أخ،أب،حم،ذو،فو) فعلامة رفعهما الواو فقط.
 ألّف الجملة بحيث يكون للفراغ أكثر من إجابة صحيحة محتملة.
 اختر إجابة صحيحة منطقية ومتعلقة بموضوع جملة التمرين.
 لا تكرر أي تمرين على الإطلاق
تنسيق الخرج:
قدم لي الخرج بتنسيق JSON سليم، حيث يكون لكل سؤال كائن يحتوي على الحقول التالية:
question: وهو الجملة ذات الفراغ.
correct_answer: وهي الكلمة الصحيحة التي تملأ الفراغ.
help_questions: وهي قائمة من ثلاثة أسئلة فقط،هدفها مساعدة المتعلم على تخمين الإجابة الصحيحة.اجعل واحد من الأسئلة المساعدة يصف وظيفة أو شكل أو مواصفات الإجابة الصحيحة إن أمكن ذلك.
grammar: وهو شرح بسيط للقاعدة النحوية.

Input: اعتمد على القاعدة التالية لتوليد تمرينين مختلفين:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة المفرد.
Output: <start_json>[{{\"question\":\"... مغلق.\",\"correct_answer\":\"الباب\",\"help_questions\":[\"ما هو الشيء الذي عادةً ما يكون له قفل ويمكن فتحه وإغلاقه\",\"ما هو الشيء الذي ندخل منه إلى الغرفة ونخرج منه\",\"هو جسم خشبي صلب، له مقبض وعادةً ما يكون لونه بني،فما هو؟\"],\"grammar\":\"اسم ظاهر معرف بأل التعريف بحالة المفرد.\"}},{{\"question\":\"... من أهم مصادر الطاقة المتجددة.\",\"correct_answer\":\"الطاقة الشمسية\",\"help_questions\":[ \"ما هو المصدر الذي يستخدم أشعة الشمس لتوليد الكهرباء؟\",\"ما هو المصدر الذي يعتبر صديق للبيئة ومستدام؟\", \"ما هو المصدر الذي يستخدم الألواح الشمسية لاستغلال الطاقة؟\"],\"grammar\":\"اسم ظاهر معرف بأل التعريف بحالة المفرد.\"}}]<end_json>

Input: اعتمد على القاعدة التالية لتوليد تمرين واحد:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة جمع المؤنث السالم.
Output: <start_json>[{{\"question\": \"... مهمة.\",\"correct_answer\":\"الواجبات\",\"help_questions\":[\"ما هي الأشياء التي يجب على الطالب إنجازها؟\", \"ما هي الأشياء التي يجب على الشخص القيام بها؟\", \"ما هي الأشياء التي تعتبر جزءًا من المهام اليومية؟\" ],\"grammar\":\"اسم ظاهر معرف بأل التعريف بحالة المؤنث السالم.\"}}]<end_json>

Input: اعتمد على القاعدة التالية لتوليد تمرين واحد:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة المثنى المؤنث.
Output: <start_json>[{{\"question\":\"... متعاونتان.\",\"correct_answer\":\"الطبيبتان\",\"help_questions\":[\"من هما الشخصان اللذان يعملان في مجال الصحة؟\", \"من هما الشخصان اللذان يساعدان المرضى؟\", \"من هما الشخصان اللذان يرتديان المعطف الأبيض؟\" ],\"grammar\":\"اسم ظاهر معرف بأل التعريف بحالة المثنى المؤنث.\"}}]<end_json>

Input: اعتمد على القاعدة التالية لتوليد تمرين واحد:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة المثنى المذكر.
Output: <start_json>[{{\"question\":\"... متفاهمان.\",\"correct_answer\":\"الزوجان\",\"help_questions\":[\"من هما الشخصان اللذان يعيشان معًا؟\", \"من هما الشخصان اللذان يتعاونان في الحياة؟\", \"من هما الشخصان اللذان يشكلان عائلة؟\" ],\"grammar\":\"اسم ظاهر معرف بأل التعريف بحالة المثنى المذكر.\"}}]<end_json>

Input: اعتمد على القاعدة التالية لتوليد تمرينين مختلفين:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة جمع التكسير.
Output:  <start_json>[{{\"question\":\"... جميلة.\",\"correct_answer\":\"الزهور\",\"help_questions\":[\"ما هي النباتات الملونة والمبهجة للعين؟\", \"ما هي العناصر الطبيعية التي تضفي جمالاً على المكان؟\", \"ما هي المكونات الأساسية لتزيين الحدائق والمنازل؟\" ],\"grammar\":\"المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة الجمع التكسير.\"}},{{\"question\":\"... قوية.\",\"correct_answer\":\"الجسور\",\"help_questions\":[\"ما هي الهياكل الهندسية المصممة لربط الأماكن عبر الأنهار والوديان؟\", \"ما هي المنشآت الضرورية لتسهيل النقل والتواصل بين المناطق؟\", \"ما هي الأمثلة البارزة للهندسة المدنية والعمارة؟\" ],\"grammar\":\"اسم ظاهر معرف بأل التعريف بحالة الجمع التكسير.\"}}]<end_json>

Input: اعتمد على القاعدة التالية لتوليد سؤالين مختلفين:المبتدأ هو اسم مرفوع تبدأ به الجملة الاسمية ويأتي على شكل اسم ظاهر معرف بأل التعريف بحالة المثنى المذكر.
Output:""",
	"parameters": {
		"decoding_method": "sample",
		"max_new_tokens": 600,
		"stop_sequences": ["<end_json>", "}}]<end_json>"],
		"temperature": 0.8,
		"top_k": 52,
		"top_p": 0.8,
		"repetition_penalty": 1.2
	},
	"model_id": "sdaia/allam-1-13b-instruct",
	"project_id": "5637c821-378b-4fc9-b2b7-c96b62f8be4e"
}

headers = {
	"Accept": "application/json",
	"Content-Type": "application/json",
	"Authorization": "p-2+x02rjx5pmgjLXjK39U+SYg==;yEAOYyxYPnw3yKKWPODvZA==:prpeNH6gYZ0DVQ11gJQZD82QGt86id9aFSbUlqJSjneYtPT7q1uneKZ5bRux164W+eN3KvVWKSW7BONFqyMPqyrBJLdhpu4+6g=="
}

response = requests.post(
	url,
	headers=headers,
	json=body
)

# if response.status_code != 200:
# 	raise Exception("Non-200 response: " + str(response.text))

data = response.json()
