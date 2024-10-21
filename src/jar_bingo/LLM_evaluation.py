
"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""
import os

import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content


genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_schema": content.Schema(
    type=content.Type.OBJECT,
    enum="[]",
    required="["sentence"]",
  properties = {
                 "sentence": content.Schema(
                   type=content.Type.STRING,
                 ),
                 "pos": content.Schema(
                   type=content.Type.ARRAY,
                   items=content.Schema(
                     type=content.Type.STRING,
                   ),
                 ),
               },
),
"response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="قم بالآتي لكل من الجمل التالية:\nقم بتصحيح الجملة لغوياً، ثم ضعها في كائن جيسون على الشكل التالي:\nتصحيح الجملة في sentence، والجملة مقطعة كلمة كلمة في pos.\nالجملة:",
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)


# import vertexai
# from vertexai.generative_models import GenerativeModel
# prompt="أكل البنت الطعام وشرب اماء"
# vertexai.init(project=PROJECT_ID, location="us-central1")

# model = GenerativeModel("gemini-1.5-flash-002")

# response = model.generate_content(
#     f"صحح النص التالي: {prompt}",
# )

# print(response.text)


