from openai import AsyncOpenAI
import requests
import asyncio

OPENAI_API_KEY = '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'
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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'
}

async def response(response_text):
    data = {
    "model": "gpt-3.5-turbo",
    "messages": [{
        "role": "user",
        "content": response_text
    }],
    "temperature": 0.5
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    response_data = response.json()
    try:
        return response_data['choices'][0]['message']['content']
    except:
        asyncio.sleep(20)
        await response(response_text)
    

async def definity_chek(message_text):  
    response_text = f"Есть ли в этом сообщении нецензурная лексика.{message_text}. Ответь одним словом да или нет"
    return await response(response_text)


async def politic_and_religiy_chek(message_text):  
    response_text = f"Есть ли в этом сообщении обсуждение политики или религии.{message_text}. Ответь одним словом да или нет"
    return await response(response_text)

async def check(message_text):
    if message_text.lower != "да":
        if await politic_and_religiy_chek(message_text) == "Да":
            return "Религия"
        elif await definity_chek(message_text) == "Да"  :
            return "Мат"
        else: 
            return "Нет"
# print("Политика "+politic_and_religiy_chek(message))

# try:
    # print("Мат: "+definity_chek(message))
    # print("Политика "+politic_and_religiy_chek(message))
# except:
#     time.sleep(60)
#     print("Мат: "+definity_chek(message))
#     print("Политика "+politic_and_religiy_chek(message))