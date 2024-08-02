from langchain_core.prompts import PromptTemplate
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import PyPDF2
from langchain_google_genai import ChatGoogleGenerativeAI
import re

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
# Define the prompt template
prompt_template = """
You are a resume parsing expert. Your task is to extract key information from the given resume and structure it into a JSON format.

Resume Content:
{resume_content}

Please parse the above resume and create a JSON object with the following structure:
{{
    "personal_info": {{
        "name": "",
        "phone": "",
        "email": "",
        "linkedin": "",
        "location": ""
    }},
    "education": [
        {{
            "degree": "",
            "institution": "",
            "grade": "",
            "date": ""
        }}
    ],
    "experience": [
        {{
            "title": "",
            "organization": "",
            "description": []
        }}
    ],
    "technical_skills": {{
        "programming": [],
        "soft_skills": []
    }},
    "projects": [
        {{
            "name": "",
            "technologies": "",
            "description": []
        }}
    ],
    "achievements": [],
    "extra_curricular": [
        {{
            "activity": "",
            "description": ""
        }}
    ],
    "publications": []
}}

Ensure that all relevant information from the resume is captured in the appropriate fields. If a field is not applicable or information is not available, leave it as an empty string or empty list as appropriate and give the output in exact JSON format.
  
Output the parsed JSON object:
"""

# Create the prompt
prompt = PromptTemplate(
    input_variables=["resume_content"],
    template=prompt_template
)

google_api_key = "AIzaSyBpNv41i7COJypYYSDOXa7xm71Vgc-z8RQ"  # Replace with your actual key
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

chain = prompt | llm | StrOutputParser()

resume_content = read_pdf("Abhishek_Resume.pdf")

result = chain.invoke(resume_content)
print(result)

cleaned_result = re.sub(r'^[\s\S]*?```json?\s*', '', result)
cleaned_result = re.sub(r'\s*```\s*$', '', cleaned_result)
cleaned_result = cleaned_result.strip()

parsed_resume = json.loads(cleaned_result)
final_json=json.dumps(parsed_resume, indent=4)

file_name ='output.json'

with open(file_name, 'w') as file:
    file.write(final_json)