from openai import AsyncOpenAI
from config import OPENAI_API_KEY
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {OPENAI_API_KEY}'
}

async def response(response_text):
    chat_completion = await client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "user","content": response_text}], temperature =  0.5)
    return chat_completion.choices[0].message.content

async def definity_chek(message_text):  
    response_text = f"Есть ли в этом сообщении нецензурная лексика.{message_text}. Ответь одним словом да или нет"
    return await response(response_text)

async def politic_and_religiy_chek(message_text):  
    response_text = f"Есть ли в этом сообщении обсуждение политики или религии.{message_text}. Ответь одним словом да или нет"
    return await response(response_text)

async def check(message_text):
    if (await definity_chek(message_text)) == "Да":
        return "Мат"
    elif (await politic_and_religiy_chek(message_text)) == "Да":
        return "Религия"
    else: 
        return "Нет"