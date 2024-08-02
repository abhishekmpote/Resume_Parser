from langchain_core.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain_openai import OpenAI
import json
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
import PyPDF2


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

Ensure that all relevant information from the resume is captured in the appropriate fields. If a field is not applicable or information is not available, leave it as an empty string or empty list as appropriate.
give an exact json format
Output the parsed JSON object:
"""

# Create the prompt
prompt = PromptTemplate(
    input_variables=["resume_content"],
    template=prompt_template
)

llm = OpenAI(temperature=0, openai_api_key="your_api_key_here")

chain = prompt | llm | StrOutputParser()

resume_content = read_pdf("Abhishek_Resume.pdf")

# Run the chain
result = chain.invoke(resume_content)
print(result)
print(type(result))


start_index = result.find('{')
end_index = result.find('}')
cleaned_result = result[start_index:end_index+1]

parsed_resume = json.loads(cleaned_result)
final_json=json.dumps(parsed_resume, indent=4)

file_name ='output.json'

with open(file_name, 'w') as file:
    file.write(final_json)
