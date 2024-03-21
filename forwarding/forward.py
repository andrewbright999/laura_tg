import asyncio, logging
from datetime import datetime
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

forward_thread = 165 #Royal Safari News

router = Router()
router.message.filter(lambda message: message.message_thread_id == forward_thread)

from_chanal_id = "1001731383596" #Royal Safari

@router.message(Command('start_forwarding'))
async def start_msg(message: Message):
    await message.bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
    print("Run")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await asyncio.sleep(1)
        if current_time in ['14:15:00','16:30:00','18:05:00']:
            albm = []
            while True:
                    post_id = get_post_id()
                    try:  
                        msg = await message.bot.forward_message(chat_id=1263494893, from_chat_id=from_chanal_id, message_id=post_id)
                        if (msg.caption != None) & (albm != []):
                            await message.copy_messages(chat_id=message.chat.id, message_thread_id=message.message_thread_id, from_chat_id=from_chanal_id, message_ids=albm)
                            albm = []
                            write_post_id(post_id)
                            break
                        else: 
                            albm.append(post_id)      
                            write_post_id(post_id+1)        
                    except:
                        write_post_id(post_id+1)


def get_post_id():
    id_file = open("IDFile.txt", "r")
    post_id = int(id_file.readline())
    id_file.close()
    return post_id

def write_post_id(id):
    id_file = open("IDFile.txt", "w")
    id_file.write(f"{id}")
    id_file.close()

