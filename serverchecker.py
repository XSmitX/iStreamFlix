import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def check_stream_availability(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    print(f"Failed --> Status code: {response.status}")
                    return False

                # Parse the HTML using BeautifulSoup
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # First, check if the media-player tag exists and has a valid source
                try:
                    media_player = soup.find('media-player')
                    if media_player:
                        src = media_player.get('src')  # Try to get the source link
                        if src:
                            print(f"Stream is available: {url}")
                            return True
                        else:
                            print(f"No streaming link found in 'media-player' tag for {url}.")
                            return False

                    # If no media-player tag, check body text for specific error messages
                    body_text = soup.get_text().strip()

                    # List of error messages indicating stream unavailability
                    error_messages = [
                        "streaming link not found",
                        "stream is not available",
                        "unable to load stream",
                        "no streams found",
                        "video not available"
                        ]

                    if any(error_message in body_text.lower() for error_message in error_messages):
                        print(f"Stream is not available (Error message found) for {url}")
                        return False

                    # If none of the errors were detected, assume the stream is available
                    print(f"Stream is available: {url}")
                except:
                    pass
                return True

    # Handling specific client-related errors such as connection issues
    except aiohttp.ClientError as e:
        print(f"Client error occurred while fetching the stream for {url}: {e}")
        return False
    # Handling timeout errors
    except asyncio.TimeoutError:
        print(f"Timeout occurred while fetching the stream for {url}")
        return False
    
