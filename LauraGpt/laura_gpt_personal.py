from openai import AsyncOpenAI
import time, json, os
from LauraGpt.instruction import club_instruct
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def answer_to_question(message_text, chat_id):
    messages = get_messages_id(chat_id)
    messages.extend([{"role": "user","content": message_text}])
    chat_completion = await client.chat.completions.create(model="gpt-4-turbo-preview",
                                                                messages=messages,
                                                                   temperature =  0.5)
    try:
        response = chat_completion.choices[0].message.content
        messages.extend([{"role":"assistant","content": response}])   
        if len(messages) > 8:
            messages.pop(2)
        write_messages_id(messages, chat_id)
        return response.replace("**", "*")
    except Exception as e:
        print(e)
        time.sleep(10)
        await answer_to_question(message_text, chat_id)

async def get_text(audio):
    audio_file= open(audio, "rb")
    transcription = await client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcription.text

def get_messages_id(chat_id):
    if not os.path.isfile(f'{chat_id}.json'):
        print("Not found")
        messages=[{"role": "system","content": club_instruct}]
        f = open(f'{chat_id}.json', 'a+', encoding="utf-8")  # open file in append mode
        f.write(json.dumps(messages, ensure_ascii=False, indent=4))
    with open(f'{chat_id}.json', encoding="utf-8") as f:
        messages = json.load(f)
        # print(messages)
    return messages

def write_messages_id(messages, chat_id):
    with open(f'{chat_id}.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(messages, ensure_ascii=False, indent=4))