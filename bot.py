import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s - %(name)s - [%(levelname)s]'
)
LOGGER = logging.getLogger(__name__)

api_id = 2772829 # int(os.environ.get("2772829"))
api_hash = "4b47a1310251bf8ce2e686c78525f55c" # os.environ.get("4b47a1310251bf8ce2e686c78525f55c")
bot_token = "1988366772:AAFYZoN0BU2SzsIL9fLTlP1gK541vqxir3Y" # "1962101886:AAHCO69yx06gyFCGylT3g2Peaaw-rQSVuhU" # os.environ.get("1962101886:AAHCO69yx06gyFCGylT3g2Peaaw-rQSVuhU")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))

async def start(event):
  await event.reply("Salam 👋\n\nMən sizin əvəzinizdən qruplarnızda istifadəçiləri tag edə bilərəm.\n\nHaqqımda daha ətraflı məlumat əldə etmək üçün /help əmrinə toxunun.",
                    buttons=(
                      [[Button.url('🌟 Məni bir qrupa əlavə et', 'https://t.me/RichTaggerBot?startgroup=true')],
                      [Button.url('📣 Yeniliklər', 'https://t.me/RichTaggerYenilikler'),
                      Button.url('🛠 Support', 'https://t.me/RichTaggerSupport')]]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Rich Tagger Bot'un Kömək Menyusu**\n\nƏmr: /all \n  Bu əmri başqalarına izah etmək istədiyiniz mətnlə istifadə edə bilərsiniz. \n`Nümunə: /all Salam Dostlar!`  \nBu əmri cavab olaraq istifadə edə bilərsiniz. Hər hansı bir mesaj Bot istifadəçiləri cavablandırılan mesaja etiketləyəcək"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Məni bir qrupa əlavə et', 'https://t.me/RichTaggerBot?startgroup=true'),
                       Button.url('📣 Support', 'https://t.me/RichTaggerSupport')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu əmr qruplarda və kanallarda istifadə edilə bilər❗__")

  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnız adminlər tərəfindən qeyd edilə bilər❗__")

  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Köhnə yazıların üzvlərindən bəhs edə bilmərəm! (qrupa əlavə etməzdən əvvəl göndərilən mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Mənə bir arqument ver❗__")
  else:
    return await event.respond("__Başqalarını qeyd etmək üçün bir mesaja cavab verin və ya mənə bir mesaj verin❗__")

  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("**Proses uğurla dayandırıldı** ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg}\n{usrtxt}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)

    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("**Proses uğurla dayandırıldı** ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

Ye
print(">> Bot işləyir narahat olma, 🚀 məlumat almaq üçün @muellime <<")
client.run_until_disconnected()
