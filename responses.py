import os
import google.generativeai as genai
from PIL import Image # pillow, python imaging library
import requests

# https://codemaker2016.medium.com/build-your-own-chatgpt-using-google-gemini-api-1b079f6a8415
# https://ai.google.dev/
# https://github.com/DeSinc/SallyBot
# https://www.analyticsvidhya.com/blog/2023/12/google-gemini-api/
# https://pillow.readthedocs.io/en/stable/

genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
MODEL = genai.GenerativeModel('gemini-pro')


# collection of one-liner responses that honduras makes when specific words/phrases are said
def honduras_interruptions(message):
    interruption = ""
    if 'honduras' in message:
        interruption += "whart\n"
    
    if 'youtube' in message:
        interruption += 'I love youtube\n'
    
    return interruption

# convert discord attachment url to images using PIL
def convert_url_to_image(image_url):
    if not image_url:
        return image_url
    return Image.open(requests.get(image_url, stream=True).raw)
    

def handle_response(message, image_url) -> str:
    image = convert_url_to_image(image_url)
    p_message = message.lower()
    interruption = honduras_interruptions(p_message)

    ai_msg = MODEL.generate_content(p_message,
                                    safety_settings=[
                                                    {
                                                        "category": "HARM_CATEGORY_HARASSMENT",
                                                        "threshold": "BLOCK_NONE",
                                                    },
                                                    {
                                                        "category": "HARM_CATEGORY_HATE_SPEECH",
                                                        "threshold": "BLOCK_NONE",
                                                    },
                                                    {
                                                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                                        "threshold": "BLOCK_NONE",
                                                    },
                                                    {
                                                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                                                        "threshold": "BLOCK_NONE",
                                                    }
                                                ],
                                    generation_config = genai.types.GenerationConfig(
                                    candidate_count = 1,
                                    stop_sequences = [],
                                    max_output_tokens = 50, # a token is approximately 4 characters so 160 char output roughly
                                    top_p = 0.9,
                                    top_k = 5,
                                    temperature = 1.0
                                    ))
    print(ai_msg.prompt_feedback)

    return interruption + ai_msg.text