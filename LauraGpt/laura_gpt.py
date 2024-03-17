from openai import AsyncOpenAI
import time, json, asyncio

from LauraGpt.instruction import system_instruct
# from LauraGpt.instruction import system_instruct

# from aiogram.methods import SendChatAction

OPENAI_API_KEY = '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'

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
messages=[{"role": "system","content": system_instruct}]

async def answer_to_question(message_text):
    messages.extend([{"role": "user","content": message_text}])
    chat_completion = await client.chat.completions.create(model="gpt-3.5-turbo",
                                                        messages=messages,
                                                                   temperature =  0.5)
    try:
        response = chat_completion.choices[0].message.content
        messages.extend([{"role":"assistant","content": response}])   
        if len(messages) > 8:
            messages.pop(1)
        return response
    except:
        asyncio.sleep(20)
        await answer_to_question(message_text)