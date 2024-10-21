
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from api import *
from serverchecker import *
import re
from pyrogram.enums import ChatMemberStatus
import random
bot = Client("mybot1",
             bot_token="7333255087:AAGwGyKJABm8FohsVdZJamRedZyiGyBHBYI",
             api_id=1712043,
             api_hash="965c994b615e2644670ea106fd31daaf"
             )
channelid = -1002305684598
channel_username = '@iStreamFlix_channel'


def check_joined():
    async def func(flt, bot, message):
        join_msg = f"**To use this bot, Please join our channel.\nJoin From The Link Below 👇**"
        user_id = message.from_user.id
        chat_id = message.chat.id
        try:
            member_info = await bot.get_chat_member(channel_username, user_id)
            if member_info.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER):
                return True
            else:
                await bot.send_message(chat_id, join_msg , reply_markup=ikm([[ikb("✅ Join Channel", url="https://t.me/iStreamFlix_channel")]]))
                return False
        except Exception as e:
            await bot.send_message(chat_id, join_msg , reply_markup=ikm([[ikb("✅ Join Channel", url="https://t.me/iStreamFlix_channel")]]))
            return False

    return filters.create(func)
    
stickers = ['CAACAgQAAxkBAAEVCJRnFViSzaM1mPE-xzSss1fY23ay-wACuBkAAv4zCFAU6_rO_T679zYE','CAACAgQAAxkBAAEVCJZnFVi3kNEefSkvP7CtbZaPFSb8mQAC6woAAukaCFCrUZcUM5emJjYE','CAACAgUAAxkBAAEVCJhnFVjccy8K5LSIB-FTL6x3YGt6_QACAg0AAiYECVaxxKu5C6qiTDYE','CAACAgUAAxkBAAEVCJpnFVlZ3x9QbFWvX5yaPD9SvYFBewACcwkAAvdGgVbuMRIz-x2CAjYE','CAACAgUAAxkBAAEVCJxnFVlrW-YB25_IB5JrjG29347waAACewsAApSSgVYlDOQTuQ81azYE','CAACAgUAAxkBAAEVCJ5nFVmGSjXIZQcJEzbP3h82nDRbUwACVw4AAo9j0VSQSl-t8eMTnTYE','CAACAgUAAxkBAAEVCIRnFVZ7DKdNxeXfHvFMPl2KXkiLBgACFwoAAnzTGVSJXsdV7fH-7jYE','CAACAgUAAxkBAAEVCIhnFVcm6i-xBf-NiK8hSddIYB7b1wAClAkAAsfseFbtd_G4kWuihTYE','CAACAgUAAxkBAAEVCIZnFVcMCwxn3W6tJcYrKC38Ml_2NgACiAoAArfYEVbq36fDWr-wyjYE','CAACAgUAAxkBAAEVCIpnFVdBd10me-YLgj5dbss2tSnmQgACWggAAnJUgVYe4mehRol3BDYE','CAACAgUAAxkBAAEVCIxnFVd4s0ljFS0hFyF9N0x1XEjo2QAC9AQAAlnPuVQEfS3PMURWcDYE','CAACAgQAAxkBAAEVCI5nFVeV3yzZQ4jm9lROILwVRSUniAACdwsAAlSPCVAIYu1Y94XdJzYE']
sticker = random.choice(stickers)
def check_and_extract_SE(string):
    pattern = r'[Ss](\d+)[Ee](\d+)'


    match = re.search(pattern, string)

    if match:
        s_value = int(match.group(1))
        e_value = int(match.group(2))
        updated_string = re.sub(pattern, '', string).strip()

        return True, updated_string, s_value, e_value
    else:
        return False, string, None, None
join_msg = '<b>Join our main channel to use bot.</b>'
@bot.on_message(filters.command("start"))
async def start_command(bot, message):
    user = message.from_user.id
    await bot.send_sticker(message.chat.id, random.choice(stickers))
    await bot.send_message(message.chat.id, "<b>Send me movie name or series name with its season and episode like 'breaking bad S3E4'\n\nIF STREAMING LINK DOESN'T WORKING THEN USE 1.1.1.1 'BOT GIVES ONLY WORKING STREAMING LINK'</b>")

