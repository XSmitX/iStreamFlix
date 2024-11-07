import asyncio  # Import asyncio for handling async tasks
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from pyrogram.enums import ChatMemberStatus
from api import search_movie_or_tv
from serverchecker import check_stream_availability 
from vidsrc_pro_api import VidSrcProAPI
bot = Client("mybot1",
             bot_token="7333255087:AAHCgXLpSUQacvoAAtxufYaeyhUFNYF_wc0",
             api_id=1712043,
             api_hash="965c994b615e2644670ea106fd31daaf"
             )
global serverchange
serverchange = False
channelid = -1002305684598
channel_username = '@iStreamFlix_channel'
admins = [6121699672]
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
stickers = 'CAACAgQAAxkBAAEVCJRnFViSzaM1mPE-xzSss1fY23ay-wACuBkAAv4zCFAU6_rO_T679zYE'

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
@bot.on_message(filters.command("start") )
async def start_command(bot, message):
    await bot.send_sticker(message.chat.id, stickers)
    await bot.send_message(message.chat.id, "<b>Send me movie name or series name with its season and episode like 'breaking bad S3E4'</b>")

@bot.on_message(filters.command(["SERVER1", "SERVER2"], prefixes="/") & filters.private)
async def Change_SRVR(bot, message):
    global serverchange

    if message.from_user.id not in admins:
        await bot.send_message(message.chat.id, "<b><i>Only the admin can add chat IDs.</i></b>")
        return
    if message.text == '/SERVER1':
        serverchange = True
        await bot.send_message(message.chat.id, "<b><i>SERVER CHANGED to VIDLINK.PRO...</i></b>")
    
    if message.text == '/SERVER2':
        serverchange = False
        await bot.send_message(message.chat.id, "<b><i>SERVER CHANGED to MULTIPLE...</i></b>")
    


# Help command
@bot.on_message(filters.command("help"))
async def help_command(bot, message):
    await bot.send_message(message.chat.id, "<b>For <u>M@Vies </u> : - Enter only M0vie Name \n\t\tEX : Fight Club\n\nFor <u>TV/Series</u> : - Enter query along with its Season and Episode.\n\t\tEX : Breaking Bad S3E4 \n\t S means season-E means episode</b>")

