from pyrogram import filters,Client as Mbot
from plugins.info import LOG_GROUP as DUMP_GROUP,BUG as LOG_GROUP
import os,re,asyncio,bs4
import requests,wget,traceback

@Mbot.on_message(filters.regex(r'https?://.*twitter[^\s]+') & filters.incoming | filters.regex(r'https?://(?:www\.)?x\.com/\S+') & filters.incoming,group=-5)
async def twitter_handler(Mbot, message):
   try:            
      link=message.matches[0].group(0)
      if "x.com" in link:
         link=link.replace("x.com","fxtwitter.com")
      elif "twitter.com" in link:
         link = link.replace("twitter.com","fxtwitter.com")
      m=await message.reply_sticker("CAACAgIAAxkBATWhF2Qz1Y-FKIKqlw88oYgN8N82FtC8AAJnAAPb234AAT3fFO9hR5GfHgQ")
      try:
          dump_file = await message.reply_video(link,caption="Thank you for using - @urlx_bot")
      except Exception as e:
          print(e)
          try:
             snd_message=await message.reply(link)
             await asyncio.sleep(1)
             dump_file = await message.reply_video(link,caption="Thank you for using - @urlx_bot")
             await snd_message.delete()
          except Exception as e:
              print(e)
              await snd_message.delete()
              get_api=requests.get(link).text
              soup=bs4.BeautifulSoup(get_api,"html.parser")
              meta_tag= soup.find("meta", attrs = {"property": "og:video"})
              if not meta_tag:
                  meta_tag = soup.find("meta", attrs={"property": "og:image"})
              content_value  = meta_tag['content']
              try:
                  dump_file = await message.reply_video(content_value,caption="Thank you for using - @urlx_bot")
              except Exception as e:
                  print(e)
                  try:
                     snd_msg=await message.reply(content_value)
                     await asyncio.sleep(1)
                     await message.reply_video(content_value,caption="Thank you for using - @urlx_bot")
                     await snd_msg.delete()
                  except Exception as e:
                      print(e)
                      await message.reply("Oops Invalid link or Media Is Not Available:)")
   except Exception as e:
        print(e)
        if LOG_GROUP:
           await Mbot.send_message(LOG_GROUP,e)
           await Mbot.send_message(LOG_GROUP,traceback.format_exc())
   finally:
       if DUMP_GROUP:
          if "dump_file" in locals():
             await dump_file.copy(DUMP_GROUP)
       await m.delete()
       await message.reply("Check out @urlx_bot(music)  @omg_info(Channel) \n Please Support Us By /donate To Maintain This Project")               
                 
      @from pyrogram import filters, Client as Mbot

@Mbot.on_message(filters.regex(r'https?://.*facebook[^\s]+') & filters.incoming,group=-6)
async def link_handler(Mbot, message):
    link = message.matches[0].group(0)
    try:
       m = await message.reply_text("⏳")
       get_api=requests.get(f"https://yasirapi.eu.org/fbdl?link={link}").json()
       if get_api['success'] == "false":
          return await message.reply("Invalid TikTok video url. Please try again :)")
       if get_api['success'] == "ok":
          if get_api.get('result').get('hd'):
             try:
                 dump_file = await message.reply_video(get_api['result']['hd'],caption="Thank you for using - @InstaReelsdownbot")
             except KeyError:
                 pass 
             except Exception:
                 try:
                     sndmsg = await message.reply(get_api['result']['hd'])
                     await asyncio.sleep(1)
                     dump_file = await message.reply_video(get_api['result']['hd'],caption="Thank you for using - @InstaReelsdownbot")
                     await sndmsg.delete()
                 except Exception:
                     try:
                        down_file = wget.download(get_api['result']['hd'])
                        await message.reply_video(down_file,caption="Thank you for using - @InstaReelsdownbot")
                        await sndmsg.delete()
                        os.remove(down_file)
                     except:
                         return await message.reply("Oops Failed To Send File Instead Of Link")
          else: 
             if get_api.get('result').get('sd'):
               try:
                   dump_file = await message.reply_video(get_api['result']['sd'],caption="Thank you for using - @InstaReelsdownbot")
               except KeyError:
                   pass
               except Exception:
                   try:
                       sndmsg = await message.reply(get_api['result']['sd'])
                       await asyncio.sleep(1)
                       dump_file = await message.reply_video(get_api['result']['sd'],caption="Thank you for using - @InstaReelsdownbot")
                       await sndmsg.delete()
                   except Exception:
                      try:
                        down_file = wget.download(get_api['result']['sd'])
                        await message.reply_video(down_file,caption="Thank you for using - @InstaReelsdownbot")
                        await sndmsg.delete()
                        os.remove(down_file)
                      except:
                         return await message.reply("Oops Failed To Send File Instead Of Link")
    except Exception as e:
           if LOG_GROUP:
               await Mbot.send_message(LOG_GROUP,f"Facebook {e} {link}")
               await Mbot.send_message(LOG_GROUP, traceback.format_exc())          
    finally:
          if 'dump_file' in locals():
            if DUMP_GROUP:
               await dump_file.copy(DUMP_GROUP)
          await m.delete()     
