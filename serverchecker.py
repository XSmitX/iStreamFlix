import requests
from bs4 import BeautifulSoup

def check_stream_availability(url):
    try:
        session = requests.Session
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            print(f"Failed --> Status code: {response.status_code}")
            return
        soup = BeautifulSoup(response.content, 'html.parser')
        
        try:
            media_player = soup.find('media-player')
            if media_player:
                try:
                    src = media_player.get('src') 
                    print(src)
                except:
                    print("Failed --> URL.")
                    return
                if src: 
                    print("Stream is available." + url)
                    return True
                else:
                    print("No streaming link found (src is empty).")
                    return False
            else:
                print("Stream is not available (media-player not found).")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")

        body_text = soup.get_text().strip()
        print(body_text)
        print("Debug: Full Body Content:\n", body_text, "\n")

        error_messages = [
            "streaming link not found",
            "stream is not available",
            "unable to load stream",
            "no streams found"
        ]

        if any(error_message in body_text.lower() for error_message in error_messages):
            print("Stream is not available." + (url))
        else:
            print("Stream is available." + (url))

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the stream: {e}")