# Asynchronous movie/TV search
@bot.on_message(filters.text & filters.private & check_joined())
async def on_message(bot, message):
    user_input = message.text
    print(serverchange)

    await bot.send_message(-1001855899992, f'Title : {user_input}\nUser : ``{message.from_user.id}`` or @{message.from_user.username}')
    
    result, updated_string, s_value, e_value = check_and_extract_SE(user_input)
    search_message = await message.reply_text('📤')
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

    async def Vidsrc_nl(VidSrcNL_SERVERS, search_message, message):
        try:
            # Gather the availability status of streams
            result = await asyncio.gather(*(check_stream_availability(vid) for vid in VidSrcNL_SERVERS))
        except:
            pass
            return None

        # Filter the available streams
        available_streams = [VidSrcNL_SERVERS[i] for i, available in enumerate(result) if available]

        # If no streams are available, delete the search message and return
        if not available_streams:
            await search_message.delete()
            return

        # Create button rows dynamically
        button_rows = []
        for index, lim in enumerate(available_streams):
            if 'hindi.vidsrc.nl' in lim:
                # Set button text to 'Hindi Server' if the URL contains 'hindi.vidsrc.nl'
                button_text = 'Hindi Server'
            else:
                # Otherwise, use 'Server X'
                button_text = f'Server {index + 1}'

            # Append the button to the rows
            button_rows.append([ikb(button_text, url=lim)])

        return button_rows



    async def handle_movie_streams():
        year = mdetails['release_date']
        api = VidSrcProAPI()
        VIdSrcPro = f'https://vidlink.pro/movie/{id}?autoplay=true'
        Server3 = f'https://embed.su/embed/movie/{id}'
        resulttt = await api.check_class_sync(VIdSrcPro, 'dark')
        await search_message.delete()
        search_message2 = await message.reply_text('📥')
        

        print(resulttt)
        if serverchange == True:
            if resulttt:
                button_rows = [[ikb('Extra Server', url=VIdSrcPro)]]
                button_rows.append([ikb('Server 3', url=Server3)])
                await search_message2.delete()
                await bot.send_message(message.chat.id, f'<b>Title : {name}\nRelease Date : {year}\nType : Movie</b>', reply_markup=ikm(button_rows))
            else:
                await search_message2.delete()
                await bot.send_message(message.chat.id,'<b>No Streams Found .....</b>')
            return
        vidcloud = [
            f'https://upstream.vidsrc.nl/stream/movie/{id}',
            f'https://hindi.vidsrc.nl/embed/movie/{id}'
        ]
        button_rows = await Vidsrc_nl(vidcloud, search_message, message)
        if button_rows:
            await search_message2.delete()
            await bot.send_message(message.chat.id,"<code><b>Trying to Add More Servers. . .</b></code>")
            if resulttt:
                button_rows[0].append(ikb('Extra Server', url=VIdSrcPro))
                button_rows.append([ikb('Server 3', url=Server3)])
                await bot.send_message(message.chat.id, f'<b>Title : {name}\nRelease Date : {year}\nType : Movie</b>', reply_markup=ikm(button_rows))
            else:
                await bot.send_message(message.chat.id,'<b>No Extra Servers Found. . .</b>')
                button_rows.append([ikb('Server 3', url=Server3)])
                await bot.send_message(message.chat.id, f'<b>Title : {name}\nRelease Date : {year}\nType : Movie</b>', reply_markup=ikm(button_rows))
        else:
            if resulttt:
                button_rows = [[ikb('Extra Server', url=VIdSrcPro)]]
                button_rows.append([ikb('Server 3', url=Server3)])
                await search_message2.delete()
                await bot.send_message(message.chat.id, f'<b>Title : {name}\nRelease Date : {year}\nType : Movie</b>', reply_markup=ikm(button_rows))
            else:
                await search_message2.delete()
                await bot.send_message(message.chat.id,'<b>No Extra Servers Found. . .</b>')
                
    async def handle_tv_streams():
        if not result:
            await search_message.delete()
            await message.reply_text(f'<b>No episode/seasons found in your text: {updated_string}. Please mention season and episode in the format S4E2.</b>')
            return
        api = VidSrcProAPI()
        s = s_value
        e = e_value
        vidsrcNl = f'https://vidlink.pro/tv/{id}/{s}/{e}'
        resulttt = await api.check_class_sync(vidsrcNl, 'dark')
        await search_message.delete()
        search_message2 = await bot.send_message(message.chat.id, '📥')
        if serverchange == True:
            if resulttt:
                button_rows = [[ikb('Extra Server', url=vidsrcNl)]]
                await search_message2.delete()
                await bot.send_message(
                    message.chat.id,
                    f'<b>Title : {name}\nSeason : {s}\nEpisode : {e}</b>',
                    reply_markup=ikm(button_rows)
                )
            else:
                await search_message2.delete()
                await bot.send_message(message.chat.id,'<b>No Streams Found .....</b>')
            return

        vidcloud = [
            f'https://upstream.vidsrc.nl/stream/tv/{id}/{s}/{e}',
            f'https://english.vidsrc.nl/stream/tv/{id}/{s}/{e}',
            f'https://hindi.vidsrc.nl/embed/tv/{id}/{s}/{e}'
        ]
        button_rows = await Vidsrc_nl(vidcloud, search_message, message)
        if button_rows:
            if resulttt:
                button_rows[0].append(ikb('Extra Server', url=vidsrcNl))
                await search_message2.delete()
                await bot.send_message(
                    message.chat.id,
                    f'<b>Title : {name}\nSeason : {s}\nEpisode : {e}</b>',
                    reply_markup=ikm(button_rows)
                )
                return
            else:
                await search_message2.delete()
                await bot.send_message(message.chat.id,'<b>No Extra Servers Found. . .</b>')
                await bot.send_message(
                    message.chat.id,
                    f'<b>Title : {name}\nSeason : {s}\nEpisode : {e}</b>',
                    reply_markup=ikm(button_rows)
                )
                
        
        if resulttt:
            button_rows = [[ikb('Extra Server', url=vidsrcNl)]]
            await search_message2.delete()
            await bot.send_message(
                message.chat.id,
                f'<b>Title : {name}\nSeason : {s}\nEpisode : {e}</b>',
                reply_markup=ikm(button_rows)
            )
            return
        else:
            await search_message2.delete()
            await bot.send_message(message.chat.id,'<b>No Extra Servers Found. . .</b>')
            return


        

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

