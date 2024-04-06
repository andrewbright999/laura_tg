import asyncio, logging
from datetime import datetime
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

forward_thread = 252 #Royal Expeditions News

router = Router()
router.message.filter(lambda message: message.message_thread_id == forward_thread)

from_chanal_id = 1263494893 #My personal
                
                
@router.message(Command('fid'))
async def start_msg(message: Message, command: CommandObject):
    await message.bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
    albm = []
    post_id = int(command.args)
    for i in range(15):
        try:  
            msg = await message.bot.forward_message(chat_id=2056795394, from_chat_id=from_chanal_id, message_id=post_id)
            if (msg.caption != None) & (albm != []):
                await message.bot.copy_messages(chat_id=message.chat.id, message_thread_id=message.message_thread_id, from_chat_id=from_chanal_id, message_ids=albm)
                albm = []
                break
            else: 
                albm.append(post_id)      
                post_id=post_id+1        
        except Exception as E:
            print(E)
            post_id=post_id+1                
                

