from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from plugins.info import GENIUS_API
import requests 
from lyricsgenius import Genius 
import os


API = "https://apis.xditya.me/lyrics?song="

@Client.on_message(filters.text & filters.command(["genius"]) )
async def sng(bot, message):  
          genius = Genius(GENIUS_API)        
          mee = await message.reply_text("`Searching`")
          try:
              song = message.text.split(None, 1)[1] #.lower().strip().replace(" ", "%20")
          except IndexError:
              await message.reply("give me a query eg `lyrics faded`")
          chat_id = message.from_user.id
    #      rpl = lyrics(song)
          songGenius = genius.search_song(song)
          rpl = songGenius.lyrics
          await mee.delete()
          try:
            await mee.delete()
            await message.reply(rpl)
          except Exception as e:                            
             await message.reply_text(f"lyrics does not found for `{song} {e}`") #", quote = True, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url = f"https://t.me/Spotify newss")]]))
          finally:
            await message.reply("Check out @urlx_bot(music)  @shado_hackers(News)")



def search(song):
        r = requests.get(API + song)
        find = r.json()
        return find
       
def lyrics(song):
        fin = search(song)
        text = fin["lyrics"]
        return text
