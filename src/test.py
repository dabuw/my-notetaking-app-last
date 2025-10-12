# import libraries
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Loads environment variables from .env
token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"

# 得到token的网址：https://github.com/settings/personal-access-tokens/new?description=Used+to+call+GitHub+Models+APIs+to+easily+run+LLMs%3A+https%3A%2F%2Fdocs.github.com%2Fgithub-models%2Fquickstart%23step-2-make-an-api-call&name=GitHub+Models+token&user_models=read


# A function to call an LLM model and return the response
def call_llm_model(model, messages, temperature=1.0, top_p=1.0):    
    client = OpenAI(base_url=endpoint, api_key=token)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        top_p=top_p
    )
    return response.choices[0].message.content

# A function to translate to target language
def translate_text(text, target_language, model=model):
    messages = [
        {"role": "system", "content": f"You are a helpful translator that translates text to {target_language}."},
        {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
    ]
    return call_llm_model(model, messages)

# Run the main function if this script is executed
if __name__ == "__main__":
    # Example usage
    text_to_translate = "Hello, how are you today?"
    target_language = "Chinese"
    translated_text = translate_text(text_to_translate, target_language)
    print(f"Original: {text_to_translate}")
    print(f"Translated ({target_language}): {translated_text}")