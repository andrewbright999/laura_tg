from openai import AsyncOpenAI
import requests
import asyncio

OPENAI_API_KEY = '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'

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def response(messages):
    chat_completion = await client.chat.completions.create(model="gpt-4-turbo-preview",
                                                        messages=messages,
                                                                   temperature =  0.1)
    response = chat_completion.choices[0].message.content
    return response
    

            
async def get_aiata(message_text):  
    messages=[{"role": "system","content": "You work as an assistant at a travel agency. A message will be sent to you about the place where the person wants to fly by plane. Find the nearest major airport or city to this place and send just its IATA code, separating them with commas"},
              {"role": "user","content": message_text}]
    first_iata = await response(messages)
    # print(first_iata)
    # messages=[{"role": "system","content": "Проверь если такого кода iata нет, отправь в ответ настоящие коды через запятую, убери лишние комментарии"},{"role": "user","content": first_iata}]
    # final_iata = await response(messages)
    return first_iata.split(",")
    
async def get_data(message_text):  
    messages=[{"role": "system","content": "You're the travel agency assistant operator's assistant. You need to find out from the message which city the person will fly from, to which city.  Convert the date to ISO8601 format. If the date is not specified, specify: today. if the date is specified tomorrow, then reply tomorrow. Answer in the format: from_where_city, to_where_city,date"},
              {"role": "user","content": message_text}]
    data = await response(messages)
    return data.split(',')
# aiata = asyncio.run(get_aiata("Чили")).replace(" ","").split(",")
# print(aiata)
# print()

    # return await response(response_text)
# print("Политика "+politic_and_religiy_chek(message))

# try:
    # print("Мат: "+definity_chek(message))
    # print("Политика "+politic_and_religiy_chek(message))
# except:
#     time.sleep(60)
#     print("Мат: "+definity_chek(message))
#     print("Политика "+politic_and_religiy_chek(message))