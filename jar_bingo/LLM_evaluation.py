import vertexai
from vertexai.generative_models import GenerativeModel
prompt="أكل البنت الطعام وشرب اماء"
PROJECT_ID = "original-voyage-437012-j5"
vertexai.init(project=PROJECT_ID, location="us-central1")

model = GenerativeModel("gemini-1.5-flash-002")

response = model.generate_content(
    f"صحح النص التالي: {prompt}",
)

print(response.text)

#!pip install google-cloud-aiplatform