@bot.on_message(filters.command("help"))
async def start_command(bot, message):
    await bot.send_message(message.chat.id, "<b>For <u>M@Vies </u> : - Enter only M0vie Name \n\t\tEX : Fight Club\n\nFor <u>TV/Series</u> : - Enter query along with its Season and Episode.\n\t\tEX : Breaking Bad S3E4 \n\t S means season-E means episode</b>")

@bot.on_message(filters.text & filters.private & check_joined())
async def on_message(bot, message):
    x1 = message.text
    await bot.send_message(-1001855899992,f'Title : {x1}\nUser : ``{message.from_user.id}`` or @{message.from_user.username}')
    result, updated_string, s_value, e_value = check_and_extract_SE(x1)
    print(result)
    if result:
        print(f'Pattern found and removed: "{updated_string}"\n'
              f'S value: {s_value}, E value: {e_value}')
    else:
        print(f'Pattern not found, original string: {updated_string}')
    
    Search = await message.reply_text('<b>Sᴇᴀʀᴄʜɪɴɢ ...</b>')
    mdetails = search_movie_or_tv(updated_string)
    
    try:
        id = mdetails['id']
    except:
        await Search.delete()
        await message.reply_text('<b><u>Movie/Series Not found</u> or <u>Incorrect Spelling.</u>\nalso make sure you have entered in the correct format.\nUse /help to know more.</b>')
        return
    
    try:
        name = mdetails['title']
    except:
        name = mdetails['name']
    

    if mdetails['type'] == 'movie':
        year = mdetails['release_date']
        mvs = []
        vidcloud = [f'https://vidcloud.vidsrc.nl/stream/movie/{id}', f'https://upstream.vidsrc.nl/stream/movie/{id}', f'https://english.vidsrc.nl/embed/movie/{id}', f'https://hindi.vidsrc.nl/embed/movie/{id}']
        for vid in vidcloud:
            checking = check_stream_availability(vid)
            if checking == True:
                mvs.append(vid)

        if mvs == []:
            await Search.delete()
            NoStream = await bot.send_message(message.chat.id, '<b>No Stream Found ....</b>')
            #await NoStream.delete()
            return

        button_rows = []
        skip_last = False
        for index,lim in enumerate(mvs):
            if lim.startswith('https://hindi.'):
                button_rows.append([ikb(f'Hindi Server', url=lim)])
                skip_last = True

            if not skip_last:
                button_rows.append([ikb(f'Server {index + 1}', url=lim)])
        keyboard = ikm(button_rows)
        await Search.delete()
        await bot.send_message(message.chat.id, f'<b>Title : {name}. \nRelease Date : {year}.Type : Movie.</b>', reply_markup=keyboard)
    elif mdetails['type'] == 'tv':
        if result == False:
            await Search.delete()
            await bot.send_message(message.chat.id, f'<b>No episode/seasons found in your text :-<u>{updated_string}</u>.\n\nPlease mention {updated_string} S4E2 means 4th season and 2nd episode...</b>')
            return
        s = s_value
        e = e_value
        mvs = []
        vidcloud = [f'https://vidcloud.vidsrc.nl/stream/tv/{id}/{s}/{e}', f'https://upstream.vidsrc.nl/stream/tv/{id}/{s}/{e}', f'https://english.vidsrc.nl/stream/tv/{id}/{s}/2{e}', f'https://hindi.vidsrc.nl/embed/tv/{id}/{s}/{e}']
        for vid in vidcloud:
            checking = check_stream_availability(vid)
            if checking == True:
                mvs.append(vid)
     
        if mvs == []:
            await Search.delete()
            await bot.send_message(message.chat.id, '<b>No Stream Found ....</b>')
            return
        button_rows = []
        skip_last = False
        for index,lim in enumerate(mvs):
            if lim.startswith('https://hindi.'):
                button_rows.append([ikb(f'Hindi Server', url=lim)])
                skip_last = True

            if not skip_last:
                button_rows.append([ikb(f'Server {index + 1}', url=lim)])

# Create the keyboard with the button rows
        keyboard = ikm(button_rows)
        await Search.delete()
        await bot.send_message(message.chat.id, f'<b>Title : <u>{name}</u>.\nType : TV Show/Web Series.\nSeason : [ {s} ] - Episode : [ {e} ]</b>', reply_markup=keyboard)
    else:
        await Search.delete()
        await bot.send_message(message.chat.id, 'No results found')


bot.run()
