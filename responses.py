import os
import google.generativeai as genai

# https://codemaker2016.medium.com/build-your-own-chatgpt-using-google-gemini-api-1b079f6a8415
# https://ai.google.dev/
# https://github.com/DeSinc/SallyBot

genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def handle_response(message) -> str:
    p_message = message.lower()
    interruption = ""

    if 'honduras' in message:
        interruption += "whart\n"
    
    if 'youtube' in message:
        interruption += 'I love youtube\n'

    return interruption + model.generate_content(p_message).text