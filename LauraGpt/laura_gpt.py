from openai import AsyncOpenAI
import time
from LauraGpt.instruction import club_instruct
from config import OPENAI_API_KEY



client = AsyncOpenAI(api_key=OPENAI_API_KEY)
messages=[{"role": "system","content": club_instruct}]

async def answer_to_question(message_text):
    messages.extend([{"role": "user","content": message_text}])
    chat_completion = await client.chat.completions.create(model="gpt-4-turbo-preview",
                                                        messages=messages,
                                                                   temperature =  0.5)
    try:
        response = chat_completion.choices[0].message.content
        messages.extend([{"role":"assistant","content": response}])   
        if len(messages) > 8:
            messages.pop(1)
        return response
    except:
        time.sleep(10)
        await answer_to_question(message_text)

async def get_text(audio): 
    audio_file= open(audio, "rb")
    transcription = await client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcription.text
