import os
from os import getenv
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Initialize the Azure client using your specific environment keys
client = AzureOpenAI(
    api_version=getenv("api_version"),
    azure_endpoint=getenv("endpoint"),
    api_key=getenv("OPENAI_API_KEY"),
)

def ask_ai(user_query):
    prompt = [
        {
            "role": "system", 
            "content": """You are a helpful medical assistant and will be helping doctors with the patient's symptom analysis. 
You will be provided patient details along with symptoms and the question that doctor is asking. 
You should respond with suggestions."""
        },
        {
            "role": "user", 
            "content": str(user_query).strip()  # Guarantees it is processed as a flat string
        }
    ]
    
    print("Payload sent to Azure:", prompt)
    
    response = client.chat.completions.create(
        model=getenv("model_name"),  # This must match your Azure deployment name
        messages=prompt
    )
    
    # Correct way to access the string content in the current OpenAI SDK
    ai_response = response.choices[0].message.content
    print("AI Response:", ai_response)
    
    return ai_response
