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
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
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
    },
]


# collection of one-liner responses that honduras makes when specific words/phrases are said
def honduras_interruptions(message):
    interruption = ""
    if 'honduras' in message:
        interruption += "whart\n"
    
    if 'youtube' in message:
        interruption += 'I love youtube\n'
    
    return interruption

def convert_discord_obj_to_url(obj):
    if not obj:
        return obj
    return str(obj[0].url)

# convert discord attachment url to images using PIL
def convert_url_to_image(image_url):
    if not image_url:
        return image_url
    try:
        return Image.open(requests.get(image_url, stream=True).raw)
    except Exception as e:
        print("Could not open image: ", e)
    
    return None


def text_response_with_image(image, caption) -> str:
    vision_model = genai.GenerativeModel('gemini-pro-vision')

    if not caption:
        caption = "Describe what is in this image."

    return vision_model.generate_content([caption, image], safety_settings = SAFETY_SETTINGS).text


def convert_to_cowboy_lingo(orig_msg) -> str:
    cowboy_msg = ""
    prompt = "Can you convert this message to cowboy lingo. Make sure to use slang: "
    
    generation_config = genai.types.GenerationConfig(
        candidate_count = 1,
        stop_sequences = [],
        max_output_tokens = 300,
        top_p = 0.9,
        top_k = 5,
        temperature = 1.0
    )

    try:
        cowboy_msg = MODEL.generate_content(prompt + orig_msg,
                                        safety_settings = SAFETY_SETTINGS,
                                        generation_config = generation_config).text      
    except ValueError as e:
        print("Could not generate, trying other way: ", e)
        try:
            cowboy_msg = MODEL.generate_content(prompt + orig_msg,
                                            safety_settings = SAFETY_SETTINGS).text
        except ValueError as e:
            print("Could not generate without filters either", e)

            return "I couldn't tell ya bud."
    
    return cowboy_msg


def text_response(message) -> str:
    # https://ai.google.dev/api/rest/v1beta/GenerateContentResponse
    ai_msg = ""
    generation_config = genai.types.GenerationConfig(
        candidate_count = 1,
        stop_sequences = [],
        max_output_tokens = 175, # a token is approximately 4 characters, this also causes issues
        top_p = 0.6,
        top_k = 5,
        temperature = 0.6
    )

    # there are times where using generation_config I do not get a response, will do more testing
    # mostly due to the max_output_tokens part of the config, but some inputs will also cause 0 output
    # print "I couldn't tell ya bud" when it doesn't know what to say
    try:
        ai_msg = MODEL.generate_content(message,
                                        safety_settings = SAFETY_SETTINGS,
                                        generation_config = generation_config).text      
    except ValueError as e:
        print("Could not generate, trying other way: ", e)
        try:
            ai_msg = MODEL.generate_content(message,
                                            safety_settings = SAFETY_SETTINGS).text
        except ValueError as e:
            print("Could not generate without filters either", e)

            return "I couldn't tell ya bud."
    
    # print(ai_msg.prompt_feedback)

    return convert_to_cowboy_lingo(ai_msg)


def handle_response(message, img_obj) -> str:
    image_url = convert_discord_obj_to_url(img_obj)
    image = convert_url_to_image(image_url)

    p_message = message.lower()
    interruption = honduras_interruptions(p_message)

    ai_msg = ""
    if image:
        ai_msg = text_response_with_image(image, p_message)
    else:
        ai_msg = text_response(p_message)

    # if message is too long for discord 2000 character allowance, return default response
    if len(interruption + ai_msg) > 2000:
        return "I couldn't tell ya bud."
    
    return interruption + ai_msg