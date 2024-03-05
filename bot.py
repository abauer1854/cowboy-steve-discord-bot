import discord
import responses

async def send_message(message, user_message, image, is_private):
    try:
        response = responses.handle_response(user_message, image)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_bot():
    TOKEN = responses.os.environ.get('BOT_TOKEN')
    # these intents are now needed so that honduras can read any message, not just ! messages
    intents = discord.Intents.default()
    intents.typing = True
    intents.messages = True
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
    
    @client.event

    async def on_message(message):
        if message.author == client.user:
            return
        
        image = None
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # handling images
        if message.attachments:
            image = message.attachments # if there are multiple attachments, image becomes a list of attachment objects

        print(f"{username} said: '{user_message}' ({channel})")

        # if user_message:
        #     if user_message[0] == '?':
        #         user_message = user_message[1:]
        #         await send_message(message, user_message, is_private=True)
        #     else:
        #         await send_message(message, user_message, is_private=False)

        await send_message(message, user_message, image, is_private=False)



    client.run(TOKEN)