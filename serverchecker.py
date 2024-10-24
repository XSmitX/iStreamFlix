import aiohttp
from bs4 import BeautifulSoup

async def check_stream_availability(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=20) as response:
                if response.status != 200:
                    print(f"Failed --> Status code: {response.status}")
                    return False
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # First, check if the media-player tag exists and has a valid source
                media_player = soup.find('media-player')
                if media_player:
                    src = media_player.get('src')  # Try to get the source link
                    if src:
                        print("Stream is available: " + url)
                        return True
                    else:
                        print("No streaming link found (src is empty).")
                        return False

                # If media-player tag doesn't exist or src is empty, check body text
                body_text = soup.get_text().strip()
                print("Debug: Full Body Content:\n", body_text, "\n")

                # Check for known error messages in the page body
                error_messages = [
                    "streaming link not found",
                    "stream is not available",
                    "unable to load stream",
                    "no streams found"
                ]

                if any(error_message in body_text.lower() for error_message in error_messages):
                    print("Stream is not available: " + url)
                    return False
                else:
                    print("Stream is available: " + url)
                    return True

    except aiohttp.ClientError as e:
        print(f"Error occurred while fetching the stream: {e}")
        return False
