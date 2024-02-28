import random

def handle_response(message) -> str:
    p_message = message.lower()


    if 'honduras' in message:
        return 'whart'
    
    if 'youtube' in message:
        return 'I love youtube'
    
    if p_message == 'roll':
        return str(random.randint(1, 6))
    
    if p_message == '!help':
        return "yagadoo"
    