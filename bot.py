import asyncio  # Import asyncio for handling async tasks
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from api import search_movie_or_tv
from serverchecker import check_stream_availability
import re
from pyrogram.enums import ChatMemberStatus
import random

bot = Client("mybot1",
             bot_token="7333255087:AAHCgXLpSUQacvoAAtxufYaeyhUFNYF_wc0",
             api_id=1712043,
             api_hash="965c994b615e2644670ea106fd31daaf"
             )

channelid = -1002305684598
channel_username = '@iStreamFlix_channel'

# Check if the user has joined the channel
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
                await bot.send_message(chat_id, join_msg, reply_markup=ikm([[ikb("✅ Join Channel", url="https://t.me/iStreamFlix_channel")]]))
                return False
        except Exception:
            await bot.send_message(chat_id, join_msg, reply_markup=ikm([[ikb("✅ Join Channel", url="https://t.me/iStreamFlix_channel")]]))
            return False

    return filters.create(func)

# Stickers list
stickers = ['CAACAgQAAxkBAAEVCJRnFViSzaM1mPE-xzSss1fY23ay-wACuBkAAv4zCFAU6_rO_T679zYE', 'CAACAgQAAxkBAAEVCJZnFVi3kNEefSkvP7CtbZaPFSb8mQAC6woAAukaCFCrUZcUM5emJjYE']

# Check and extract season/episode
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

# Start command
@bot.on_message(filters.command("start"))
async def start_command(bot, message):
    await bot.send_sticker(message.chat.id, random.choice(stickers))
    await bot.send_message(message.chat.id, "<b>Send me movie name or series name with its season and episode like 'breaking bad S3E4'</b>")

# Help command
@bot.on_message(filters.command("help"))
async def help_command(bot, message):
    await bot.send_message(message.chat.id, "<b>For <u>M@Vies </u> : - Enter only M0vie Name \n\t\tEX : Fight Club\n\nFor <u>TV/Series</u> : - Enter query along with its Season and Episode.\n\t\tEX : Breaking Bad S3E4 \n\t S means season-E means episode</b>")

# Asynchronous movie/TV search
@bot.on_message(filters.text & filters.private & check_joined())
async def on_message(bot, message):
    user_input = message.text
    await bot.send_message(-1001855899992, f'Title : {user_input}\nUser : ``{message.from_user.id}`` or @{message.from_user.username}')
    
    result, updated_string, s_value, e_value = check_and_extract_SE(user_input)
    search_message = await message.reply_text('<b>Sᴇᴀʀᴄʜɪɴɢ ...</b>')
    
    # Perform the search concurrently to avoid blocking
    mdetails = await asyncio.to_thread(search_movie_or_tv, updated_string)
    
    if not mdetails:
        await search_message.delete()
        await message.reply_text('<b>Movie/Series Not found or Incorrect Spelling. Use /help to know more.</b>')
        return
    
    try:
        name = mdetails.get('title', mdetails.get('name'))
        id = mdetails['id']
    except KeyError:
        await search_message.delete()
        await message.reply_text('<b>Invalid Movie/Series Data.</b>')
        return

    async def handle_movie_streams():
        year = mdetails['release_date']
        vidcloud = [
            f'https://vidcloud.vidsrc.nl/stream/movie/{id}',
            f'https://upstream.vidsrc.nl/stream/movie/{id}',
            f'https://english.vidsrc.nl/embed/movie/{id}',
            f'https://hindi.vidsrc.nl/embed/movie/{id}'
        ]
        mvs = await asyncio.gather(*(check_stream_availability(vid) for vid in vidcloud))
        available_streams = [vidcloud[i] for i, available in enumerate(mvs) if available]

        if not available_streams:
            await search_message.delete()
            await message.reply_text('<b>No Stream Found.</b>')
            return

        button_rows = [[ikb(f'Server {index + 1}', url=lim)] for index, lim in enumerate(available_streams)]
        await search_message.delete()
        await bot.send_message(message.chat.id, f'<b>Title : {name}\nRelease Date : {year}\nType : Movie</b>', reply_markup=ikm(button_rows))

    async def handle_tv_streams():
        if not result:
            await search_message.delete()
            await message.reply_text(f'<b>No episode/seasons found in your text: {updated_string}. Please mention season and episode in the format S4E2.</b>')
            return

        s = s_value
        e = e_value
        vidcloud = [
            f'https://vidcloud.vidsrc.nl/stream/tv/{id}/{s}/{e}',
            f'https://upstream.vidsrc.nl/stream/tv/{id}/{s}/{e}',
            f'https://english.vidsrc.nl/stream/tv/{id}/{s}/{e}',
            f'https://hindi.vidsrc.nl/embed/tv/{id}/{s}/{e}'
        ]
        mvs = await asyncio.gather(*(check_stream_availability(vid) for vid in vidcloud))
        available_streams = [vidcloud[i] for i, available in enumerate(mvs) if available]

        if not available_streams:
            await search_message.delete()
            await message.reply_text('<b>No Stream Found.</b>')
            return

        button_rows = [[ikb(f'Server {index + 1}', url=lim)] for index, lim in enumerate(available_streams)]
        await search_message.delete()
        await bot.send_message(message.chat.id, f'<b>Title : {name}\nSeason : {s}\nEpisode : {e}</b>', reply_markup=ikm(button_rows))

    # Handle movie or TV based on the type
    if mdetails['type'] == 'movie':
        await handle_movie_streams()
    elif mdetails['type'] == 'tv':
        await handle_tv_streams()
    else:
        await search_message.delete()
        await message.reply_text('<b>No results found.</b>')

# Run the bot
bot.run()
